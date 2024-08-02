from datetime import date, timedelta, datetime
import mysql.connector
from classes.connection import HostConfig, ConfigPaths, ConnectParam
import os
from flask_mail import Mail, Message
from flask import Blueprint, render_template, session, request, redirect, url_for, flash
from authentication.middleware import auth

issue_raisedAdmin_blueprint = Blueprint('issue_raisedAdmin', __name__)


def issue_raisedAdmin_auth(app):
    # ------ HOST Configs are in classes/connection.py
    host = HostConfig.host
    app_paths = ConfigPaths.paths.get(host)
    if app_paths:
        for key, value in app_paths.items():
            app.config[key] = value

    @issue_raisedAdmin_blueprint.route('/admin_issue_raised_by_students', methods=['GET'])
    def admin_issue_raised_by_students():
        cnx = mysql.connector.connect(user='root', password='A9CALcsd7lc%7ac',
                                      host=host,
                                      database='ICSApplication')
        cursor = cnx.cursor(dictionary=True)
        sql = """SELECT * FROM issue_raised """
        cursor.execute(sql)
        # Fetch all records matching the query
        records = cursor.fetchall()
        print(records)
        # Close the cursor and database connection
        cursor.close()
        cnx.close()
        return render_template('Admin/admin_issue_raised_by_students.html', records=records)