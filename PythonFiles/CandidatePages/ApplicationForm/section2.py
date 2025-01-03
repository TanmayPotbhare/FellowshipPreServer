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
        cursor.execute("SELECT ssc_passing_year, ssc_percentage, ssc_school_name, "
                       "hsc_passing_year, hsc_percentage, hsc_school_name, graduation_passing_year, "
                       "graduation_percentage, graduation_school_name, phd_passing_year, phd_percentage, "
                       "phd_school_name, have_you_qualified, phd_registration_year, "
                       "concerned_university, department_name, topic_of_phd, name_of_guide, name_of_college, "
                       " faculty, family_annual_income, phd_registration_date, section2"
                       "income_certificate_number, issuing_authority, ssc_stream, ssc_attempts, ssc_total, hsc_stream, hsc_attempts,"
                        "hsc_total,grad_stream,grad_attempts, grad_total, pg_stream, pg_attempts,pg_total, income_issuing_district "
                       " FROM application_page WHERE email = %s", (email,))
        record = cursor.fetchone()

        # Initialize an empty dictionary if no record is found
        if record is None:
            record = {}

        if request.method == 'POST':
            ssc_passing_year = request.form['ssc_passing_year']
            stream = request.form['stream']
            ssc_school_name = request.form['ssc_school_name']
            ssc_attempts = request.form['ssc_attempts']
            ssc_total = request.form['ssc_total']
            ssc_percentage = request.form['ssc_percentage']

            hsc_passing_year = request.form['hsc_passing_year']
            hsc_stream = session['hsc_stream']
            hsc_school_name = request.form['hsc_school_name']
            hsc_attempts = request.form['hsc_attempts']
            hsc_total = request.form['hsc_total']
            hsc_percentage = request.form['hsc_percentage']

            graduation_passing_year = request.form['graduation_passing_year']
            grad_stream = request.form['grad_stream']
            graduation_school_name = request.form['graduation_school_name']
            grad_attempts = request.form['grad_attempts']
            grad_total = request.form['grad_total']
            graduation_percentage = request.form['graduation_percentage']

            phd_passing_year = request.form['phd_passing_year']
            pg_stream = request.form['pg_stream']
            phd_school_name = request.form['phd_school_name']
            pg_attempts = request.form['pg_attempts']
            pg_total = request.form['pg_total']
            phd_percentage = request.form['phd_percentage']

            have_you_qualified = request.form['have_you_qualified']
            phd_registration_date = request.form['phd_registration_date']
            fellowship_applying_year = request.form['fellowship_applying_year']
            phd_registration_day = request.form['phd_registration_day']
            phd_registration_month = request.form['phd_registration_month']
            phd_registration_year = request.form['phd_registration_year']
            phd_registration_age = request.form['phd_registration_age']

            concerned_university = request.form['concerned_university']
            other_university = request.form['other_university']
            name_of_college = request.form['name_of_college']
            other_college_name = request.form['other_college_name']
            department_name = request.form['department_name']
            topic_of_phd = request.form['topic_of_phd']
            name_of_guide = request.form['name_of_guide']
            faculty = request.form['faculty']
            other_faculty = request.form['other_faculty']

            section2 = 'filled'

            print(request.form)



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
