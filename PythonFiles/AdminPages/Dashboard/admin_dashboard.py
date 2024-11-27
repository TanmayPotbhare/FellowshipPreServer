from Classes.database import HostConfig, ConfigPaths, ConnectParam
from flask import Blueprint, render_template, session, request, redirect, url_for, flash, jsonify
from PythonFiles.AdminPages.Dashboard.dashboardCount_functions import *

admin_dashboard_blueprint = Blueprint('admin_dashboard', __name__)


def admin_dashboard_auth(app):
    # ------ HOST Configs are in classes/connection.py
    host = HostConfig.host
    app_paths = ConfigPaths.paths.get(host)
    if app_paths:
        for key, value in app_paths.items():
            app.config[key] = value

    @admin_dashboard_blueprint.route('/get_year_count', methods=['GET', 'POST'])
    def get_year_count():
        year = request.args.get('year', '2023')
        # print(year)
        # Try-catch to catch any errors while fetching data

        data = {
            'total_appl_count': total_application_count(year),
            'completed_form_count': completed_applications(year),
            'incomplete_form_count': incomplete_applications(year),
            'accepted_appl_count': accepted_applications(year),
            'rejected_appl_count': rejected_applications(year),
            'male_count': male_applications(year),
            'female_count': female_applications(year)
        }
        return data
        # Proceed with your logic

    @admin_dashboard_blueprint.route('/get_gender_data', methods=['GET'])
    def get_gender_data():
        data = {
            'male_count': {year: male_applications(year) for year in range(2020, 2024)},
            'female_count': {year: female_applications(year) for year in range(2020, 2024)},
        }
        return jsonify(data)

    @admin_dashboard_blueprint.route('/get_district_data', methods=['POST'])
    def get_district_data():
        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect()

        # Get the year from the request
        selected_year = request.form['selected_year']

        # Queries to get district data for the map
        district_query = """SELECT district, COUNT(*) AS student_count 
                                            FROM application_page 
                                            WHERE phd_registration_year = %s 
                                            GROUP BY district;"""
        # Execute district count query
        cursor.execute(district_query, (selected_year,))
        district_results = cursor.fetchall()

        # Construct district data dictionary
        district_data = {row[0]: row[1] for row in district_results}  # row[0] is district, row[1] is student_count

        return jsonify(district_data=district_data)

    @admin_dashboard_blueprint.route('/admin_dashboard', methods=['GET', 'POST'])
    def admin_dashboard():
        if not session.get('logged_in'):
            # Redirect to the admin login page if the user is not logged in
            flash('Please enter Email ID and Password', 'error')
            return redirect(url_for('adminlogin.admin_login'))

        year = request.args.get('year', '2023')
        # print(year)
        # Try-catch to catch any errors while fetching data

        data = {
            'total_appl_count': total_application_count(year),
            'completed_form_count': completed_applications(year),
            'incomplete_form_count': incomplete_applications(year),
            'accepted_appl_count': accepted_applications(year),
            'rejected_appl_count': rejected_applications(year),
            'male_count': male_applications(year),
            'female_count': female_applications(year)
        }

        return render_template('AdminPages/admin_dashboard.html', data=data)