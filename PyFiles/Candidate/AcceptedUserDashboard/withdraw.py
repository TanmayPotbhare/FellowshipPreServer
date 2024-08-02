from datetime import date, datetime, timedelta
import mysql.connector
from classes.connection import HostConfig, ConfigPaths
import os
from fpdf import FPDF
from flask import Blueprint, render_template, session, request, redirect, url_for, flash, Response
from authentication.middleware import auth

withdraw_blueprint = Blueprint('withdraw', __name__)


def withdraw_auth(app):
    # ------ HOST Configs are in classes/connection.py
    host = HostConfig.host
    app_paths = ConfigPaths.paths.get(host)
    if app_paths:
        for key, value in app_paths.items():
            app.config[key] = value

    @withdraw_blueprint.route('/with_from_fellowship_AA', methods=['GET', 'POST'])
    def with_from_fellowship_AA():
        email = session.get('email')
        if email is None:
            # Handle the case where the user is not logged in
            return redirect('/login')

        cnx = mysql.connector.connect(user='root', password='A9CALcsd7lc%7ac',
                                      host=host,
                                      database='ICSApplication')
        cursor = cnx.cursor(dictionary=True)

        if request.method == 'POST':
            # Handle the form submission
            update_query = "UPDATE signup SET request_withdrawal = %s, withdrawal_request_date = %s WHERE email = %s"
            withdrawal_request_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute(update_query, (True, withdrawal_request_date, email))
            cnx.commit()

        # Fetch the relevant information
        select_query = "SELECT request_withdrawal, withdrawal_request_date FROM signup WHERE email = %s"
        cursor.execute(select_query, (email,))
        result = cursor.fetchone()

        cursor.close()
        cnx.close()
        return render_template('Candidate/AcceptedUserDashboard/with_from_fellowship_AA.html', result=result)