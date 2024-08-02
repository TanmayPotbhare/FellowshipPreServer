import mysql.connector
from classes.connection import HostConfig, ConfigPaths
from flask import Blueprint, render_template, session, request, redirect, url_for, flash
from authentication.middleware import auth

viewform_blueprint = Blueprint('viewform', __name__)


def viewform_auth(app):
    # ------ HOST Configs are in classes/connection.py
    host = HostConfig.host
    app_paths = ConfigPaths.paths.get(host)
    if app_paths:
        for key, value in app_paths.items():
            app.config[key] = value

    @viewform_blueprint.route('/viewform_old_users/<int:id>', methods=['GET', 'POST'])
    def viewform_old_users(id):  # -------------- VIEW STUDENT FORM
        cnx = mysql.connector.connect(user='root', password='A9CALcsd7lc%7ac',
                                      host=host,
                                      database='ICSApplication')
        cursor = cnx.cursor(dictionary=True)
        sql = """SELECT * FROM application_page WHERE id = %s"""
        cursor.execute(sql, (id,))
        # Fetch all records matching the query
        records = cursor.fetchall()
        print(records)
        # Close the cursor and database connection
        cursor.close()
        cnx.close()
        return render_template('form-view-olduser.html', records=records)

    @viewform_blueprint.route('/viewform/<int:id>', methods=['GET', 'POST'])
    def viewform(id):  # -------------- VIEW STUDENT FORM
        cnx = mysql.connector.connect(user='root', password='A9CALcsd7lc%7ac',
                                      host=host,
                                      database='ICSApplication')
        cursor = cnx.cursor(dictionary=True)
        sql = """SELECT * FROM application_page WHERE id = %s"""
        cursor.execute(sql, (id,))
        # Fetch all records matching the query
        records = cursor.fetchall()
        if records:
            user = 'User'
        else:
            user = 'Admin'
        topic_of_phd_utf8_list = []

        # Iterate over each record and extract the value of 'topic_of_phd' column
        for record in records:
            # Assuming 'topic_of_phd' is the 42nd column in your query result

            topic_of_phd = record['topic_of_phd']
            # Encode the topic_of_phd as UTF-8 and append it to the list
            topic_of_phd_utf8 = topic_of_phd.encode('utf-8')
            topic_of_phd_utf8_list.append(topic_of_phd_utf8)

        # Close the cursor and database connection
        cursor.close()
        cnx.close()
        return render_template('Candidate/OldUser/form-view.html', records=records,
                               topic_of_phd_utf8_list=topic_of_phd_utf8_list, user=user)

    @viewform_blueprint.route('/mainpage')
    @auth
    def main_page():  # -------------- APPLICATION LIST PAGE
        if session.pop('logged_in_from_login', None):
            flash('Logged in Successfully', 'success')
        email = session['email']
        print(" User Email: " + email)
        cnx = mysql.connector.connect(user='root', password='A9CALcsd7lc%7ac',
                                      host=host,
                                      database='ICSApplication')
        cursor = cnx.cursor(dictionary=True)
        sql = """SELECT first_name, middle_name, last_name, email, applicant_photo, applicant_id, application_date, id, 
        phd_registration_date, phd_registration_year, adhaar_number FROM application_page WHERE email = %s"""
        cursor.execute(sql, (email,))
        # Fetch all records matching the query
        records = cursor.fetchall()
        # Close the cursor and database connection
        sql = """SELECT year FROM signup WHERE email = %s"""
        cursor.execute(sql, (email,))
        # Fetch all records matching the query
        result = cursor.fetchall()
        cursor.close()
        cnx.close()
        # Process each record
        for record in records:
            if not record['applicant_photo']:
                session['applicant_photo'] = '/static/assets/img/default_user.png'
            else:
                session['applicant_photo'] = record['applicant_photo']
        return render_template('Candidate/commonFiles/application-list.html', records=records, result=result)