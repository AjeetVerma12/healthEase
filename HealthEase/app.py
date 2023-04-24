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

# MySQL connection details
mysql_user = 'root'
mysql_password = 'your_mysql_password'
mysql_host = 'localhost'
mysql_database = 'your_database_name'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        # Connect to MySQL database
        conn = mysql.connector.connect(user=mysql_user, password=mysql_password,
                                       host=mysql_host, database=mysql_database)

        # Create a cursor object
        cursor = conn.cursor()

        # Insert form data into MySQL table
        query = "INSERT INTO messages (name, email, message) VALUES (%s, %s, %s)"
        values = (name, email, message)
        cursor.execute(query, values)

        # Commit changes to database
        conn.commit()

        # Close database connection
        cursor.close()
        conn.close()

        return "Data stored successfully in MySQL database!"

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
