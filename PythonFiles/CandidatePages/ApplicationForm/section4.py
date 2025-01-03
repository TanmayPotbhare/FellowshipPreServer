import datetime
import requests
import os
from Classes.caste import casteController
from Classes.database import HostConfig, ConfigPaths, ConnectParam
from flask import Blueprint, render_template, session, request, redirect, url_for, flash, make_response, jsonify


section4_blueprint = Blueprint('section4', __name__)


def section4_auth(app):
    # ------ HOST Configs are in classes/connection.py
    host = HostConfig.host
    app_paths = ConfigPaths.paths.get(host)
    if app_paths:
        for key, value in app_paths.items():
            app.config[key] = value

    @section4_blueprint.route('/get_ifsc_data', methods=['GET'])
    def get_ifsc_data():
        ifsc = request.args.get('ifsc')
        api_url = f'https://ifsc.razorpay.com/{ifsc}'
        try:
            response = requests.get(api_url)
            response.raise_for_status()  # Raise an exception for bad responses (4xx or 5xx)
            data = response.json()
            return jsonify(data)
        except requests.exceptions.RequestException as e:
            return jsonify({'error': str(e)}), 500
    

    @section4_blueprint.route('/section4', methods=['GET', 'POST'])
    def section4():
        if not session.get('logged_in_from_login'):
            # Redirect to the admin login page if the user is not logged in
            return redirect(url_for('login_signup.login'))

        email = session['email']

        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)

        caste_class = casteController(host)
        all_caste = caste_class.get_all_caste_details()

        # Check if a record already exists for this user
        cursor.execute("SELECT * FROM application_page WHERE email = %s", (email,))
        record = cursor.fetchone()

        if record:
            # print(record)
            if record['final_approval'] not in ['accepted', 'None', '']:
                finally_approved = 'pending'
            else:
                finally_approved = 'approved'

            if record:
                user = record['first_name'] + ' ' + record['last_name']
                photo = record['applicant_photo']
            else:
                user = "Admin"
                photo = '/static/assets/img/default_user.png'

            signup_record = record['email']

            return render_template('CandidatePages/ApplicationForm/section4.html', record=record, all_caste=all_caste,
                                   finally_approved=finally_approved, user=user, photo=photo, signup_record=signup_record,
                                   title='Application Form (Personal Details)')
        else:
            user = "Student"
            finally_approved = 'pending'

            cursor.execute("SELECT * FROM signup WHERE email = %s", (email,))
            signup_record = cursor.fetchone()

        return render_template('CandidatePages/ApplicationForm/section4.html', record=record, all_caste=all_caste,
                               finally_approved=finally_approved, user=user, signup_record=signup_record,
                               title='Application Form (Personal Details)')

    @section4_blueprint.route('/section4_submit', methods=['GET', 'POST'])
    def section4_submit():
        if not session.get('logged_in_from_login'):
            # Redirect to the admin login page if the user is not logged in
            return redirect(url_for('login_signup.login'))

        email = session['email']

        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)

        # Check if a record already exists for this user
        cursor.execute("""
            SELECT section4 FROM application_page WHERE email = %s
        """, (email,))
        record = cursor.fetchone()
        filled_section4 = record['section4']
        # Initialize an empty dictionary if no record is found
        # if record is None:
        #     record = {}

        if request.method == 'POST':
            father_name = request.form['father_name']
            mother_name = request.form['mother_name']
            work_in_government = request.form['work_in_government']
            gov_department = request.form['gov_department']
            gov_position = request.form['gov_position']
            bank_name = request.form['bank_name']
            print(bank_name)
            account_number = request.form['account_number']
            ifsc_code = request.form['ifsc_code']
            account_holder_name = request.form['account_holder_name']
            micr = request.form['micr']
            section4 = 'filled'


            if filled_section4 != 'filled':
                # Save the form data to the database
                sql = """
                        UPDATE application_page
                        SET
                            father_name = %s, mother_name = %s,work_in_government = %s,gov_department = %s,gov_position = %s,
                            bank_name = %s,account_number = %s,ifsc_code = %s, account_holder_name = %s, micr = %s, section4 = %s
                        WHERE email = %s
                    """
                values = (
                    father_name, mother_name, work_in_government, gov_department, gov_position,
                    bank_name, account_number, ifsc_code, account_holder_name, micr, section4, email
                )

                cursor.execute(sql, values)
                cnx.commit()
                session['show_flash'] = True
                return redirect(url_for('section5.section5'))
                # Check if the user is approved for fellowship no matter the year to show the desired sidebar.
        else:
            return redirect(url_for('section4.section4'))
