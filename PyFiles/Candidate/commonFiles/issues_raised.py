from datetime import datetime, date
import random
import mysql.connector
import requests
import os
from flask_mail import Mail, Message
from classes.connection import HostConfig, ConfigPaths
from flask import Blueprint, render_template, session, request, jsonify, flash, Response

issue_raised_blueprint = Blueprint('issue_raised', __name__)


def issue_raised_auth(app, mail):
    # ------ HOST Configs are in classes/connection.py
    host = HostConfig.host
    app_paths = ConfigPaths.paths.get(host)
    if app_paths:
        for key, value in app_paths.items():
            app.config[key] = value

    @issue_raised_blueprint.route('/issues_raised_students', methods=['GET', 'POST'])
    def issues_raised_students():
        email = session['email']
        print(email)
        cnx = mysql.connector.connect(user='root', password='A9CALcsd7lc%7ac',
                                      host=host,
                                      database='ICSApplication')
        cursor = cnx.cursor(dictionary=True)
        if request.method == 'POST':
            ticket = '#' + str(random.randint(1000, 9999))
            current_datetime = datetime.now()
            date = current_datetime.strftime('%Y-%m-%d')
            time = current_datetime.strftime('%H:%M:%S')

            fullname = request.form['full_name']
            email = request.form['email']
            issue_subject = request.form['issue_subject']
            description = request.form['description']
            document = request.files['document']
            sql = """SELECT email, first_name FROM application_page where email=%s"""
            cursor.execute(sql, (email,))
            result = cursor.fetchall()
            if result:
                user = result[0]['first_name']
            else:
                user = 'Admin'
            if document.filename != '':
                photo_path = save_issue_raised_photo(document)
            else:
                photo_path = request.form['user_photo']

            cursor.execute(
                "INSERT INTO issue_raised (ticket, fullname, email, issue_subject, description, document, date, time) VALUES (%s, %s, %s,  %s, %s, %s, %s, %s)",
                (ticket, fullname, email, issue_subject, description, photo_path, date, time))
            cnx.commit()

            cnx = mysql.connector.connect(user='root', password='A9CALcsd7lc%7ac',
                                          host=host,
                                          database='ICSApplication')
            cursor = cnx.cursor(dictionary=True)
            sql = """SELECT * FROM issue_raised where email=%s"""
            cursor.execute(sql, (email,))
            # Fetch all records matching the query
            records = cursor.fetchall()
            # Close the cursor and database connection

            cursor.close()
            cnx.close()
            return render_template('Candidate/commonFiles/submitted_issue_raised.html', records=records, user=user)
        sql = """SELECT email, first_name FROM application_page where email=%s"""
        cursor.execute(sql, (email,))
        result = cursor.fetchall()
        if result:
            user = result[0]['first_name']
        else:
            user = 'Admin'
        cursor.close()
        cnx.close()
        return render_template('Candidate/commonFiles/issues_raised_students.html', user=user)

    @issue_raised_blueprint.route('/submitted_issue_raised', methods=['GET'])
    def submitted_issue_raised():
        email = session['email']
        cnx = mysql.connector.connect(user='root', password='A9CALcsd7lc%7ac',
                                      host=host,
                                      database='ICSApplication')
        cursor = cnx.cursor(dictionary=True)
        sql = """SELECT * FROM issue_raised where email=%s"""
        cursor.execute(sql, (email,))
        # Fetch all records matching the query
        records = cursor.fetchall()
        print(records)
        # Close the cursor and database connection
        cursor.close()
        cnx.close()
        return render_template('Candidate/commonFiles/submitted_issue_raised.html', records=records)

    def save_issue_raised_photo(file):
        if file:
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_PHOTO_SECTION1'], filename))
            # return os.path.join(app.config['UPLOAD_PHOTO_SECTION1'], filename)
            return '/static/uploads/image_retrive/' + filename
        else:
            return "Save File"