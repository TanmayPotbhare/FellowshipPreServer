from datetime import date, datetime, timedelta
import mysql.connector
from classes.connection import HostConfig, ConfigPaths
import os
from fpdf import FPDF
from flask import Blueprint, render_template, session, request, redirect, url_for, flash, Response
from authentication.middleware import auth

hracert_blueprint = Blueprint('hracert', __name__)


def hracert_auth(app):
    # ------ HOST Configs are in classes/connection.py
    host = HostConfig.host
    app_paths = ConfigPaths.paths.get(host)
    if app_paths:
        for key, value in app_paths.items():
            app.config[key] = value

    @hracert_blueprint.route('/rent_agreement_AA', methods=['GET', 'POST'])
    def rent_agreement_AA():
        if 'email' not in session:
            # Redirect to the login page if the user is not logged in
            return redirect('/login')

        email = session['email']
        cnx = mysql.connector.connect(user='root', password='A9CALcsd7lc%7ac',
                                      host=host,
                                      database='ICSApplication')
        cursor = cnx.cursor(dictionary=True)
        existing_reports = []  # Initialize existing_reports here
        submitted_documents = []
        cursor.execute("SELECT first_name, last_name FROM application_page WHERE email = %s", (email,))
        result = cursor.fetchone()

        if request.method == 'POST':
            # Handle file uploads and save them to the database
            report_paths = []
            for i in range(1, 6):
                report = request.files.get(f'rent_agreement{i}')
                if report:
                    first_name = result['first_name']
                    last_name = result['last_name']
                    # Save the uploaded report to a directory
                    # You can use your own logic to save the report and get the file path
                    report_path = save_file_rent_agreement(report, first_name, last_name)
                    report_paths.append(
                        (f'rent_agreement{i}', report_path))  # Store the field name along with the file path

            # Update the database with the report paths
            for report_field, report_path in report_paths:
                cursor.execute(f"UPDATE application_page SET {report_field} = %s WHERE email = %s",
                               (report_path, email))
            cnx.commit()

        # Fetch the saved reports for the user
        cursor.execute(
            f"SELECT rent_agreement1, rent_agreement2, rent_agreement3, rent_agreement4, rent_agreement5 FROM application_page WHERE email = %s",
            (email,))
        reports = cursor.fetchone()
        # Count the number of submitted reports
        submitted_count = sum([1 for i in range(1, 6) if reports[f'rent_agreement{i}']])
        for i in range(1, 11):
            if reports.get(f'rent_agreement{i}'):
                submitted_documents.append(f'rent_agreement{i}')
        # Fetch the joining date for the user
        cursor.execute("SELECT phd_registration_date FROM application_page WHERE email = %s", (email,))
        result = cursor.fetchone()

        if result:
            joining_date = result['phd_registration_date']
            start_dates = [joining_date + timedelta(days=i * 365) for i in range(5)]
            end_dates = [start_date + timedelta(days=365) for start_date in start_dates]
        else:
            joining_date = None
            start_dates = []
            end_dates = []

        cursor.close()
        cnx.close()

        return render_template('Candidate/AcceptedUserDashboard/rent_agreement_AA.html', reports=reports, joining_date=joining_date,
                               start_dates=start_dates, end_dates=end_dates, submitted_count=submitted_count,
                               submitted_documents=submitted_documents)

    def save_file_rent_agreement(file, firstname, lastname):
        if file:
            filename = f"{firstname}_{lastname}_{file.filename}"
            file.save(os.path.join(app.config['RENT_AGREEMENT_REPORT'], filename))
            # return os.path.join(app.config['RENT_AGREEMENT_REPORT'], filename)
            return '/static/uploads/rent_agreement/' + filename
        else:
            return "Save File"
