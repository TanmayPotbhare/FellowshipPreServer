from flask import Blueprint, render_template, session, request, redirect, url_for, jsonify
import os
import mysql.connector
# Middleware import
from authentication.middleware import auth
from classes.university import universityController
from classes.connection import HostConfig, ConfigPaths


section2_blueprint = Blueprint('section2', __name__)


def section2_auth(app):
    # ------ HOST Configs are in classes/connection.py
    host = HostConfig.host
    app_paths = ConfigPaths.paths.get(host)
    if app_paths:
        for key, value in app_paths.items():
            app.config[key] = value

    @section2_blueprint.route('/section2', methods=['GET', 'POST'])
    @auth
    def section2():
        email = session['email']
        print('I am in section 2:' + email)
        cnx = mysql.connector.connect(user='root', password='A9CALcsd7lc%7ac',
                                      host=host,
                                      database='ICSApplication')
        cursor = cnx.cursor(dictionary=True)
        university_data = universityController(host)
        university_names = university_data.get_all_university()
        # Check if a record already exists for this user
        cursor.execute("SELECT ssc_passing_year, ssc_percentage, ssc_school_name, "
                       "hsc_passing_year, hsc_percentage, hsc_school_name, graduation_passing_year, "
                       "graduation_percentage, graduation_school_name, phd_passing_year, phd_percentage, "
                       "phd_school_name, have_you_qualified, phd_registration_year, "
                       "concerned_university, department_name, topic_of_phd, name_of_guide, name_of_college, "
                       " faculty, family_annual_income, phd_registration_date,"
                       "income_certificate_number, issuing_authority,ssc_stream,ssc_attempts,ssc_total,hsc_stream,hsc_attempts,"
                       "hsc_total,grad_stream,grad_attempts,grad_total,pg_stream,pg_attempts,pg_total, income_issuing_district "
                       "FROM application_page WHERE email = %s", (email,))
        existing_record = cursor.fetchone()
        print('existing_record', existing_record)
        cursor.execute('SELECT year FROM signup where email = %s', (email,))
        signup_year = cursor.fetchone()
        cursor.execute('SELECT YEAR(date_of_birth) AS birth_year FROM application_page where email = %s', (email,))
        dob_year = cursor.fetchone()

        if existing_record:
            # Determine whether the user is in "view" or "edit" mode
            if not any(value is None or value == '' for value in existing_record.values()):
                view_mode = 'view'
            else:
                view_mode = 'edit'
        else:
            # Handle the case when existing_record is None or empty
            view_mode = 'edit'  # or 'view', depending on your logic for this case

        # print(existing_record.values())

        if request.method == 'POST':
            ssc_passing_year = request.form['ssc_passing_year']
            ssc_percentage = request.form['ssc_percentage']
            ssc_school_name = request.form['ssc_school_name']
            hsc_passing_year = request.form['hsc_passing_year']
            hsc_percentage = request.form['hsc_percentage']
            hsc_school_name = request.form['hsc_school_name']
            graduation_passing_year = request.form['graduation_passing_year']
            graduation_percentage = request.form['graduation_percentage']
            graduation_school_name = request.form['graduation_school_name']
            phd_passing_year = request.form['phd_passing_year']
            phd_percentage = request.form['phd_percentage']
            phd_school_name = request.form['phd_school_name']
            have_you_qualified = request.form['have_you_qualified']
            cet_other = request.form['cet_other']
            phd_registration_date = request.form['phd_registration_date']
            phd_registration_year = request.form['phd_registration_year']
            phd_registration_age = request.form['phd_registration_age']
            concerned_university = request.form['concerned_university']
            topic_of_phd = request.form['topic_of_phd']
            name_of_guide = request.form['name_of_guide']
            name_of_college = request.form['name_of_college']
            print(name_of_college)
            faculty = request.form['faculty']
            family_annual_income = request.form['family_annual_income']
            income_certificate_number = request.form['income_certificate_number']
            issuing_authority = request.form['issuing_authority']
            # Code added by Akash /*-------------- Starts here ------------*/
            # for ssc changes percentage
            ssc_stream = request.form['ssc_stream']
            ssc_attempts = request.form['ssc_attempts']
            ssc_total = request.form['ssc_total']

            # for hsc percentage changes
            hsc_stream = request.form['hsc_stream']
            hsc_attempts = request.form['hsc_attempts']
            hsc_total = request.form['hsc_total']

            # For Graduation section
            grad_stream = request.form['grad_stream']
            grad_attempts = request.form['grad_attempts']
            grad_total = request.form['grad_total']

            # Post Graduation Section
            pg_stream = request.form['pg_stream']
            pg_attempts = request.form['pg_attempts']
            pg_total = request.form['pg_total']

            # Department section of college
            department_name = request.form['department_name']
            income_issuing_district = request.form['income_issuing_district']
            income_issuing_taluka = request.form['income_issuing_taluka']

            print("Values in existing_record:", existing_record.values())
            if all(value is None or value == '' for value in existing_record.values()):
                print('Inserting new record for:' + email)
                if view_mode == 'edit':
                    cursor.execute(
                        "UPDATE application_page SET ssc_passing_year = %s, ssc_percentage = %s, ssc_school_name = %s, "
                        "hsc_passing_year = %s, hsc_percentage = %s, hsc_school_name = %s, graduation_passing_year = %s, "
                        "graduation_percentage = %s, graduation_school_name = %s, phd_passing_year = %s, phd_percentage = %s, "
                        "phd_school_name = %s, have_you_qualified = %s, phd_registration_date = %s, phd_registration_year = %s, "
                        "phd_registration_age = %s, concerned_university = %s, topic_of_phd = %s, name_of_guide = %s, name_of_college = %s, "
                        " faculty = %s, family_annual_income = %s, "
                        "income_certificate_number = %s, issuing_authority = %s,ssc_stream = %s, ssc_attempts =%s,"
                        "ssc_total = %s, hsc_stream = %s,hsc_attempts = %s,hsc_total = %s,grad_stream = %s,"
                        "grad_attempts =%s, grad_total = %s, pg_stream = %s, pg_attempts = %s, pg_total = %s,"
                        "department_name = %s,income_issuing_district = %s, income_issuing_taluka =%s, have_you_qualified_other = %s  "
                        "WHERE email = %s",
                        (ssc_passing_year, ssc_percentage, ssc_school_name, hsc_passing_year, hsc_percentage,
                         hsc_school_name,
                         graduation_passing_year, graduation_percentage, graduation_school_name, phd_passing_year,
                         phd_percentage,
                         phd_school_name, have_you_qualified, phd_registration_date, phd_registration_year,
                         phd_registration_age, concerned_university,
                         topic_of_phd, name_of_guide, name_of_college, faculty,
                         family_annual_income, income_certificate_number, issuing_authority, ssc_stream,
                         ssc_attempts, ssc_total, hsc_stream, hsc_attempts, hsc_total, grad_stream, grad_attempts,
                         grad_total, pg_stream, pg_attempts, pg_total, department_name, income_issuing_district,
                         income_issuing_taluka, cet_other, email))
                    cnx.commit()
                return redirect(url_for('section3.section3'))
        # Select records again to verify the insertion
        cursor.execute("SELECT ssc_passing_year, ssc_percentage, ssc_school_name, "
                       "hsc_passing_year, hsc_percentage, hsc_school_name, graduation_passing_year, "
                       "graduation_percentage, graduation_school_name, phd_passing_year, phd_percentage, "
                       "phd_school_name, have_you_qualified, phd_registration_year, "
                       "concerned_university, department_name, topic_of_phd, name_of_guide, name_of_college, "
                       "other_college_name,  faculty, family_annual_income, phd_registration_date,"
                       "income_certificate_number, issuing_authority,ssc_stream,ssc_attempts,ssc_total,hsc_stream,hsc_attempts,"
                       "hsc_total,grad_stream,grad_attempts,grad_total,pg_stream,pg_attempts,pg_total, income_issuing_district,"
                       "diploma_percentage, diploma_passing_year, diploma_stream, diploma_school_name, diploma_attempts, diploma_total "
                       "FROM application_page WHERE email = %s", (email,))
        new_record = cursor.fetchone()
        print('new_record', new_record)
        # Initialize view_mode with a default value

        return render_template('Candidate/NewUser/ApplicationForm/AForm_section2.html', existing_record=existing_record, view_mode=view_mode,
                               university_data=university_names, signup_year=signup_year, dob_year=dob_year,
                               new_record=new_record)

    @section2_blueprint.route('/get_college_data_by_university', methods=['GET', 'POST'])
    def get_college_data_by_university():
        u_id = request.form.get('u_id')
        print(u_id)
        college_obj = universityController(host)
        college_name = college_obj.get_college_name(u_id)
        return jsonify(college_name)