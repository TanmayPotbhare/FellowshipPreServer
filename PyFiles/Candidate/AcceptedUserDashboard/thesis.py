from datetime import date, datetime, timedelta
import mysql.connector
from classes.connection import HostConfig, ConfigPaths
import os
from fpdf import FPDF
from flask import Blueprint, render_template, session, request, redirect, url_for, flash, Response
from authentication.middleware import auth

thesis_blueprint = Blueprint('thesis', __name__)


def thesis_auth(app):
    # ------ HOST Configs are in classes/connection.py
    host = HostConfig.host
    app_paths = ConfigPaths.paths.get(host)
    if app_paths:
        for key, value in app_paths.items():
            app.config[key] = value

    @thesis_blueprint.route('/upload_thesis_AA', methods=['GET', 'POST'])
    def upload_thesis_AA():
        if 'email' not in session:
            return redirect(url_for('login_signup.login'))  # Redirect to login if user not logged in
        email = session['email']
        # Establish database connection
        cnx = mysql.connector.connect(user='root', password='A9CALcsd7lc%7ac',
                                      host=host,
                                      database='ICSApplication')
        cursor = cnx.cursor(dictionary=True)
        cursor.execute("SELECT first_name, last_name FROM application_page WHERE email = %s", (email,))
        result = cursor.fetchone()

        if request.method == 'POST':
            if 'phd_thesis' in request.files:
                file = request.files['phd_thesis']
                if file.filename != '':
                    file_paths = []  # Create an empty list to store tuples

                    first_name = result['first_name']
                    last_name = result['last_name']

                    # Save the uploaded report to a directory and get the file path
                    file_path = save_file_uplaod_thesis(file, first_name, last_name)

                    # Append a tuple to the list
                    file_paths.append((f'phd_award', file_path))

                    # Get user's email from session
                    email = session['email']

                    cursor = cnx.cursor()
                    update_query = "UPDATE application_page SET phd_thesis = %s WHERE email = %s"
                    cursor.execute(update_query, (file_path, email))

                    cnx.commit()
                    cursor.close()
                    return redirect(url_for('thesis.upload_thesis_AA'))

        email = session['email']
        cursor = cnx.cursor()
        cursor.execute("SELECT phd_thesis FROM application_page WHERE email = %s", (email,))
        result = cursor.fetchone()

        if result is not None:
            phd_thesis = result[0]
        else:
            phd_thesis = None

        cnx.close()
        return render_template('Candidate/AcceptedUserDashboard/upload_thesis_AA.html', phd_thesis=phd_thesis)

    def save_file_uplaod_thesis(file, firstname, lastname):
        if file:
            filename = f"{firstname}_{lastname}_{file.filename}"
            file.save(os.path.join(app.config['UPLOAD_THESIS'], filename))
            # return os.path.join(app.config['HALF_YEARLY_REPORTS'], filename)
            return '/static/uploads/upload_thesis/' + filename
        else:
            return "Save File"