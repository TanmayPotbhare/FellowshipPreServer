from datetime import date, datetime, timedelta
import mysql.connector
from classes.connection import HostConfig, ConfigPaths
import os
from fpdf import FPDF
from flask import Blueprint, render_template, session, request, redirect, url_for, flash, Response
from authentication.middleware import auth

halfyearly_blueprint = Blueprint('halfyearly', __name__)


def halfyearly_auth(app):
    # ------ HOST Configs are in classes/connection.py
    host = HostConfig.host
    app_paths = ConfigPaths.paths.get(host)
    if app_paths:
        for key, value in app_paths.items():
            app.config[key] = value

    @halfyearly_blueprint.route('/half_yearly_rep_AA', methods=['GET', 'POST'])
    def half_yearly_rep_AA():
        if 'email' not in session:
            return redirect('/login')

        email = session['email']
        cnx = mysql.connector.connect(user='root', password='A9CALcsd7lc%7ac', host=host, database='ICSApplication')
        cursor = cnx.cursor(dictionary=True)
        existing_reports = []  # Initialize existing_reports here
        submitted_documents = []
        cursor.execute("SELECT first_name, last_name FROM application_page WHERE email = %s", (email,))
        result = cursor.fetchone()

        if request.method == 'POST':
            # Handle file uploads and save them to the database
            report_paths = []
            for i in range(1, 11):
                report = request.files.get(f'half_yearly_report{i}')
                if report:
                    first_name = result['first_name']
                    last_name = result['last_name']
                    # Save the uploaded report to a directory
                    # You can use your own logic to save the report and get the file path
                    report_path = save_file_half_yearly(report, first_name, last_name)
                    report_paths.append((f'half_yearly_report{i}', report_path))

            # Update the database with the report paths
            for report_field, report_path in report_paths:
                cursor.execute(f"UPDATE application_page SET {report_field} = %s WHERE email = %s",
                               (report_path, email))
            cnx.commit()

        # Fetch the saved reports for the user
        cursor.execute(
            f"SELECT half_yearly_report1, half_yearly_report2, half_yearly_report3, half_yearly_report4, half_yearly_report5, "
            f"half_yearly_report6, half_yearly_report7, half_yearly_report8, half_yearly_report9, half_yearly_report10 "
            f"FROM application_page WHERE email = %s",
            (email,))
        reports = cursor.fetchone()
        print(reports)
        # Count the number of submitted reports

        submitted_count = sum([1 for i in range(1, 11) if reports[f'half_yearly_report{i}']])
        for i in range(1, 11):
            if reports.get(f'half_yearly_report{i}'):
                submitted_documents.append(f'half_yearly_report{i}')

        # Fetch the joining date for the user
        cursor.execute("SELECT phd_registration_date FROM application_page WHERE email = %s", (email,))
        result = cursor.fetchone()

        if result:
            joining_date = result['phd_registration_date']
            start_dates = [joining_date + timedelta(days=i * 30 * 6) for i in range(10)]
            end_dates = [start_date + timedelta(days=30 * 6) for start_date in start_dates]
        else:
            joining_date = None
            start_dates = []
            end_dates = []

        cursor.close()
        cnx.close()
        return render_template('Candidate/AcceptedUserDashboard/half_yearly_rep_AA.html', reports=reports, joining_date=joining_date,
                               start_dates=start_dates, end_dates=end_dates, submitted_count=submitted_count,
                               submitted_documents=submitted_documents)

    def save_file_half_yearly(file, firstname, lastname):
        if file:
            filename = f"{firstname}_{lastname}_{file.filename}"
            file.save(os.path.join(app.config['HALF_YEARLY_REPORTS'], filename))
            # return os.path.join(app.config['HALF_YEARLY_REPORTS'], filename)
            return '/static/uploads/half_yearly/' + filename
        else:
            return "Save File"