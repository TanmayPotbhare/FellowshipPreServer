import mysql.connector
from classes.connection import HostConfig, ConfigPaths
import os
from flask import Blueprint, render_template, session, request, redirect, url_for, flash
from authentication.middleware import auth

adhaarseed_blueprint = Blueprint('adhaarseed', __name__)


def adhaarseed_auth(app):
    # ------ HOST Configs are in classes/connection.py
    host = HostConfig.host
    app_paths = ConfigPaths.paths.get(host)
    if app_paths:
        for key, value in app_paths.items():
            app.config[key] = value

    @adhaarseed_blueprint.route('/old_user_adhaar_seed', methods=['GET', 'POST'])
    def old_user_adhaar_seed():
        cnx = mysql.connector.connect(user='root', password='A9CALcsd7lc%7ac',
                                      host=host,
                                      database='ICSApplication')
        cursor = cnx.cursor(dictionary=True)
        records = None
        adhaar_seeding_doc = None
        joining_date = None  # Initialize with a default value
        email = session.get('email', None)
        existing_report = []
        # Fetch the joining date from the database

        email = session['email']
        cursor.execute(
            "SELECT first_name, last_name, phd_registration_date, joining_date, adhaar_seeding, adhaar_seeding_doc, application_date FROM application_page WHERE email = %s",
            (email,))
        result = cursor.fetchone()

        if result:
            user = result['first_name']
        else:
            user = 'Admin'

        if result:
            joining_date = result['application_date']
            existing_report = result['adhaar_seeding_doc']
        if request.method == 'POST':
            first_name = result['first_name']
            last_name = result['last_name']
            existing_report = result['adhaar_seeding_doc']
            adhaar_seeding_doc = save_file_joining_report(request.files['adhaar_seeding_doc'], first_name, last_name)
            print(adhaar_seeding_doc)
            print(existing_report)

            update_query = "UPDATE application_page SET adhaar_seeding_doc=%s, joining_date=%s  WHERE email = %s"
            cursor.execute(update_query, (adhaar_seeding_doc, joining_date, email))
            cnx.commit()

        cursor.close()
        cnx.close()
        return render_template('Candidate/AcceptedUserDashboard/old_user_adhaar_seed.html', records=records,
                               joining_date=joining_date, adhaar_seeding_doc=adhaar_seeding_doc,
                               result=result, existing_report=existing_report, user=user)

    def save_file_joining_report(file, firstname, lastname):
        if file:
            filename = f"{firstname}_{lastname}_{file.filename}"
            file.save(os.path.join(app.config['JOINING_REPORT'], filename))
            # return os.path.join(app.config['RENT_AGREEMENT_REPORT'], filename)
            return '/static/uploads/joining_reports/' + filename
        else:
            return "Save File"