import os
import mysql.connector
import requests

from classes.connection import HostConfig, ConfigPaths
from flask import Blueprint, render_template, session, request, redirect, url_for, jsonify
# Middleware import
from authentication.middleware import auth
from classes.university import universityController

section4_blueprint = Blueprint('section4', __name__)


def section4_auth(app):
    # ------ HOST Configs are in classes/connection.py
    host = HostConfig.host
    app_paths = ConfigPaths.paths.get(host)
    if app_paths:
        for key, value in app_paths.items():
            app.config[key] = value

    @section4_blueprint.route('/section4', methods=['GET', 'POST'])
    def section4():
        email = session['email']
        print('I am in section 4:' + email)
        cnx = mysql.connector.connect(user='root', password='A9CALcsd7lc%7ac',
                                      host=host,
                                      database='ICSApplication')
        cursor = cnx.cursor(dictionary=True)

        # Check if a record already exists for this user
        cursor.execute("SELECT father_name, mother_name, work_in_government, bank_name, account_number, "
                       "ifsc_code, account_holder_name, micr FROM application_page WHERE email = %s", (email,))
        existing_record = cursor.fetchone()
        print(existing_record)

        if existing_record is not None:
            # Determine whether the user is in "view" or "edit" mode
            if not any(existing_record.values()):
                view_mode = 'edit'
            else:
                view_mode = 'view'
        else:
            # Handle the case when existing_record is None
            view_mode = 'edit'  # or 'view', depending on your logic for this case

        if request.method == 'POST':
            # Save form data in the session for this section
            father_name = request.form['father_name']
            mother_name = request.form['mother_name']
            work_in_government = request.form['work_in_government']
            gov_department = request.form['gov_department']
            gov_position = request.form['gov_position']
            bank_name = request.form['bank_name']
            account_number = request.form['account_number']
            ifsc_code = request.form['ifsc_code']
            account_holder_name = request.form['account_holder_name']
            micr = request.form['micr']
            # Process the fields as needed
            print(request.form)
            print("I am breaking before the if condition")
            if all(value is None for value in existing_record.values()):
                # Save the form data to the database
                print('I am breaking while insertion')
                print('Inserting new record for:' + email)
                if view_mode == 'edit':
                    cursor.execute(
                        "UPDATE application_page SET father_name = %s, mother_name = %s, work_in_government = %s,"
                        "gov_department = %s, gov_position = %s, bank_name = %s, account_number = %s, "
                        "ifsc_code = %s, account_holder_name = %s, micr = %s WHERE email = %s",
                        (father_name, mother_name, work_in_government, gov_department, gov_position, bank_name,
                         account_number, ifsc_code, account_holder_name, micr,
                         email))
                    cnx.commit()
                return redirect(url_for('section5.section5'))
            # Select records again to verify the insertion
            cursor.execute(
                "SELECT father_name, mother_name, work_in_government, gov_department, gov_position, bank_name,"
                "account_number, ifsc_code, account_holder_name, micr FROM application_page WHERE email = %s", (email,))
            existing_record = cursor.fetchone()
            print(existing_record)
        return render_template('Candidate/NewUser/ApplicationForm/AForm_section4.html', existing_record=existing_record, view_mode=view_mode)

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