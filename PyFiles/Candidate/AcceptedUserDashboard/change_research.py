from datetime import date, datetime, timedelta
import mysql.connector
from classes.connection import HostConfig, ConfigPaths
import os
from fpdf import FPDF
from flask import Blueprint, render_template, session, request, redirect, url_for, flash, Response
from authentication.middleware import auth

changeres_blueprint = Blueprint('changeres', __name__)


def changeres_auth(app):
    # ------ HOST Configs are in classes/connection.py
    host = HostConfig.host
    app_paths = ConfigPaths.paths.get(host)
    if app_paths:
        for key, value in app_paths.items():
            app.config[key] = value

    @changeres_blueprint.route('/change_center_AA', methods=['GET', 'POST'])
    def change_center_AA():
        if 'email' not in session:
            # Redirect to the login page if the user is not logged in
            return redirect(url_for('login_signup.login'))

            # Update the database to change the name of the center
        cnx = mysql.connector.connect(user='root', password='A9CALcsd7lc%7ac',
                                      host=host,
                                      database='ICSApplication')

        if request.method == 'POST':
            # Get the user's email from the session
            email = session['email']
            new_center_name = request.form.get('new_center_name')
            cursor = cnx.cursor()
            update_query = "UPDATE application_page SET name_of_college = %s WHERE email = %s"
            cursor.execute(update_query, (new_center_name, email))

            # Commit the transaction and close the cursor and connection
            cnx.commit()
            cursor.close()
            return redirect(url_for('changeres.change_center_AA'))
        cursor = cnx.cursor()

        # SQL query to fetch the present center name from database
        email = session['email']
        cursor.execute("SELECT name_of_college FROM application_page WHERE email = %s", (email,))
        result = cursor.fetchone()

        if result is not None:
            center_name = result[0]
        else:
            center_name = "No Center Found"

        # cursor.close()
        cnx.close()
        return render_template('Candidate/AcceptedUserDashboard/change_center_AA.html', center_name=center_name)