import mysql.connector
from classes.connection import HostConfig, ConfigPaths
import os
from fpdf import FPDF
from flask import Blueprint, render_template, session, request, redirect, url_for, flash, Response
from authentication.middleware import auth

phdaward_blueprint = Blueprint('phdaward', __name__)


def phdaward_auth(app):
    # ------ HOST Configs are in classes/connection.py
    host = HostConfig.host
    app_paths = ConfigPaths.paths.get(host)
    if app_paths:
        for key, value in app_paths.items():
            app.config[key] = value

    @phdaward_blueprint.route('/phd_award_AA', methods=['GET', 'POST'])
    def phd_award_AA():
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
            if 'phd_award' in request.files:
                file = request.files['phd_award']
                if file.filename != '':
                    file_paths = []  # Create an empty list to store tuples

                    first_name = result['first_name']
                    last_name = result['last_name']

                    # Save the uploaded report to a directory and get the file path
                    file_path = save_file_pdf_cert(file, first_name, last_name)

                    # Append a tuple to the list
                    file_paths.append((f'phd_award', file_path))

                    # Get user's email from session
                    email = session['email']

                    cursor = cnx.cursor()
                    update_query = "UPDATE application_page SET phd_award = %s WHERE email = %s"
                    cursor.execute(update_query, (file_path, email))

                    cnx.commit()
                    cursor.close()
                    return redirect(url_for('phdaward.phd_award_AA'))

        email = session['email']
        cursor = cnx.cursor()
        cursor.execute("SELECT phd_award FROM application_page WHERE email = %s", (email,))
        result = cursor.fetchone()

        if result is not None:
            phd_award = result[0]
        else:
            phd_award = None

        cnx.close()
        return render_template('Candidate/AcceptedUserDashboard/phd_award_AA.html', phd_award=phd_award)

    def save_file_pdf_cert(file, firstname, lastname):
        if file:
            filename = f"{firstname}_{lastname}_{file.filename}"
            file.save(os.path.join(app.config['PDF_CERTIFICATE'], filename))
            # return os.path.join(app.config['RENT_AGREEMENT_REPORT'], filename)
            return '/static/uploads/phd_certificate/' + filename
        else:
            return "Save File"