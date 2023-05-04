from flask import Flask, render_template, request, make_response,jsonify, flash, redirect, request, url_for, session
from flaskext.mysql import MySQL
import pymysql
from pymysql.cursors import DictCursor
import pandas as pd
import numpy as np
from datetime import date
import time
import mysql.connector
import datetime



app = Flask(__name__)
app.secret_key = b'\x0f\xcf\xf0w\xdc\x93f\xd7\xa8\xffs^'

mysql = MySQL(autocommit = True, cursorclass = pymysql.cursors.DictCursor)
mysql.init_app(app)

# configuring MySQL for the web application
app.config['MYSQL_DATABASE_USER'] = 'root'   
app.config['MYSQL_DATABASE_PASSWORD'] = 'password' 
app.config['MYSQL_DATABASE_DB'] = 'Students'  
app.config['MYSQL_DATABASE_HOST'] = 'localhost' 


#initialise mySQL
#create connection to access data
conn = mysql.connect()
cursor = conn.cursor()


@app.route('/LoginPatient', methods=['GET', 'POST'])
def LoginPatient():
    if request.method == 'POST':
        # Get form data
        enroll = request.form['PatientEnrollment']
        password = request.form['PatientPassword']
        

        query = "SELECT * FROM LoginPatient WHERE enroll = %s AND pass=%s"
        # query = "SELECT * FROM LoginPatient where enroll = '" + enroll+ "' and pass = '" + password+ "'"

        values=(enroll,password)
        cursor.execute(query,values)
        print(query)
        result = cursor.fetchall()
        print(result)

        # If login credentials are correct, redirect to home page
        if result:
            session["loggedin"] = True
            session["enroll"]= enroll
            return redirect(url_for('home'))

        # If login credentials are incorrect, show error message
        else:
            error = 'Invalid email or password. Please try again.'
            return render_template('LoginPatient.html', error=error)

    return render_template('LoginPatient.html')

@app.route('/')
@app.route('/home')
def home():
    # check if user is logged in or not
    if 'loggedin' in session:
        user_is_logged_in = True
    else:
        user_is_logged_in = False
    return render_template('home.html', user_is_logged_in=user_is_logged_in)

@app.route('/DoctorLogin' ,methods=['GET', 'POST'])
def DoctorLogin():
    if request.method == 'POST':
        # Get form data
        DocID = request.form['DocID']
        password = request.form['DoctorPassword']

        query = "SELECT * FROM LoginDoctor WHERE DocID=%s AND pass=%s"
        values = (DocID, password)
        cursor.execute(query, values)
        result = cursor.fetchone()

        # If login credentials are correct, redirect to home page
        if result:
            session['loggedin'] = True
            session['DocID']=result['DocID']
            return redirect(url_for('home'))

        # If login credentials are incorrect, show error message
        else:
            error = 'Invalid email or password. Please try again.'
            return render_template('DoctorLogin.html', error=error)

    return render_template('DoctorLogin.html')

@app.route('/request' , methods=['GET','POST'])
def requests():
    # check if user is logged in or not
    if 'loggedin' in session:
        if 'enroll' in session:
            if request.method == 'POST':
                # return render_template('request.html')
            #Get Form data
                name= request.form['Pname']
                number=request.form['number']
                enroll= request.form['enroll']
                gender= request.form['gender']
                age= request.form['age']
                requirement= request.form['requirement']
                medname= request.form['medname']
                symptoms=request.form['symptoms']
                prescription=request.files['prescription']  #prescription or filename
                date = datetime.datetime.now()

                query= "Insert into requests values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                values=(name,number,enroll,gender,age,requirement,medname,symptoms,prescription,date)
                cursor.execute(query,values)

                return redirect(url_for('home'))
            
    else:
        return redirect(url_for('LoginPatient'))
    
    return render_template('request.html')

        #session['name']= fetch from mysql
    # if 'user_id' in session:
        # Connect to the MySQL database
    #     cnx = mysql.connector.connect(**db_config)
    #     cursor = cnx.cursor()

    #     # Fetch data from the MySQL table based on the session variable value
    #     query = "SELECT * FROM your_table_name WHERE user_id = %s"
    #     cursor.execute(query, (session['user_id'],))
    #     data = cursor.fetchall()

    #     # Close the MySQL database connection
    #     cursor.close()
    #     cnx.close()

    #     # Pass the data to the HTML template for rendering
    #     return render_template('data.html', data=data)
    # else:
    #     # Redirect to the login page if the session variable is not set
    #     return redirect('/login')

@app.route('/dashboard' , methods=['GET','POST'])
def dashboard():
# check if user is logged in or not
    if 'loggedin' in session:
        if 'enroll' in session:
            enrollment=session['enroll']
            query = "select Pname from Students where enroll=%s"
            values = (enrollment,)
            cursor.execute(query,values)
            result = cursor.fetchone()
            print(result)
            return render_template('dashboard.html',result=result)
        elif 'DocID' in session:
            return render_template('dashboard1.html')
    else:
        return redirect(url_for('LoginPatient'))
    # return render_template('dashboard.html')

@app.route('/book' , methods=['GET','POST'])
def book():
    if request.method == "POST":
        name= request.form['name']
        phone= request.form['phone']
        email = request.form ['email']

        query = "Insert into HealthCampBooking values(%s,%s,%s)"
        values = (name,phone,email)
        cursor.execute(query,values)
        #create a table for appointments

        return redirect(url_for('home'))


@app.route('/logout')
def Logout():
    #session variable
    # if 'enroll' in session:
    session.pop('enroll',None)
    # elif 'DocID' in session:
    session.pop("DocID",None)
    session.pop('loggedin',None)
    return redirect(url_for('home'))

@app.route('/your-prescriptions')
def yourprescriptions():
    # fetch user
    if 'enroll' in session:
        #to be added: date and time of prescription record
        enrollment = session['enroll']
        query = "select* from prescriptions where enroll=%s"
        values = (enrollment,)
        cursor.execute(query,values)
        result = cursor.fetchall()
        print(result)

        return render_template('your-prescriptions.html', result=result)




if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
