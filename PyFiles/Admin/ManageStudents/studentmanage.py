from datetime import date, timedelta, datetime
import mysql.connector
from classes.connection import HostConfig, ConfigPaths, ConnectParam
import os
from flask_mail import Mail, Message
from flask import Blueprint, render_template, session, request, redirect, url_for, flash
from authentication.middleware import auth

managestud_blueprint = Blueprint('managestud', __name__)


def managestud_auth(app):
    # ------ HOST Configs are in classes/connection.py
    host = HostConfig.host
    app_paths = ConfigPaths.paths.get(host)
    if app_paths:
        for key, value in app_paths.items():
            app.config[key] = value

    @managestud_blueprint.route('/student_manage_dashbaord')
    def student_manage_dashbaord():
        return render_template('Admin/ManageStudents/student_manage_dashbaord.html')

    @managestud_blueprint.route('/admin_issue_dashboard', methods=['GET', 'POST'])
    def admin_issue_dashboard():
        cnx = mysql.connector.connect(user='root', password='A9CALcsd7lc%7ac',
                                      host=host,
                                      database='ICSApplication')
        cursor = cnx.cursor(dictionary=True)
        sql = """ SELECT * FROM application_page """
        cursor.execute(sql)
        result = cursor.fetchall()
        for record in result:
            id = record['id']
        print(result)
        delete_student = delete_student_management(id)
        return render_template('Admin/ManageStudents/admin_issue_dashboard.html',
                               result=result, delete_student=delete_student)

    @managestud_blueprint.route('/delete_student_management/<int:id>')
    def delete_student_management(id):
        cnx = mysql.connector.connect(user='root', password='A9CALcsd7lc%7ac',
                                      host=host,
                                      database='ICSApplication')
        cursor = cnx.cursor(dictionary=True)
        sql = "DELETE FROM application_page WHERE id = %s"
        cursor.execute(sql, (id,))
        # Close the cursor and database connection
        cursor.close()
        cnx.close()
        return render_template('Admin/ManageStudents/deleted_student_success.html')

    @managestud_blueprint.route('/edit_student_admin_management/<int:id>', methods=['GET', 'POST'])
    def edit_student_admin_management(id):
        cnx = mysql.connector.connect(user='root', password='A9CALcsd7lc%7ac',
                                      host=host,
                                      database='ICSApplication')
        cursor = cnx.cursor(dictionary=True)
        sql = """SELECT * FROM application_page WHERE id = %s"""
        cursor.execute(sql, (id,))
        # Fetch all records matching the query
        records = cursor.fetchall()
        # Close the cursor and database connection
        cursor.close()
        cnx.close()
        return render_template('Admin/ManageStudents/edit_student_admin_management.html', records=records)

    @managestud_blueprint.route('/issue_resolve/<int:id>', methods=['GET', 'POST'])
    def issue_resolve(id):  # -------------- VIEW STUDENT FORM
        cnx = mysql.connector.connect(user='root', password='A9CALcsd7lc%7ac',
                                      host=host,
                                      database='ICSApplication')
        cursor = cnx.cursor(dictionary=True)
        sql = """SELECT * FROM application_page WHERE id = %s"""
        cursor.execute(sql, (id,))
        # Fetch all records matching the query
        records = cursor.fetchall()
        # Close the cursor and database connection
        cursor.close()
        cnx.close()
        return render_template('Admin/ManageStudents/issue_resolve.html', records=records)

    @managestud_blueprint.route('/old_user_insertion_by_admin', methods=['GET', 'POST'])
    def old_user_insertion_by_admin():
        cnx = mysql.connector.connect(user='root', password='A9CALcsd7lc%7ac',
                                      host=host,
                                      database='ICSApplication')
        cursor = cnx.cursor(dictionary=True)
        if request.method == 'POST':
            first_name = request.form['first_name']
            middle_name = request.form['middle_name']
            last_name = request.form['last_name']
            email = request.form['email']
            password = 'Fellowship123'
            confirm_password = 'Fellowship123'
            year = request.form['year']
            phd_registration_date = request.form['phd_registration_date']
            phd_registration_year = request.form['phd_registration_year']
            caste = 'Scheduled Tribes'
            fellowship_withdrawn = 'not_withdrawn'
            form_filled = '0'
            added_by = 'Admin'
            current_datetime = datetime.now()
            added_date = current_datetime.date()
            added_time = current_datetime.time()

            sql = "INSERT INTO signup (first_name, middle_name, last_name, email, password, confirm_password, year, " \
                  "fellowship_withdrawn, added_by, added_date, added_time) " \
                  "VALUES (%(first_name)s, %(middle_name)s, %(last_name)s, %(email)s, %(password)s, %(confirm_password)s," \
                  " %(year)s, %(fellowship_withdrawn)s, %(added_by)s, %(added_date)s, %(added_time)s)"
            signup_data = {
                "first_name": first_name,
                "middle_name": middle_name,
                "last_name": last_name,
                "email": email,
                "password": password,
                "confirm_password": confirm_password,
                "year": year,
                "fellowship_withdrawn": fellowship_withdrawn,
                "added_by": added_by,
                "added_date": added_date,
                "added_time": added_time
            }
            cursor.execute(sql, signup_data)

            sql = "INSERT INTO old_users (form_filled, first_name, middle_name, last_name, email, phd_registration_date, " \
                  "phd_registration_year, caste) " \
                  "VALUES (%(form_filled)s, %(first_name)s, %(middle_name)s, %(last_name)s, %(email)s, " \
                  "%(phd_registration_date)s, %(phd_registration_year)s, %(caste)s)"

            olduser_data = {
                "form_filled": form_filled,
                "first_name": first_name,
                "middle_name": middle_name,
                "last_name": last_name,
                "email": email,
                "phd_registration_date": phd_registration_date,
                "phd_registration_year": phd_registration_year,
                "caste": caste
            }
            cursor.execute(sql, olduser_data)

            cnx.commit()

            cursor.close()
            cnx.close()
            return redirect(url_for('managestud.old_user_added_by_admin'))
        return render_template('Admin/ManageStudents/old_user_insertion_by_admin.html')

    @managestud_blueprint.route('/old_user_added_by_admin', methods=['GET', 'POST'])
    def old_user_added_by_admin():
        cnx = mysql.connector.connect(user='root', password='A9CALcsd7lc%7ac',
                                      host=host,
                                      database='ICSApplication')
        cursor = cnx.cursor(dictionary=True)
        current_date = datetime.now().date()
        sql = """SELECT * FROM signup WHERE added_date = %s"""
        cursor.execute(sql, (current_date,))
        record = cursor.fetchall()
        cnx.commit()
        return render_template('Admin/ManageStudents/old_user_added_by_admin.html', record=record)