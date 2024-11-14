from datetime import date, datetime, timedelta
import mysql.connector
from classes.connection import HostConfig, ConfigPaths
import os
from fpdf import FPDF
from flask import Blueprint, render_template, session, request, redirect, url_for, flash, Response
from authentication.middleware import auth

assessment_blueprint = Blueprint('assessment', __name__)


def assessment_auth(app):
    # ------ HOST Configs are in classes/connection.py
    host = HostConfig.host
    app_paths = ConfigPaths.paths.get(host)
    if app_paths:
        for key, value in app_paths.items():
            app.config[key] = value

    @assessment_blueprint.route('/assessment_report_AA', methods=['GET', 'POST'])
    def assessment_report_AA():
        cnx = mysql.connector.connect(user='root', password='A9CALcsd7lc%7ac',
                                      host=host,
                                      database='ICSApplication')
        cursor = cnx.cursor(dictionary=True)
        records = None
        joining_report = None
        joining_date = None  # Initialize with a default value
        email = session.get('email', None)
        existing_report = []
        # Fetch the joining date from the database

        email = session['email']
        cursor.execute(
            "SELECT first_name, last_name, phd_registration_date, assessment_report FROM application_page WHERE email = %s",
            (email,))
        result = cursor.fetchone()
        if result:
            user = result['first_name']
        else:
            user = 'Admin'

        if result:
            joining_date = result['phd_registration_date']
            existing_report = result['assessment_report']
            print("existing_report", existing_report)
        if request.method == 'POST':
            print('Inside POST request')
            first_name = result['first_name']
            last_name = result['last_name']
            existing_report = result['assessment_report']
            joining_report = save_file_assessment_report(request.files['assessment_report'], first_name, last_name)
            print(joining_report)
            print(existing_report)

            update_query = "UPDATE application_page SET assessment_report=%s WHERE email = %s"
            cursor.execute(update_query, (joining_report, email))
            cnx.commit()

        cursor.close()
        cnx.close()
        return render_template('Candidate/AcceptedUserDashboard/assessment_report_AA.html', records=records, joining_date=joining_date,
                               joining_report=joining_report, user=user,
                               result=result, existing_report=existing_report)

    def save_file_assessment_report(file, firstname, lastname):
        if file:
            filename = f"{firstname}_{lastname}_{file.filename}"
            file.save(os.path.join(app.config['ASSESSMENT_REPORT'], filename))
            # return os.path.join(app.config['RENT_AGREEMENT_REPORT'], filename)
            return '/static/uploads/assessment_report/' + filename
        else:
            return "Save File"