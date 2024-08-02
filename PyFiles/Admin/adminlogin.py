import mysql.connector
from classes.connection import HostConfig, ConfigPaths
import os
from flask import Blueprint, render_template, session, request, redirect, url_for, flash
from authentication.middleware import auth

adminlogin_blueprint = Blueprint('adminlogin', __name__)


def adminlogin_auth(app):
    # ------ HOST Configs are in classes/connection.py
    host = HostConfig.host
    app_paths = ConfigPaths.paths.get(host)
    if app_paths:
        for key, value in app_paths.items():
            app.config[key] = value

    @adminlogin_blueprint.route('/adminlogin', methods=['GET', 'POST'])
    def admin_login():  # ------------------ ADMIN LOGIN
        cnx = mysql.connector.connect(user='root', password='A9CALcsd7lc%7ac',
                                      host=host,
                                      database='ICSApplication')
        cursor = cnx.cursor(dictionary=True)

        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            # Validate that both username and password are provided
            if not username or not password:
                flash('Please enter username and password.', 'error')
                cursor.close()
                cnx.close()
                return redirect(url_for('adminlogin.admin_login'))

            # Check if the user is an admin
            sql = "SELECT * FROM admin WHERE username=%s AND password=%s"
            cursor.execute(sql, (username, password))
            user = cursor.fetchone()
            print(user)
            cnx.commit()

            if not user:
                flash('Please enter valid username and password.', 'error')
                cursor.close()
                cnx.close()
                return redirect(url_for('adminlogin.admin_login'))

            session['user'] = user['username']

            if user:
                # Set session variable to indicate user is logged in
                session['logged_in'] = True
                # Close the connection and cursor
                cursor.close()
                cnx.close()
                return redirect(url_for('index.index'))
            else:
                error = 'Invalid username or password'
                # Close the connection and cursor
                cursor.close()
                cnx.close()
                flash('Please enter Valid Details to Login', 'error')
                return render_template('Admin/adminlogin.html', error=error)
        return render_template('Admin/adminlogin.html')
