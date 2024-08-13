from datetime import datetime, date
import mysql.connector
import requests
import os
from classes.connection import HostConfig, ConfigPaths
from flask import Blueprint, render_template, session, request, jsonify, flash

old_user_blueprint = Blueprint('old_user', __name__)


def old_user_auth(app):
    # ------ HOST Configs are in classes/connection.py
    host = HostConfig.host
    app_paths = ConfigPaths.paths.get(host)
    if app_paths:
        for key, value in app_paths.items():
            app.config[key] = value

    def university_college():
        email = session['email']
        cnx = mysql.connector.connect(user='icswebapp', password='A9CALcsd7lc%7ac',
                                      host=host,
                                      database='ICSApplication')
        cursor = cnx.cursor(dictionary=True)
        # concerned_university = request.form['concerned_university']
        cursor.execute("SELECT DISTINCT id, u_id, affiliated_universities FROM universities GROUP BY u_id")
        data = cursor.fetchall()
        # print("Data :", data)
        return data

    @old_user_blueprint.route('/submit_form', methods=['GET', 'POST'])
    def submit_form():
        print('I am in application form submit route')
        email = session['email']
        cnx = mysql.connector.connect(user='root', password='A9CALcsd7lc%7ac',
                                      host=host,
                                      database='ICSApplication')
        cursor = cnx.cursor(dictionary=True)

        records = None

        if request.method == 'POST':
            print('Got the POST request')
            today = date.today()
            now = datetime.now()
            dt_string = now.strftime("%d%m%Y%H%M%S")

            # Folder Set
            applicant_photo = request.files['applicant_photo']
            adhaar_number = request.form['adhaar_number']
            adhaar_seeding = request.form['adhaar_seeding']
            first_name = request.form['first_name']
            middle_name = request.form['middle_name']
            last_name = request.form['last_name']
            mobile_number = request.form['mobile_number']
            email = request.form['email']
            date_of_birth = request.form['date_of_birth']
            gender = request.form['gender']
            age = request.form['age']
            marital_status = request.form['marital_status']
            add_1 = request.form['add_1']
            add_2 = request.form['add_2']
            pincode = request.form['pincode']
            village = request.form['village']
            taluka = request.form['taluka']
            city = request.form['city']
            district = request.form['district']
            state = request.form['state']
            ssc_passing_year = request.form['ssc_passing_year']
            ssc_percentage = request.form['ssc_percentage']
            ssc_school_name = request.form['ssc_school_name']
            hsc_passing_year = request.form['hsc_passing_year']
            hsc_percentage = request.form['hsc_percentage']
            hsc_school_name = request.form['hsc_school_name']
            graduation_passing_year = request.form['graduation_passing_year']
            graduation_percentage = request.form['graduation_percentage']
            graduation_school_name = request.form['graduation_school_name']
            phd_passing_year = request.form["phd_passing_year"]
            phd_percentage = request.form["phd_percentage"]
            phd_school_name = request.form["phd_school_name"]
            phd_registration_date = request.form['phd_registration_date']
            phd_registration_year = request.form['phd_registration_year']
            concerned_university = request.form['concerned_university']
            name_of_college = request.form.get('selected_college')
            other_college_name = request.form['other_college_name']
            department_name = request.form['department_name']
            topic_of_phd = request.form['topic_of_phd']
            name_of_guide = request.form['name_of_guide']
            faculty = request.form['faculty']
            salaried = request.form['salaried']
            disability = request.form['disability']
            family_annual_income = request.form['family_annual_income']
            income_certificate_number = request.form['income_certificate_number']
            issuing_authority = request.form['issuing_authority']
            domicile = request.form.get('domicile')
            domicile_certificate = request.form.get('domicile_certificate')
            domicile_number = request.form['domicile_number']
            validity_certificate = request.form['validity_certificate']
            validity_cert_number = request.form['validity_cert_number']
            caste_certf = request.form.get('caste_certf')
            caste_certf_number = request.form['caste_certf_number']
            caste = request.form['caste']
            your_caste = request.form['your_caste']
            issuing_district = request.form['issuing_district']
            caste_issuing_authority = request.form['caste_issuing_authority']
            father_name = request.form['father_name']
            mother_name = request.form['mother_name']
            bank_name = request.form['bank_name']
            account_number = request.form['account_number']
            ifsc_code = request.form['ifsc_code']
            account_holder_name = request.form['account_holder_name']
            signature = request.files['signature']
            print(signature)
            documentfile1 = request.files['documentfile1']
            documentfile2 = request.files['documentfile2']
            documentfile3 = request.files['documentfile3']
            documentfile4 = request.files['documentfile4']
            documentfile5 = request.files['documentfile5']
            documentfile6 = request.files['documentfile6']
            documentfile7 = request.files['documentfile7']
            documentfile8 = request.files['documentfile8']
            documentfile9 = request.files['documentfile9']
            documentfile10 = request.files['documentfile10']

            # Save files
            if signature.filename != '':
                signature_path = save_applicant_photo(signature, first_name, last_name)
            else:
                signature_path = request.form['signature_photo']

            if applicant_photo.filename != '':
                photo_path = save_applicant_photo(applicant_photo, first_name, last_name)
            else:
                photo_path = request.form['user_photo']

            if documentfile1.filename != '':
                documentfile1_path = applicant_pdf_upload_section_five(documentfile1, first_name, last_name)
            else:
                documentfile1_path = request.form['file1']

            if documentfile2.filename != '':
                documentfile2_path = applicant_pdf_upload_section_five(documentfile2, first_name, last_name)
            else:
                documentfile2_path = request.form['file2']

            if documentfile3.filename != '':
                documentfile3_path = applicant_pdf_upload_section_five(documentfile3, first_name, last_name)
            else:
                documentfile3_path = request.form['file3']

            if documentfile4.filename != '':
                documentfile4_path = applicant_pdf_upload_section_five(documentfile4, first_name, last_name)
            else:
                documentfile4_path = request.form['file4']

            if documentfile5.filename != '':
                documentfile5_path = applicant_pdf_upload_section_five(documentfile5, first_name, last_name)
            else:
                documentfile5_path = request.form['file5']

            if documentfile6.filename != '':
                documentfile6_path = applicant_pdf_upload_section_five(documentfile6, first_name, last_name)
            else:
                documentfile6_path = request.form['file6']

            if documentfile7.filename != '':
                documentfile7_path = applicant_pdf_upload_section_five(documentfile7, first_name, last_name)
            else:
                documentfile7_path = request.form['file7']

            if documentfile8.filename != '':
                documentfile8_path = applicant_pdf_upload_section_five(documentfile8, first_name, last_name)
            else:
                documentfile8_path = request.form['file8']

            if documentfile9.filename != '':
                documentfile9_path = applicant_pdf_upload_section_five(documentfile9, first_name, last_name)
            else:
                documentfile9_path = request.form['file9']

            if documentfile10.filename != '':
                documentfile10_path = applicant_pdf_upload_section_five(documentfile10, first_name, last_name)
            else:
                documentfile10_path = request.form['file10']

            print('Got all the request. fields')

            cursor.execute("SELECT phd_registration_year, id FROM application_page WHERE email = %s", (email,))
            result = cursor.fetchone()

            cursor.execute("SELECT phd_registration_year, id FROM old_users WHERE email = %s", (email,))
            record = cursor.fetchone()
            print("Record", record)

            if result:
                print('I am in result')
                phd_registration_year = result['phd_registration_year']
                id = result['id']
                datatime_now = datetime.now()
                applicant_id = f"TRTI/{phd_registration_year}/{id}"

                print(signature_path)

                update_data = {
                    "applicant_id": applicant_id,
                    "form_filled": 1,
                    "application_date": datetime.now(),
                    "applicant_photo": photo_path,
                    "adhaar_number": adhaar_number,
                    "adhaar_seeding": adhaar_seeding,
                    "first_name": first_name,
                    "middle_name": middle_name,
                    "last_name": last_name,
                    "mobile_number": mobile_number,
                    "date_of_birth": date_of_birth,
                    "gender": gender,
                    "age": age,
                    "marital_status": marital_status,
                    "add_1": add_1,
                    "add_2": add_2,
                    "pincode": pincode,
                    "village": village,
                    "city": city,
                    "taluka": taluka,
                    "district": district,
                    "state": state,
                    "ssc_passing_year": ssc_passing_year,
                    "ssc_percentage": ssc_percentage,
                    "ssc_school_name": ssc_school_name,
                    "hsc_passing_year": hsc_passing_year,
                    "hsc_percentage": hsc_percentage,
                    "hsc_school_name": hsc_school_name,
                    "graduation_passing_year": graduation_passing_year,
                    "graduation_percentage": graduation_percentage,
                    "graduation_school_name": graduation_school_name,
                    "phd_passing_year": phd_passing_year,
                    "phd_percentage": phd_percentage,
                    "phd_school_name": phd_school_name,
                    "phd_registration_date": phd_registration_date,
                    "phd_registration_year": phd_registration_year,
                    "concerned_university": concerned_university,
                    "name_of_college": name_of_college,
                    "other_college_name": other_college_name,
                    "department_name": department_name,
                    "topic_of_phd": topic_of_phd,
                    "name_of_guide": name_of_guide,
                    "faculty": faculty,
                    "salaried": salaried,
                    "disability": disability,
                    "family_annual_income": family_annual_income,
                    "income_certificate_number": income_certificate_number,
                    "issuing_authority": issuing_authority,
                    "domicile": domicile,
                    "domicile_certificate": domicile_certificate,
                    "domicile_number": domicile_number,
                    "validity_certificate": validity_certificate,
                    "validity_cert_number": validity_cert_number,
                    "caste_certf": caste_certf,
                    "caste_certf_number": caste_certf_number,
                    "caste": caste,
                    "your_caste": your_caste,
                    "issuing_district": issuing_district,
                    "caste_issuing_authority": caste_issuing_authority,
                    "father_name": father_name,
                    "mother_name": mother_name,
                    "bank_name": bank_name,
                    "account_number": account_number,
                    "ifsc_code": ifsc_code,
                    "account_holder_name": account_holder_name,
                    "signature": signature_path,
                    "documentfile1": documentfile1_path,
                    "documentfile2": documentfile2_path,
                    "documentfile3": documentfile3_path,
                    "documentfile4": documentfile4_path,
                    "documentfile5": documentfile5_path,
                    "documentfile6": documentfile6_path,
                    "documentfile7": documentfile7_path,
                    "documentfile8": documentfile8_path,
                    "documentfile9": documentfile9_path,
                    "documentfile10": documentfile10_path,
                    "email": email
                }
                if phd_registration_year is not None and phd_registration_year >= 2023:
                    update_database(update_data, phd_registration_year, cursor)
            elif record:
                print('I am in record')
                cursor.execute("INSERT INTO application_page (email) VALUES (%s)", (email,))
                cnx.commit()
                print('I have added the record email in application page')
                cursor.execute("UPDATE application_page SET status='accepted', scrutiny_status='accepted', "
                               "final_approval='accepted', joining_date=(SELECT phd_registration_date FROM old_users WHERE email=%s) WHERE email=%s ",
                               (email, email))
                cnx.commit()
                print('I have updated status and allt threee to accepted')
                cursor.execute("SELECT email FROM award_letter where email = %s", (email,))
                output = cursor.fetchall()
                print('Result of Award Letter', output)
                if email not in output:  # Check if the email is not already in the existing emails
                    cursor.execute("INSERT INTO award_letter (email) VALUES (%s) ", (email,))
                    cnx.commit()
                phd_registration_year = record['phd_registration_year']
                id = record['id']
                datatime_now = datetime.now()
                applicant_id = f"TRTI/{phd_registration_year}/{id}"

                update_data = {
                    "applicant_id": applicant_id,
                    "form_filled": 1,
                    "application_date": datetime.now(),
                    "applicant_photo": photo_path,
                    "adhaar_number": adhaar_number,
                    "adhaar_seeding": adhaar_seeding,
                    "first_name": first_name,
                    "middle_name": middle_name,
                    "last_name": last_name,
                    "mobile_number": mobile_number,
                    "date_of_birth": date_of_birth,
                    "gender": gender,
                    "age": age,
                    "marital_status": marital_status,
                    "add_1": add_1,
                    "add_2": add_2,
                    "pincode": pincode,
                    "village": village,
                    "city": city,
                    "taluka": taluka,
                    "district": district,
                    "state": state,
                    "ssc_passing_year": ssc_passing_year,
                    "ssc_percentage": ssc_percentage,
                    "ssc_school_name": ssc_school_name,
                    "hsc_passing_year": hsc_passing_year,
                    "hsc_percentage": hsc_percentage,
                    "hsc_school_name": hsc_school_name,
                    "graduation_passing_year": graduation_passing_year,
                    "graduation_percentage": graduation_percentage,
                    "graduation_school_name": graduation_school_name,
                    "phd_passing_year": phd_passing_year,
                    "phd_percentage": phd_percentage,
                    "phd_school_name": phd_school_name,
                    "phd_registration_date": phd_registration_date,
                    "phd_registration_year": phd_registration_year,
                    "concerned_university": concerned_university,
                    "name_of_college": name_of_college,
                    "other_college_name": other_college_name,
                    "department_name": department_name,
                    "topic_of_phd": topic_of_phd,
                    "name_of_guide": name_of_guide,
                    "faculty": faculty,
                    "salaried": salaried,
                    "disability": disability,
                    "family_annual_income": family_annual_income,
                    "income_certificate_number": income_certificate_number,
                    "issuing_authority": issuing_authority,
                    "domicile": domicile,
                    "domicile_certificate": domicile_certificate,
                    "domicile_number": domicile_number,
                    "validity_certificate": validity_certificate,
                    "validity_cert_number": validity_cert_number,
                    "caste_certf": caste_certf,
                    "caste_certf_number": caste_certf_number,
                    "caste": caste,
                    "your_caste": your_caste,
                    "issuing_district": issuing_district,
                    "caste_issuing_authority": caste_issuing_authority,
                    "father_name": father_name,
                    "mother_name": mother_name,
                    "bank_name": bank_name,
                    "account_number": account_number,
                    "ifsc_code": ifsc_code,
                    "account_holder_name": account_holder_name,
                    "signature": signature_path,
                    "documentfile1": documentfile1_path,
                    "documentfile2": documentfile2_path,
                    "documentfile3": documentfile3_path,
                    "documentfile4": documentfile4_path,
                    "documentfile5": documentfile5_path,
                    "documentfile6": documentfile6_path,
                    "documentfile7": documentfile7_path,
                    "documentfile8": documentfile8_path,
                    "documentfile9": documentfile9_path,
                    "documentfile10": documentfile10_path,
                    "email": email
                }

                if phd_registration_year in (2020, 2021, 2022):
                    # update_database_old_users(update_data, phd_registration_year, cursor)
                    update_database(update_data, phd_registration_year, cursor)
                cnx.commit()

                cursor.execute("SELECT form_filled='1' FROM old_users WHERE email = %s", (email,))
                records = cursor.fetchone()
                if records:
                    update_old_user_in_application_page(update_data, phd_registration_year, cursor)
                print('I have updated the data and commited it successfully')

                # Close the cursor and connection
                cursor.close()
                cnx.close()

            cnx = mysql.connector.connect(user='root', password='A9CALcsd7lc%7ac',
                                          host=host,
                                          database='ICSApplication')
            cursor = cnx.cursor(dictionary=True)
            cursor.execute("SELECT * FROM application_page WHERE email = %s", (email,))
            records = cursor.fetchone()
            cursor.close()
            cnx.close()

        return render_template('Candidate/NewUser/ApplicationForm/submit_form.html', records=records, email=email)

    def save_applicant_photo(file, firstname, lastname):
        if file:
            filename = f"{firstname}_{lastname}_{file.filename}"
            file.save(os.path.join(app.config['UPLOAD_PHOTO_SECTION1'], filename))
            # return os.path.join(app.config['UPLOAD_PHOTO_SECTION1'], filename)
            return '/static/uploads/image_retrive/' + filename
        else:
            return "Save File"

    def applicant_pdf_upload_section_five(file, firstname, lastname):
        if file:
            filename = f"{firstname}_{lastname}_{file.filename}"
            file.save(os.path.join(app.config['USER_DOC_SEC_FIVE'], filename))
            # return os.path.join(app.config['USER_DOC_SEC_FIVE'], filename)
            return '/static/uploads/user_doc_secfive/' + filename
        else:
            return "Save File"

    def update_database(data, phd_registration_year, cursor):
        try:
            with mysql.connector.connect(user='root', password='A9CALcsd7lc%7ac',
                                         host=host,
                                         database='ICSApplication') as cnx:
                with cnx.cursor(dictionary=True) as cursor:
                    print("phd_registration_year", phd_registration_year)
                    # Using the update_data dictionary in the SQL query

                    # Build the SQL UPDATE statement
                    update_query = f"""
                                UPDATE application_page
                                SET 
                                form_filled = 1,
                                applicant_id = %(applicant_id)s,
                                application_date = %(application_date)s,
                                applicant_photo = %(applicant_photo)s,
                                adhaar_number = %(adhaar_number)s,
                                adhaar_seeding = %(adhaar_seeding)s,
                                first_name = %(first_name)s,
                                middle_name = %(middle_name)s,
                                last_name = %(last_name)s,
                                mobile_number = %(mobile_number)s,
                                date_of_birth = %(date_of_birth)s,
                                gender = %(gender)s,
                                age = %(age)s,
                                marital_status = %(marital_status)s,
                                add_1 = %(add_1)s,
                                add_2 = %(add_2)s,
                                pincode = %(pincode)s,
                                village = %(village)s,
                                city = %(city)s,
                                taluka = %(taluka)s,
                                district = %(district)s,
                                state = %(state)s,
                                ssc_passing_year = %(ssc_passing_year)s,
                                ssc_percentage = %(ssc_percentage)s,
                                ssc_school_name = %(ssc_school_name)s,
                                hsc_passing_year = %(hsc_passing_year)s,
                                hsc_percentage = %(hsc_percentage)s,
                                hsc_school_name = %(hsc_school_name)s,
                                graduation_passing_year = %(graduation_passing_year)s,
                                graduation_percentage = %(graduation_percentage)s,
                                graduation_school_name = %(graduation_school_name)s,
                                phd_passing_year = %(phd_passing_year)s,
                                phd_percentage = %(phd_percentage)s,
                                phd_school_name = %(phd_school_name)s,
                                phd_registration_date = %(phd_registration_date)s,
                                phd_registration_year = %(phd_registration_year)s,
                                concerned_university = %(concerned_university)s,
                                name_of_college = %(name_of_college)s,
                                other_college_name = %(other_college_name)s,
                                department_name = %(department_name)s,
                                topic_of_phd = %(topic_of_phd)s,
                                name_of_guide = %(name_of_guide)s,
                                faculty = %(faculty)s,
                                salaried = %(salaried)s,
                                disability = %(disability)s,
                                family_annual_income = %(family_annual_income)s,
                                income_certificate_number = %(income_certificate_number)s,
                                issuing_authority = %(issuing_authority)s,
                                domicile = %(domicile)s,
                                domicile_certificate = %(domicile_certificate)s,
                                domicile_number = %(domicile_number)s,
                                validity_certificate = %(validity_certificate)s,
                                validity_cert_number = %(validity_cert_number)s,
                                caste_certf = %(caste_certf)s,
                                caste_certf_number = %(caste_certf_number)s,
                                caste = %(caste)s,
                                your_caste = %(your_caste)s,
                                issuing_district = %(issuing_district)s,
                                caste_issuing_authority = %(caste_issuing_authority)s,
                                father_name = %(father_name)s,
                                mother_name = %(mother_name)s,
                                bank_name = %(bank_name)s,
                                account_number = %(account_number)s,
                                ifsc_code = %(ifsc_code)s,
                                account_holder_name = %(account_holder_name)s,
                                signature = %(signature)s,
                                documentfile1 = %(documentfile1)s,
                                documentfile2 = %(documentfile2)s,
                                documentfile3 = %(documentfile3)s,
                                documentfile4 = %(documentfile4)s,
                                documentfile5 = %(documentfile5)s,
                                documentfile6 = %(documentfile6)s,
                                documentfile7 = %(documentfile7)s,
                                documentfile8 = %(documentfile8)s,
                                documentfile9 = %(documentfile9)s,
                                documentfile10 = %(documentfile10)s
                                WHERE email = %(email)s
                            """
                    print('update_query' + update_query)
                    # Execute the UPDATE statement with data
                    cursor.execute(update_query, data)
                    cnx.commit()
                    print(f"Rows affected: {cursor.rowcount}")
        except mysql.connector.Error as e:
            # Handle the exception, rollback if necessary
            print(f"Error: {e}")

    def update_old_user_in_application_page(data, phd_registration_year, cursor):
        try:
            with mysql.connector.connect(user='root', password='A9CALcsd7lc%7ac',
                                         host=host,
                                         database='ICSApplication') as cnx:
                with cnx.cursor(dictionary=True) as cursor:
                    print("phd_registration_year", phd_registration_year)
                    # Using the update_data dictionary in the SQL query

                    # Build the SQL UPDATE statement
                    update_query = f"""
                                UPDATE old_users
                                SET 
                                form_filled = %(form_filled)s,
                                applicant_id = %(applicant_id)s,
                                application_date = %(application_date)s,
                                applicant_photo = %(applicant_photo)s,
                                adhaar_number = %(adhaar_number)s,
                                first_name = %(first_name)s,
                                middle_name = %(middle_name)s,
                                last_name = %(last_name)s,
                                mobile_number = %(mobile_number)s,
                                date_of_birth = %(date_of_birth)s,
                                gender = %(gender)s,
                                age = %(age)s,
                                marital_status = %(marital_status)s,
                                add_1 = %(add_1)s,
                                add_2 = %(add_2)s,
                                pincode = %(pincode)s,
                                village = %(village)s,
                                city = %(city)s,
                                taluka = %(taluka)s,
                                district = %(district)s,
                                state = %(state)s,
                                ssc_passing_year = %(ssc_passing_year)s,
                                ssc_percentage = %(ssc_percentage)s,
                                ssc_school_name = %(ssc_school_name)s,
                                hsc_passing_year = %(hsc_passing_year)s,
                                hsc_percentage = %(hsc_percentage)s,
                                hsc_school_name = %(hsc_school_name)s,
                                graduation_passing_year = %(graduation_passing_year)s,
                                graduation_percentage = %(graduation_percentage)s,
                                graduation_school_name = %(graduation_school_name)s,
                                phd_passing_year = %(phd_passing_year)s,
                                phd_percentage = %(phd_percentage)s,
                                phd_school_name = %(phd_school_name)s,
                                phd_registration_date = %(phd_registration_date)s,
                                phd_registration_year = %(phd_registration_year)s,
                                concerned_university = %(concerned_university)s,
                                name_of_college = %(name_of_college)s,
                                department_name = %(department_name)s,
                                topic_of_phd = %(topic_of_phd)s,
                                name_of_guide = %(name_of_guide)s,
                                faculty = %(faculty)s,
                                salaried = %(salaried)s,
                                disability = %(disability)s,
                                family_annual_income = %(family_annual_income)s,
                                income_certificate_number = %(income_certificate_number)s,
                                issuing_authority = %(issuing_authority)s,
                                domicile = %(domicile)s,
                                domicile_certificate = %(domicile_certificate)s,
                                domicile_number = %(domicile_number)s,
                                caste_certf = %(caste_certf)s,
                                issuing_district = %(issuing_district)s,
                                caste_issuing_authority = %(caste_issuing_authority)s,
                                father_name = %(father_name)s,
                                mother_name = %(mother_name)s,
                                bank_name = %(bank_name)s,
                                account_number = %(account_number)s,
                                ifsc_code = %(ifsc_code)s,
                                account_holder_name = %(account_holder_name)s,
                                signature = %(signature)s,
                                documentfile1 = %(documentfile1)s,
                                documentfile2 = %(documentfile2)s,
                                documentfile3 = %(documentfile3)s,
                                documentfile4 = %(documentfile4)s,
                                documentfile5 = %(documentfile5)s,
                                documentfile6 = %(documentfile6)s,
                                documentfile7 = %(documentfile7)s,
                                documentfile8 = %(documentfile8)s,
                                documentfile9 = %(documentfile9)s,
                                documentfile10 = %(documentfile10)s
                                WHERE email = %(email)s
                            """
                    print('update_old_user_in_application_page', update_query)
                    # Execute the UPDATE statement with data
                    cursor.execute(update_query, data)
                    cnx.commit()
                    print(f"Rows affected: {cursor.rowcount}")
        except mysql.connector.Error as e:
            # Handle the exception, rollback if necessary
            print(f"Error: {e}")

    @old_user_blueprint.route('/get_colleges', methods=['POST'])
    def get_colleges():
        selected_university = request.form['selected_university']
        cnx = mysql.connector.connect(user='icswebapp', password='A9CALcsd7lc%7ac',
                                      host=host,
                                      database='ICSApplication')
        cursor = cnx.cursor(dictionary=True)
        # Fetch the colleges for the selected university ID
        cursor.execute("SELECT id, college_name FROM universities WHERE u_id = %s", (selected_university,))
        colleges = cursor.fetchall()
        return jsonify(colleges)

    @old_user_blueprint.route('/old_user_preview', methods=['GET', 'POST'])
    def old_user_preview():
        if session.pop('logged_in_from_login', None):
            flash('Logged in Successfully', 'success')
        email = session['email']
        cnx = mysql.connector.connect(user='icswebapp', password='A9CALcsd7lc%7ac',
                                      host=host,
                                      database='ICSApplication')
        cursor = cnx.cursor(dictionary=True)
        # Check if the user's email is in old_users for 2021 or 2022
        cursor.execute("SELECT year FROM signup WHERE email = %s AND year IN ('2020', '2021', '2022')", (email,))
        old_user = cursor.fetchone()
        concerned_university = request.get_data('concerned_university')
        cursor.execute("SELECT college_name FROM universities WHERE affiliated_universities = %s ",
                       (concerned_university,))
        data_college = cursor.fetchone()
        cursor.execute('SELECT * FROM districts')
        district_list = cursor.fetchall()
        if old_user:
            session['user_type'] = 'old_user'
            university_data = university_college()
            cursor.execute("SELECT * FROM old_users WHERE email = %s", (email,))
            old_user_data = cursor.fetchone()
            # User exists in old_users for 2021 or 2022, use this data
            return render_template('Candidate/OldUser/old_user_preview.html', records=old_user_data, editable=True,
                                   university_data=university_data, data_college=data_college,
                                   district_list=district_list)
        else:
            session['user_type'] = 'new_user'
            # User does not exist in old_users for 2021 or 2022, fetch from application_page
            cursor.execute("SELECT * FROM application_page WHERE email = %s", (email,))
            application_page_data = cursor.fetchone()
            university_data = university_college()
            return render_template('Candidate/OldUser/old_user_preview.html', records=application_page_data, editable=True,
                                   university_data=university_data, data_college=data_college,
                                   district_list=district_list)
        cursor.close()
        cnx.close()
        return render_template('Candidate/OldUser/old_user_preview.html', records=records, editable=True, adhaar_error=adhaar_error)

    # Get address details using pincode
    @old_user_blueprint.route('/get_pincode_data', methods=['GET'])
    def get_pincode_data():
        pincode_data = request.args.get('pincode')
        api_url = f'https://api.worldpostallocations.com/pincode?postalcode={pincode_data}&countrycode=IN'
        try:
            response = requests.get(api_url)
            response.raise_for_status()  # Raise an exception for bad responses (4xx or 5xx)
            data = response.json()
            return jsonify(data)
        except requests.exceptions.RequestException as e:
            return jsonify({'error': str(e)}), 500

    @old_user_blueprint.route('/get_ifsc_data', methods=['GET'])
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