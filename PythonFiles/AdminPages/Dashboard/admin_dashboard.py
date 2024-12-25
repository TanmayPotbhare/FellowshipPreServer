from datetime import timedelta, date
from Classes.database import HostConfig, ConfigPaths, ConnectParam
from openpyxl import Workbook
from io import BytesIO
import io
from flask import Blueprint, render_template, session, request, redirect, url_for, flash, jsonify, make_response
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
        """
            This function is used for giving dynamic count on the change of Year on Admin Dashboard.
            This AJAX Call is written in /static/admin.js file on line number 69.
        :return:
        """
        year = request.args.get('year', '2023')
        try:
            data = {
                'total_appl_count': total_application_count(year),
                'completed_form_count': completed_applications(year),
                'incomplete_form_count': incomplete_applications(year),
                'accepted_appl_count': accepted_applications(year),
                'rejected_appl_count': rejected_applications(year),
                'male_count': male_applications(year),
                'female_count': female_applications(year),
                'disabled_count': disabled_applications(year),
                'not_disabled_count': notdisabled_applications(year)
            }
            return jsonify(data)
        except Exception as e:
            print(f"Error fetching year count data: {e}")
            return jsonify({"error": "Failed to fetch data"}), 500

    @admin_dashboard_blueprint.route('/get_gender_data', methods=['GET'])
    def get_gender_data():
        """
            This function is used for giving dynamic gender count on the change of Year on Admin Dashboard.
            This AJAX Call is written in /templates/admin_dashboard.html file on line number 315.
        :return:
        """
        data = {
            'male_count': {year: male_applications(year) for year in range(2020, 2024)},
            'female_count': {year: female_applications(year) for year in range(2020, 2024)},
        }
        return jsonify(data)

    @admin_dashboard_blueprint.route('/get_disabled_data', methods=['GET'])
    def get_disabled_data():
        """
            This function is used for giving dynamic disability count on the change of Year on Admin Dashboard.
            This AJAX Call is written in /templates/admin_dashboard.html file on line number 481.
        :return:
        """
        data = {
            'disabled_count': {year: disabled_applications(year) for year in range(2020, 2024)},
            'not_disabled_count': {year: notdisabled_applications(year) for year in range(2020, 2024)},
        }
        return jsonify(data)

    @admin_dashboard_blueprint.route('/get_district_data', methods=['POST'])
    def get_district_data():
        """
            This function is used for giving dynamic gender count on the change of Year on Admin Dashboard.
            This AJAX Call is written in /templates/admin_dashboard.html file on line number 202.
        :return:
        """
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
            'female_count': female_applications(year),
            'pvtg_applications': pvtg_applications(),
            'disabled_count': disabled_applications(year),
            'not_disabled_count': notdisabled_applications(year)
        }
        katkari, kolam, madia = get_individual_counts()  # Use the function you created earlier
        counts = {'katkari': katkari, 'kolam': kolam, 'madia': madia}
        return render_template('AdminPages/admin_dashboard.html', data=data, counts=counts)

    @admin_dashboard_blueprint.route('/total_application_report', methods=['GET', 'POST'])
    def total_application_report():
        """
            This function is responsible for handling the dynamic fetching of application report data based
            on the selected year.
            Path of AJAX Call: /static/admin.js file on LINE 139.
            Path of HTML can be found in the render template of this function.
        :return:
        """
        if not session.get('logged_in'):
            # Redirect to the admin login page if the user is not logged in
            flash('Please enter Email ID and Password', 'error')
            return redirect(url_for('adminlogin.admin_login'))

        year = request.args.get('year', default=2023, type=int)
        # print(year)
        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)

        cursor.execute("SELECT * FROM application_page WHERE phd_registration_year = %s", (year,))
        result = cursor.fetchall()
        cnx.commit()
        cursor.close()
        cnx.close()
        # print(count(result))
        # If it's an AJAX request, return JSON data
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            for record in result:
                for key, value in record.items():
                    if isinstance(value, timedelta):
                        record[key] = str(value)  # Convert to a string (e.g., "5 days, 0:00:00")
                    if isinstance(value, date):
                        record[key] = value.strftime('%Y-%m-%d')  # Format date for JSON
            return jsonify(result)

        # print(result)
        return render_template('AdminPages/DashboardCountReports/total_application_report.html', result=result,
                               year=year)

    @admin_dashboard_blueprint.route('/completed_form', methods=['GET', 'POST'])
    def completed_form():
        """
            This function is responsible for handling the dynamic fetching of application report data based
            on the selected year.
            Path of AJAX Call: /static/admin.js file on LINE 217.
            Path of HTML can be found in the render template of this function.
        :return:
        """
        if not session.get('logged_in'):
            # Redirect to the admin login page if the user is not logged in
            flash('Please enter Email ID and Password', 'error')
            return redirect(url_for('adminlogin.admin_login'))

        year = request.args.get('year', default=2023, type=int)

        # print(year)
        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)

        cursor.execute(" SELECT * FROM application_page WHERE phd_registration_year = %s and form_filled='1' ", (year,))
        result = cursor.fetchall()

        cnx.commit()
        cursor.close()
        cnx.close()
        # print(count(result))
        # If it's an AJAX request, return JSON data
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            for record in result:
                for key, value in record.items():
                    if isinstance(value, timedelta):
                        record[key] = str(value)  # Convert to a string (e.g., "5 days, 0:00:00")
                    if isinstance(value, date):
                        record[key] = value.strftime('%Y-%m-%d')  # Format date for JSON
            return jsonify(result)

        # print(result)
        return render_template('AdminPages/DashboardCountReports/completed_form.html', result=result,
                               year=year)

    @admin_dashboard_blueprint.route('/incompleted_form', methods=['GET', 'POST'])
    def incompleted_form():
        """
            This function is responsible for handling the dynamic fetching of application report data based
            on the selected year.
            Path of AJAX Call: /static/admin.js file on LINE 296.
            Path of HTML can be found in the render template of this function.
        :return:
        """
        if not session.get('logged_in'):
            # Redirect to the admin login page if the user is not logged in
            flash('Please enter Email ID and Password', 'error')
            return redirect(url_for('adminlogin.admin_login'))

        year = request.args.get('year', default=2023, type=int)
        # print(year)
        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)

        cursor.execute(" SELECT * FROM application_page WHERE phd_registration_year = %s and form_filled='0' ", (year,))
        result = cursor.fetchall()
        cnx.commit()
        cursor.close()
        cnx.close()
        # print(count(result))
        # If it's an AJAX request, return JSON data
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            for record in result:
                for key, value in record.items():
                    if isinstance(value, timedelta):
                        record[key] = str(value)  # Convert to a string (e.g., "5 days, 0:00:00")
                    if isinstance(value, date):
                        record[key] = value.strftime('%Y-%m-%d')  # Format date for JSON
            return jsonify(result)

        # print(result)
        return render_template('AdminPages/DashboardCountReports/incompleted_form.html', result=result,
                               year=year)

    @admin_dashboard_blueprint.route('/total_accepted_report', methods=['GET', 'POST'])
    def total_accepted_report():
        """
            This function is responsible for handling the dynamic fetching of application report data based
            on the selected year.
            Path of AJAX Call: /static/admin.js file on LINE 374.
            Path of HTML can be found in the render template of this function.
        :return:
        """
        if not session.get('logged_in'):
            # Redirect to the admin login page if the user is not logged in
            flash('Please enter Email ID and Password', 'error')
            return redirect(url_for('adminlogin.admin_login'))

        year = request.args.get('year', default=2023, type=int)
        # print(year)
        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)

        cursor.execute(" SELECT * FROM application_page WHERE phd_registration_year = %s and form_filled='1' and final_approval='accepted' ", (year,))
        result = cursor.fetchall()
        cnx.commit()
        cursor.close()
        cnx.close()
        # print(count(result))
        # If it's an AJAX request, return JSON data
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            for record in result:
                for key, value in record.items():
                    if isinstance(value, timedelta):
                        record[key] = str(value)  # Convert to a string (e.g., "5 days, 0:00:00")
                    if isinstance(value, date):
                        record[key] = value.strftime('%Y-%m-%d')  # Format date for JSON
            return jsonify(result)

        # print(result)
        return render_template('AdminPages/DashboardCountReports/total_accepted_report.html', result=result,
                               year=year)

    @admin_dashboard_blueprint.route('/total_rejected_report', methods=['GET', 'POST'])
    def total_rejected_report():
        """
            This function is responsible for handling the dynamic fetching of application report data based
            on the selected year.
            Path of AJAX Call: /static/admin.js file on LINE 452.
            Path of HTML can be found in the render template of this function.
        :return:
        """
        if not session.get('logged_in'):
            # Redirect to the admin login page if the user is not logged in
            flash('Please enter Email ID and Password', 'error')
            return redirect(url_for('adminlogin.admin_login'))

        year = request.args.get('year', default=2023, type=int)
        # print(year)
        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)

        cursor.execute(
            " SELECT * FROM application_page WHERE phd_registration_year = %s and form_filled='1' and final_approval='rejected' ",
            (year,))
        result = cursor.fetchall()
        cnx.commit()
        cursor.close()
        cnx.close()
        # print(count(result))
        # If it's an AJAX request, return JSON data
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            for record in result:
                for key, value in record.items():
                    if isinstance(value, timedelta):
                        record[key] = str(value)  # Convert to a string (e.g., "5 days, 0:00:00")
                    if isinstance(value, date):
                        record[key] = value.strftime('%Y-%m-%d')  # Format date for JSON
            return jsonify(result)

        # print(result)
        return render_template('AdminPages/DashboardCountReports/total_rejected_report.html', result=result,
                               year=year)

    @admin_dashboard_blueprint.route('/male_report', methods=['GET', 'POST'])
    def male_report():
        """
            This function is responsible for handling the dynamic fetching of application report data based
            on the selected year.
            Path of AJAX Call: /static/admin.js file on LINE 530.
            Path of HTML can be found in the render template of this function.
        :return:
        """
        if not session.get('logged_in'):
            # Redirect to the admin login page if the user is not logged in
            flash('Please enter Email ID and Password', 'error')
            return redirect(url_for('adminlogin.admin_login'))

        year = request.args.get('year', default=2023, type=int)
        # print(year)
        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)

        cursor.execute(
            " SELECT * FROM application_page WHERE phd_registration_year = %s and gender='Male' ",
            (year,))
        result = cursor.fetchall()
        cnx.commit()
        cursor.close()
        cnx.close()
        # print(count(result))
        # If it's an AJAX request, return JSON data
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            for record in result:
                for key, value in record.items():
                    if isinstance(value, timedelta):
                        record[key] = str(value)  # Convert to a string (e.g., "5 days, 0:00:00")
                    if isinstance(value, date):
                        record[key] = value.strftime('%Y-%m-%d')  # Format date for JSON
            return jsonify(result)

        # print(result)
        return render_template('AdminPages/DashboardCountReports/male_report.html', result=result,
                               year=year)

    @admin_dashboard_blueprint.route('/female_report', methods=['GET', 'POST'])
    def female_report():
        """
            This function is responsible for handling the dynamic fetching of application report data based
            on the selected year.
            Path of AJAX Call: /static/admin.js file on LINE 615.
            Path of HTML can be found in the render template of this function.
        :return:
        """
        if not session.get('logged_in'):
            # Redirect to the admin login page if the user is not logged in
            flash('Please enter Email ID and Password', 'error')
            return redirect(url_for('adminlogin.admin_login'))

        year = request.args.get('year', default=2023, type=int)
        # print(year)
        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)

        cursor.execute(
            " SELECT * FROM application_page WHERE phd_registration_year = %s and gender='Female' ",
            (year,))
        result = cursor.fetchall()
        cnx.commit()
        cursor.close()
        cnx.close()
        # print(count(result))
        # If it's an AJAX request, return JSON data
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            for record in result:
                for key, value in record.items():
                    if isinstance(value, timedelta):
                        record[key] = str(value)  # Convert to a string (e.g., "5 days, 0:00:00")
                    if isinstance(value, date):
                        record[key] = value.strftime('%Y-%m-%d')  # Format date for JSON
            return jsonify(result)

        # print(result)
        return render_template('AdminPages/DashboardCountReports/female_report.html', result=result,
                               year=year)

    @admin_dashboard_blueprint.route('/disabled_report', methods=['GET', 'POST'])
    def disabled_report():
        """
            This function is responsible for handling the dynamic fetching of application report data based
            on the selected year.
            Path of AJAX Call: /static/admin.js file on LINE 615.
            Path of HTML can be found in the render template of this function.
        :return:
        """
        if not session.get('logged_in'):
            # Redirect to the admin login page if the user is not logged in
            flash('Please enter Email ID and Password', 'error')
            return redirect(url_for('adminlogin.admin_login'))

        year = request.args.get('year', default=2023, type=int)
        # print(year)
        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)

        cursor.execute(
            " SELECT * FROM application_page WHERE phd_registration_year = %s and disability='Yes' ",
            (year,))
        result = cursor.fetchall()
        cnx.commit()
        cursor.close()
        cnx.close()
        # print(count(result))
        # If it's an AJAX request, return JSON data
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            for record in result:
                for key, value in record.items():
                    if isinstance(value, timedelta):
                        record[key] = str(value)  # Convert to a string (e.g., "5 days, 0:00:00")
                    if isinstance(value, date):
                        record[key] = value.strftime('%Y-%m-%d')  # Format date for JSON
            return jsonify(result)

        # print(result)
        return render_template('AdminPages/DashboardCountReports/disabled_report.html', result=result,
                               year=year)

    @admin_dashboard_blueprint.route('/not_disabled_report', methods=['GET', 'POST'])
    def not_disabled_report():
        """
            This function is responsible for handling the dynamic fetching of application report data based
            on the selected year.
            Path of AJAX Call: /static/admin.js file on LINE 615.
            Path of HTML can be found in the render template of this function.
        :return:
        """
        if not session.get('logged_in'):
            # Redirect to the admin login page if the user is not logged in
            flash('Please enter Email ID and Password', 'error')
            return redirect(url_for('adminlogin.admin_login'))

        year = request.args.get('year', default=2023, type=int)
        # print(year)
        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)

        cursor.execute(
            " SELECT * FROM application_page WHERE phd_registration_year = %s and disability='No' ",
            (year,))
        result = cursor.fetchall()
        cnx.commit()
        cursor.close()
        cnx.close()
        # print(count(result))
        # If it's an AJAX request, return JSON data
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            for record in result:
                for key, value in record.items():
                    if isinstance(value, timedelta):
                        record[key] = str(value)  # Convert to a string (e.g., "5 days, 0:00:00")
                    if isinstance(value, date):
                        record[key] = value.strftime('%Y-%m-%d')  # Format date for JSON
            return jsonify(result)

        # print(result)
        return render_template('AdminPages/DashboardCountReports/not_disabled_report.html', result=result,
                               year=year)

    @admin_dashboard_blueprint.route('/export_to_excel', methods=['GET'])
    def export_to_excel():
        """
            This function is responsible for handling the dynamic exporting of application report data based
            on the selected year.
            Path of AJAX Call: /static/admin.js. (Search the form_types in the JS File)
            Path of HTML can be found in the respective templates.
        """
        if not session.get('logged_in'):
            flash('Please enter Email ID and Password', 'error')
            return redirect(url_for('adminlogin.admin_login'))

        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)

        year = request.args.get('year', default=2023, type=int)
        # print(year)
        form_type = request.args.get('form_type')  # Get the form type (e.g., "completed_form")

        # Dynamically change the SQL query based on form_type
        if form_type == "total_application_records":
            cursor.execute("SELECT * FROM application_page WHERE phd_registration_year = %s", (year,))
        elif form_type == "completed_form_records":
            cursor.execute("SELECT * FROM application_page WHERE phd_registration_year = %s AND form_filled='1'",
                           (year,))
        elif form_type == "incomplete_form_records":
            cursor.execute("SELECT * FROM application_page WHERE phd_registration_year = %s AND form_filled='0'",
                           (year,))
        elif form_type == 'accepted_records':
            cursor.execute(" SELECT * FROM application_page WHERE phd_registration_year = %s AND "
                           "final_approval='accepted' AND form_filled=1 ",
                           (year,))
        elif form_type == 'rejected_records':
            cursor.execute(" SELECT * FROM application_page WHERE phd_registration_year = %s AND "
                           "final_approval='rejected' AND form_filled=1 ",
                           (year,))
        elif form_type == 'male_application_records':
            cursor.execute(" SELECT * FROM application_page WHERE phd_registration_year = %s and gender='Male' ",
                           (year,))
        elif form_type == 'female_application_records':
            cursor.execute(" SELECT * FROM application_page WHERE phd_registration_year = %s and gender='Female' ",
                           (year,))
        elif form_type == 'disabled_application_records':
            cursor.execute(" SELECT * FROM application_page WHERE phd_registration_year = %s and disability='Yes' ",
                           (year,))
        elif form_type == 'not_disabled_application_records':
            cursor.execute(" SELECT * FROM application_page WHERE phd_registration_year = %s and disability='No' ",
                           (year,))
        else:
            # Handle other form types or default case
            flash('Error fetching Details. Some details are missing.', 'error')

        data = cursor.fetchall()  # Fetch the results

        # Close the connection
        cursor.close()
        cnx.close()

        # Create an Excel workbook
        workbook = Workbook()
        sheet = workbook.active
        sheet.title = f"Data_{year}"

        # Write headers
        if data:
            headers = list(data[0].keys())  # Get the column headers from the first row
            sheet.append(headers)  # Add headers to the first row

            # Write data rows
            for row_data in data:
                sheet.append(list(row_data.values()))  # Add each row of data

        # Save the workbook to an in-memory stream
        output = BytesIO()
        workbook.save(output)
        output.seek(0)

        # Return the file as a downloadable response
        response = make_response(output.read())
        response.headers['Content-Disposition'] = f'attachment; filename=export_{form_type}_{year}.xlsx'
        response.headers['Content-type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        return response
