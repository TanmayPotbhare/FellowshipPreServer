import mysql.connector
from classes.connection import HostConfig, ConfigPaths
import os
from fpdf import FPDF
from flask import Blueprint, render_template, session, request, redirect, url_for, flash, Response
from authentication.middleware import auth

joiningreport_blueprint = Blueprint('joiningreport', __name__)


def joiningreport_auth(app):
    # ------ HOST Configs are in classes/connection.py
    host = HostConfig.host
    app_paths = ConfigPaths.paths.get(host)
    if app_paths:
        for key, value in app_paths.items():
            app.config[key] = value

    @joiningreport_blueprint.route('/joining_report_AA', methods=['GET', 'POST'])
    def joining_report_AA():
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
            "SELECT first_name, last_name, phd_registration_date, joining_date, joining_report FROM application_page WHERE email = %s",
            (email,))
        result = cursor.fetchone()
        print(result)
        if result:
            joining_date = result['phd_registration_date']
            existing_report = result['joining_report']
        if request.method == 'POST':
            first_name = result['first_name']
            last_name = result['last_name']
            existing_report = result['joining_report']
            joining_report = save_file_joining_report(request.files['joining_report'], first_name, last_name)
            print(joining_report)
            print(existing_report)

            update_query = "UPDATE application_page SET joining_report=%s, joining_date=%s  WHERE email = %s"
            cursor.execute(update_query, (joining_report, joining_date, email))
            cnx.commit()
            flash('Joining Report Uploaded Successfully', 'success')
        cursor.close()
        cnx.close()

        return render_template('Candidate/AcceptedUserDashboard/joining_report_AA.html', records=records, joining_date=joining_date,
                               joining_report=joining_report,
                               result=result, existing_report=existing_report)

    def save_file_joining_report(file, firstname, lastname):
        if file:
            filename = f"{firstname}_{lastname}_{file.filename}"
            file.save(os.path.join(app.config['JOINING_REPORT'], filename))
            # return os.path.join(app.config['RENT_AGREEMENT_REPORT'], filename)
            return '/static/uploads/joining_reports/' + filename
        else:
            return "Save File"