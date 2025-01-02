import datetime
import requests
import os
from Classes.caste import casteController
from Classes.database import HostConfig, ConfigPaths, ConnectParam
from flask import Blueprint, render_template, session, request, redirect, url_for, flash, make_response, jsonify

from Classes.university import universityController

section2_blueprint = Blueprint('section2', __name__)


def section2_auth(app):
    # ------ HOST Configs are in classes/connection.py
    host = HostConfig.host
    app_paths = ConfigPaths.paths.get(host)
    if app_paths:
        for key, value in app_paths.items():
            app.config[key] = value

    @section2_blueprint.route('/section2', methods=['GET', 'POST'])
    def section2():
        if not session.get('logged_in_from_login'):
            # Redirect to the admin login page if the user is not logged in
            return redirect(url_for('login_signup.login'))

        if session.get('show_flash', True):  # Retrieve and clear the flag
            flash('Profile section has been successfully saved.', 'success')

        email = session['email']

        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)

        university_data = universityController(host)
        university_names = university_data.get_all_university()

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

            return render_template('CandidatePages/ApplicationForm/section2.html', record=record, university_data=university_names,
                                   finally_approved=finally_approved, user=user, photo=photo, signup_record=signup_record,
                                   title='Application Form (Personal Details)')
        else:
            user = "Student"
            photo = '/static/assets/img/default_user.png'
            finally_approved = 'pending'

        cursor.execute("SELECT * FROM signup WHERE email = %s", (email,))
        signup_record = cursor.fetchone()

        return render_template('CandidatePages/ApplicationForm/section2.html', record=record, university_data=university_names,
                               finally_approved=finally_approved, user=user, photo=photo, signup_record=signup_record,
                               title='Application Form (Personal Details)')

    @section2_blueprint.route('/section2_submit', methods=['GET', 'POST'])
    def section2_submit():
        if not session.get('logged_in_from_login'):
            # Redirect to the admin login page if the user is not logged in
            return redirect(url_for('login_signup.login'))

        email = session['email']

        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)

        # Check if a record already exists for this user
        cursor.execute("SELECT applicant_photo, adhaar_number, adhaar_seeding, first_name, final_approval,"
                       "middle_name, last_name, mobile_number, email, date_of_birth, gender, age, caste, your_caste, subcaste,"
                       "pvtg, pvtg_caste, marital_status, add_1, add_2, pincode, village, taluka, district, state, city"
                       " FROM application_page WHERE email = %s", (email,))
        record = cursor.fetchone()

        # Initialize an empty dictionary if no record is found
        if record is None:
            record = {}

        if request.method == 'POST':
            photo = request.files['applicant_photo']
            adhaar_number = request.form['adhaar_number']
            adhaar_seeding = request.files['adhaar_seeding_bank']
            first_name = request.form['first_name']
            middle_name = request.form['middle_name']
            last_name = request.form['last_name']
            mobile_number = request.form['mobile_number']
            email = session['email']
            date_of_birth = request.form['date_of_birth']
            gender = request.form['gender']
            age = request.form['age']
            category = request.form['category']
            pvtg = request.form['pvtg']
            pvtg_caste = request.form['pvtg_caste']
            caste = request.form['caste']
            subcaste = request.form['subcaste']
            marital_status = request.form['marital_status']
            add_1 = request.form['add_1']
            pincode = request.form['pincode']
            village = request.form['village']
            taluka = request.form['taluka']
            district = request.form['district']
            state = request.form['state']
            comm_add_1 = request.form['comm_add_1']
            comm_pincode = request.form['comm_pincode']
            comm_village = request.form['comm_village']
            comm_taluka = request.form['comm_taluka']
            comm_district = request.form['comm_district']
            comm_state = request.form['comm_state']
            section1 = 'filled'

            print(request.form)

            # Handle file upload (applicant's photo)
            photo_path = save_applicant_photo(photo, first_name, last_name)
            adhaar_path = save_applicant_photo(adhaar_seeding, first_name, last_name)

            if not record:
                # Save the form data to the database
                print('Inserting new record for:' + email)
                sql = """
                INSERT INTO application_page (
                    applicant_photo, adhaar_number, adhaar_seeding, first_name, middle_name, last_name, 
                    mobile_number, email, date_of_birth, gender, age, caste, pvtg, pvtg_caste, your_caste, 
                    subcaste, marital_status, add_1, pincode, village, taluka, district, state, 
                    comm_add_1, comm_pincode, comm_village, comm_taluka, comm_district, comm_state, section1
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, 
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                    %s, %s, %s, %s, %s, %s, %s, %s, 
                    %s, %s, %s, %s, %s, %s, %s
                )
                """

                values = (
                    photo_path, adhaar_number, adhaar_path, first_name, middle_name, last_name,
                    mobile_number, email, date_of_birth, gender, age, category, pvtg, pvtg_caste, caste,
                    subcaste, marital_status, add_1, pincode, village, taluka, district, state,
                    comm_add_1, comm_pincode, comm_village, comm_taluka, comm_district, comm_state, section1
                )

                cursor.execute(sql, values)
                cnx.commit()
                return redirect(url_for('section3.section3'))
                # Check if the user is approved for fellowship no matter the year to show the desired sidebar.

        return redirect(url_for('section2.section2'))
