from datetime import date
import mysql.connector
from classes.connection import HostConfig, ConfigPaths
import os
from fpdf import FPDF
from flask import Blueprint, render_template, session, request, redirect, url_for, flash, Response
from authentication.middleware import auth

undertakingdoc_blueprint = Blueprint('undertakingdoc', __name__)


def undertakingdoc_auth(app):
    # ------ HOST Configs are in classes/connection.py
    host = HostConfig.host
    app_paths = ConfigPaths.paths.get(host)
    if app_paths:
        for key, value in app_paths.items():
            app.config[key] = value

    @undertakingdoc_blueprint.route('/undertakingDoc', methods=['GET', 'POST'])
    def undertakingDoc():
        """
            This function helps in Uploading the Undertaking Document
            from the user and if the document is already uploaded the
            user can view the document.
        """
        cnx = mysql.connector.connect(user='root', password='A9CALcsd7lc%7ac',
                                      host=host,
                                      database='ICSApplication')
        cursor = cnx.cursor(dictionary=True)
        records = None
        undertaking_doc = None
        undertaking_doc_date = None  # Initialize with a default value
        email = session.get('email', None)
        existing_report = []

        # Fetch the joining date from the database
        email = session['email']
        cursor.execute(
            "SELECT first_name, last_name, phd_registration_date, undertaking_doc_date, undertaking_doc FROM application_page WHERE email = %s",
            (email,))
        result = cursor.fetchone()

        if result:
            user = result['first_name']
        else:
            user = 'Admin'

        if result:
            undertaking_doc_date = result['undertaking_doc_date']
            existing_report = result['undertaking_doc']
        if request.method == 'POST':
            first_name = result['first_name']
            last_name = result['last_name']
            existing_report = result['undertaking_doc']
            undertaking_doc = save_file_undertaking_report(request.files['undertaking_doc'], first_name, last_name)
            undertaking_doc_date = date.today()
            print('undertaking_doc', undertaking_doc)
            print(existing_report)

            update_query = "UPDATE application_page SET undertaking_doc=%s, undertaking_doc_date=%s WHERE email = %s"
            cursor.execute(update_query, (undertaking_doc, undertaking_doc_date, email))
            cnx.commit()
            flash('Undertaking Document Report Uploaded Successfully', 'success')

        cursor.execute(
            "SELECT undertaking_doc FROM application_page WHERE email = %s",
            (email,))
        output = cursor.fetchone()
        doc = output['undertaking_doc']
        print(doc)
        cursor.close()
        cnx.close()
        return render_template('Candidate/AcceptedUserDashboard/undertakingDoc.html', records=records,
                               undertaking_doc_date=undertaking_doc_date, undertaking_doc=undertaking_doc,
                               esult=result, existing_report=existing_report, doc=doc, user=user)
    # --------------------  Function End ----------------------------

    def save_file_undertaking_report(file, firstname, lastname):
        if file:
            filename = f"{firstname}_{lastname}_{file.filename}"
            file.save(os.path.join(app.config['UNDERTAKING_REPORT'], filename))
            # return os.path.join(app.config['RENT_AGREEMENT_REPORT'], filename)
            return '/static/uploads/undertaking_report/' + filename
        else:
            return "Save File"