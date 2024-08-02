from datetime import date, datetime, timedelta
import mysql.connector
from classes.connection import HostConfig, ConfigPaths
import os
from fpdf import FPDF
from flask import Blueprint, render_template, session, request, redirect, url_for, flash, Response
from authentication.middleware import auth

presenty_blueprint = Blueprint('presenty', __name__)


def presenty_auth(app):
    # ------ HOST Configs are in classes/connection.py
    host = HostConfig.host
    app_paths = ConfigPaths.paths.get(host)
    if app_paths:
        for key, value in app_paths.items():
            app.config[key] = value

    @presenty_blueprint.route('/presenty_AA', methods=['GET', 'POST'])
    def presenty_AA():
        if 'email' not in session:
            return redirect('/login')

        email = session['email']
        cnx = mysql.connector.connect(user='root', password='A9CALcsd7lc%7ac', host=host, database='ICSApplication')
        cursor = cnx.cursor(dictionary=True)
        existing_reports = []  # Initialize existing_reports here

        cursor.execute("SELECT first_name, last_name FROM application_page WHERE email = %s", (email,))
        result = cursor.fetchone()

        if request.method == 'POST':
            # Handle file uploads and save them to the database
            for i in range(1, 61):  # Assuming up to 60 months (5 years) of reports
                report = request.files.get(f'monthly_report{i}')
                if report:
                    first_name = result['first_name']
                    last_name = result['last_name']
                    # Save the uploaded report to a directory
                    report_path = save_file_presenty_report(report, first_name, last_name)
                    # Update the database with the report path
                    cursor.execute(f"UPDATE award_letter SET monthly_report{i} = %s WHERE email = %s",
                                   (report_path, email))
            cnx.commit()

        # Fetch the saved reports for the user
        cursor.execute(
            f"SELECT monthly_report1, monthly_report2, monthly_report3, monthly_report4, monthly_report5, "
            f"monthly_report6, monthly_report7, monthly_report8, monthly_report9, monthly_report10, "
            f"monthly_report11, monthly_report12, monthly_report13, monthly_report14, monthly_report15, "
            f"monthly_report16, monthly_report17, monthly_report18, monthly_report19, monthly_report20, "
            f"monthly_report21, monthly_report22, monthly_report23, monthly_report24, monthly_report25, "
            f"monthly_report26, monthly_report27, monthly_report28, monthly_report29, monthly_report30, "
            f"monthly_report31, monthly_report32, monthly_report33, monthly_report34, monthly_report35, "
            f"monthly_report36, monthly_report37, monthly_report38, monthly_report39, monthly_report40, "
            f"monthly_report41, monthly_report42, monthly_report43, monthly_report44, monthly_report45, "
            f"monthly_report46, monthly_report47, monthly_report48, monthly_report49, monthly_report50, "
            f"monthly_report51, monthly_report52, monthly_report53, monthly_report54, monthly_report55, "
            f"monthly_report56, monthly_report57, monthly_report58, monthly_report59, monthly_report60 "
            f"FROM award_letter WHERE email = %s",
            (email,))
        reports = cursor.fetchone()
        # Count the number of submitted reports
        # Calculate the submitted count and get the list of submitted documents
        submitted_count = 0
        submitted_documents = []

        for i in range(1, 61):
            if reports[f'monthly_report{i}']:
                submitted_count += 1
                submitted_documents.append(f'monthly_report{i}')
        index = 1
        # Now you have the submitted count and the list of submitted documents
        print("Submitted Count:", submitted_count)
        print("Submitted Documents:", submitted_documents)
        # Fetch the joining date for the user
        cursor.execute("SELECT phd_registration_date FROM application_page WHERE email = %s", (email,))
        result = cursor.fetchone()

        i = submitted_count + 1

        # Use parameterized placeholders for the column names
        query = f"SELECT submission_date_report{i}, submission_day_report{i} FROM award_letter WHERE email = %s"
        cursor.execute(query, (email,))
        record = cursor.fetchone()

        if result:
            joining_date = result['phd_registration_date']
            print(joining_date)
            start_dates = [datetime.combine(joining_date, datetime.min.time()) + timedelta(days=i * 30) for i in
                           range(60)]
            end_dates = [start_date + timedelta(days=30) for start_date in start_dates]

            if record:
                # Use existing submission date and day
                submitted_date = record[f'submission_date_report{i}']
                submitted_day = record[f'submission_day_report{i}']
            else:
                # Generate new submission date and day
                current_datetime = datetime.now()
                submitted_date = current_datetime.strftime('%Y-%m-%d')
                submitted_day = current_datetime.strftime('%A')  # Full weekday name (e.g., Monday)
        else:
            joining_date = None
            submitted_date = None
            submitted_day = None
            start_dates = []
            end_dates = []

        # Update the database
        update_query = f"""
            UPDATE award_letter
            SET submission_date_report{i} = %s,
                submission_day_report{i} = %s
            WHERE email = %s
        """
        cursor.execute(update_query, (submitted_date, submitted_day, email))
        cnx.commit()
        # Zip the start_dates and end_dates
        zipped_dates = list(zip(start_dates, end_dates))

        return render_template('Candidate/AcceptedUserDashboard/presenty_AA.html', zipped_dates=zipped_dates,
                               reports=reports, start_dates=start_dates, end_dates=end_dates, joining_date=joining_date,
                               submitted_count=submitted_count, submitted_date=submitted_date,
                               submitted_day=submitted_day,
                               submitted_documents=submitted_documents, index=index)

    def save_file_presenty_report(file, firstname, lastname):
        if file:
            filename = f"{firstname}_{lastname}_{file.filename}"
            file.save(os.path.join(app.config['PRESENTY_REPORTS'], filename))
            # return os.path.join(app.config['PRESENTY_REPORTS'], filename)
            return '/static/uploads/presenty_reports/' + filename
        else:
            return "Save File"