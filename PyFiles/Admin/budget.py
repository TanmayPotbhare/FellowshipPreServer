from datetime import date, timedelta
import mysql.connector
from classes.connection import HostConfig, ConfigPaths, ConnectParam
import os
from flask_mail import Mail, Message
from flask import Blueprint, render_template, session, request, redirect, url_for, flash
from authentication.middleware import auth

budget_blueprint = Blueprint('budget', __name__)


def budget_auth(app):
    # ------ HOST Configs are in classes/connection.py
    host = HostConfig.host
    app_paths = ConfigPaths.paths.get(host)
    if app_paths:
        for key, value in app_paths.items():
            app.config[key] = value

    @budget_blueprint.route('/budget', methods=['GET', 'POST'])
    def budget():
        if not session.get('logged_in'):
            # Redirect to the admin login page if the user is not logged in
            return redirect(url_for('adminlogin.admin_login'))

        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)

        if request.method == 'POST':
            allocated_budget = float(request.form['allocated_budget'])  # Convert to float
            spent_budget = float(request.form['spent_budget'])  # Convert to float
            year = request.form['year']
            inhand_budget = allocated_budget - spent_budget
            print(inhand_budget)
            cursor.execute("INSERT INTO budget (allocated, spent, inhand, year) VALUES (%s, %s, %s, %s)",
                           (allocated_budget, spent_budget, inhand_budget, year))
            cnx.commit()

        sql = "SELECT * FROM budget"
        cursor.execute(sql)  # Corrected syntax for executing the SQL query
        budget = cursor.fetchall()  # Use fetchall to retrieve all rows
        print(budget)
        cursor.close()
        cnx.close()
        return render_template('Admin/budget.html', budget=budget)