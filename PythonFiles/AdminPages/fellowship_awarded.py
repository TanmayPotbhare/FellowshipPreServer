from datetime import date, timedelta, datetime
import mysql.connector
from Classes.database import HostConfig, ConfigPaths, ConnectParam
import os
from flask_mail import Mail, Message
from flask import Blueprint, render_template, session, request, redirect, url_for, flash
from Authentication.middleware import auth

fellowship_awarded_blueprint = Blueprint('fellowship_awarded', __name__)


def fellowship_awarded_auth(app):
    # ------ HOST Configs are in classes/connection.py
    host = HostConfig.host
    app_paths = ConfigPaths.paths.get(host)
    if app_paths:
        for key, value in app_paths.items():
            app.config[key] = value

    @fellowship_awarded_blueprint.route('/fellowship_awarded', methods=['GET', 'POST'])
    def fellowship_awarded():
        if not session.get('logged_in'):
            # Redirect to the admin login page if the user is not logged in
            return redirect(url_for('adminlogin.admin_login'))

        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)

        sql = """ 

                    SELECT * 
                    FROM application_page 
                    WHERE final_approval = 'accepted' 
                      AND phd_registration_year >= '2023'

                    UNION

                    SELECT * 
                    FROM application_page 
                    WHERE phd_registration_year > '2020' 
                      AND aadesh = 1; 

            """
        cursor.execute(sql)
        result = cursor.fetchall()
        # print(result)
        cursor.close()
        cnx.close()
        return render_template('AdminPages/fellowship_awarded.html', result=result)