import os
import mysql.connector
from classes.connection import HostConfig, ConfigPaths
from flask import Blueprint, render_template, session, request, redirect, url_for
# Middleware import
from authentication.middleware import auth
from classes.university import universityController

section3_blueprint = Blueprint('section3', __name__)


def section3_auth(app):
    # ------ HOST Configs are in classes/connection.py
    host = HostConfig.host
    app_paths = ConfigPaths.paths.get(host)
    if app_paths:
        for key, value in app_paths.items():
            app.config[key] = value

    @section3_blueprint.route('/section3', methods=['GET', 'POST'])
    @auth
    def section3():
        email = session['email']
        print('I am in section 3:' + email)
        cnx = mysql.connector.connect(user='root', password='A9CALcsd7lc%7ac',
                                      host=host,
                                      database='ICSApplication')
        cursor = cnx.cursor(dictionary=True)

        # Check if a record already exists for this user
        cursor.execute("SELECT domicile, domicile_certificate, domicile_number, caste_certf, issuing_district, "
                       "caste_issuing_authority, salaried, disability, type_of_disability, caste_certf_number,validity_certificate, validity_cert_number, validity_issuing_district, validity_issuing_authority  "
                       "FROM application_page WHERE email = %s", (email,))
        existing_record = cursor.fetchone()
        print("existing_record", existing_record)
        # print(existing_record)
        # Check if existing_record is not None
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
            if request.method == 'POST':
                domicile = request.form['domicile']
                domicile_certificate = request.form['domicile_certificate']
                domicile_number = request.form['domicile_number']
                caste_certf = request.form['caste_certf']
                issuing_district = request.form['issuing_district']
                caste_issuing_authority = request.form['caste_issuing_authority']
                caste_cert_number = request.form['caste_cert_number']
                validity_certificate = request.form['validity_certificate']
                validity_num = request.form['validity_num']
                validity_issuing_district = request.form['validity_issuing_district']
                validity_issuing_authority = request.form['validity_issuing_authority']
                salaried = request.form['salaried']
                disability = request.form['disability']
                type_of_disability = request.form['type_of_disability']

                print("I am breaking before the if condition")
                if all(value is None for value in existing_record.values()):
                    # Save the form data to the database
                    print('I am breaking while insertion')
                    print('Inserting new record for:' + email)
                    if view_mode == 'edit':
                        cursor.execute(
                            "UPDATE application_page SET domicile = %s, domicile_certificate = %s, domicile_number = %s, "
                            "caste_certf = %s, issuing_district = %s, caste_issuing_authority = %s, salaried = %s, "
                            "disability = %s, type_of_disability = %s ,"
                            "caste_certf_number = %s, validity_certificate = %s,validity_cert_number = %s, validity_issuing_district =%s,validity_issuing_authority =%s  WHERE email = %s",
                            (domicile, domicile_certificate, domicile_number, caste_certf, issuing_district,
                             caste_issuing_authority, salaried, disability, type_of_disability, caste_cert_number,
                             validity_certificate, validity_num, validity_issuing_district, validity_issuing_authority,
                             email))
                        cnx.commit()
                        # cursor.execute("SELECT domicile, domicile_certificate, domicile_number, "
                        #                "caste_certf, issuing_district, caste_issuing_authority, salaried, disability,"
                        #                " type_of_disability FROM application_page WHERE email = %s", (email,))
                        # existing_record = cursor.fetchone()
                        # if existing_record:
                        #     return redirect(url_for('section4'))
                return redirect(url_for('section4.section4'))
            # Select records again to verify the insertion
            cursor.execute("SELECT domicile, domicile_certificate, domicile_number, caste_certf, issuing_district, "
                           "caste_issuing_authority, salaried, disability, type_of_disability, caste_certf_number,validity_certificate, validity_cert_number, validity_issuing_district, validity_issuing_authority  "
                           "FROM application_page WHERE email = %s", (email,))
            existing_record = cursor.fetchone()
            print(existing_record)
        return render_template('Candidate/NewUser/ApplicationForm/AForm_section3.html', existing_record=existing_record, view_mode=view_mode)