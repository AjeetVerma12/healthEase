from flask import Flask, render_template, request, make_response,jsonify, flash, redirect, request, url_for, session
from flaskext.mysql import MySQL
import pymysql
from pymysql.cursors import DictCursor
import pandas as pd
import numpy as np
from datetime import date
import time
import mysql.connector

app = Flask(__name__)
# app.secret_key = b'$3cr3tK3y!'

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

@app.route('/')
@app.route('/LoginPatient', methods=['GET', 'POST'])
def LoginPatient():
    if request.method == 'POST':
        # Get form data
        enroll = request.form['PatientEnrollment']
        password = request.form['PatientPassword']

        query = "SELECT * FROM Login WHERE enroll=%s AND pass=%s"
        values = (enroll, password)
        cursor.execute(query, values)
        result = cursor.fetchone()

        # If login credentials are correct, redirect to home page
        if result:
            return redirect(url_for('home'))

        # If login credentials are incorrect, show error message
        else:
            error = 'Invalid email or password. Please try again.'
            return render_template('LoginPatient.html', error=error)

    return render_template('LoginPatient.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/DoctorLogin')
def DoctorLogin():
    return render_template("DoctorLogin.html")

if __name__ == '__main__':
    app.run(debug=True)
