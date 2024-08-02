from datetime import date, datetime, timedelta
import mysql.connector
from classes.connection import HostConfig, ConfigPaths
import os
from fpdf import FPDF
from flask import Blueprint, render_template, session, request, redirect, url_for, flash, Response
from authentication.middleware import auth

changeguide_blueprint = Blueprint('changeguide', __name__)


def changeguide_auth(app):
    # ------ HOST Configs are in classes/connection.py
    host = HostConfig.host
    app_paths = ConfigPaths.paths.get(host)
    if app_paths:
        for key, value in app_paths.items():
            app.config[key] = value

    @changeguide_blueprint.route('/change_guide_AA', methods=['GET', 'POST'])
    def change_guide_AA():
        if 'email' not in session:
            # Redirect to the login page if the user is not logged in
            return redirect(url_for('login_signup.login'))

            # Update the database to change the name of the guide
        cnx = mysql.connector.connect(user='root', password='A9CALcsd7lc%7ac',
                                      host=host,
                                      database='ICSApplication')

        if request.method == 'POST':
            # Get the user's email from the session
            email = session['email']

            new_guide_name = request.form.get('new_guide_name')
            cursor = cnx.cursor()

            # Execute an SQL query to update the giude's name
            update_query = "UPDATE application_page SET name_of_guide = %s WHERE email = %s"
            cursor.execute(update_query, (new_guide_name, email))

            # Commit the transaction and close the cursor and connection
            cnx.commit()
            cursor.close()
            return redirect(url_for('changeguide.change_guide_AA'))

        cursor = cnx.cursor()

        # SQL query to fetch the present guide name from database
        # cursor.execute("SELECT name_of_guide FROM application_page")
        email = session['email']
        cursor.execute("SELECT name_of_guide FROM application_page WHERE email = %s", (email,))
        result = cursor.fetchone()

        if result is not None:
            guide_name = result[0]
        else:
            guide_name = "No Guide Found"

        # cursor.close()
        cnx.close()

        return render_template('Candidate/AcceptedUserDashboard/change_guide_AA.html', guide_name=guide_name)
