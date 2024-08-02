import os
from datetime import datetime, timedelta, date
import mysql.connector
from classes.connection import HostConfig, ConfigPaths
from flask import Blueprint, render_template, session, request, redirect, url_for
# Middleware import
from authentication.middleware import auth
from classes.university import universityController

section5_blueprint = Blueprint('section5', __name__)


def section5_auth(app):
    # ------ HOST Configs are in classes/connection.py
    host = HostConfig.host
    app_paths = ConfigPaths.paths.get(host)
    if app_paths:
        for key, value in app_paths.items():
            app.config[key] = value

    @section5_blueprint.route('/section5', methods=['GET', 'POST'])
    def section5():
        email = session['email']
        print('I am in section 5:' + email)
        cnx = mysql.connector.connect(user='root', password='A9CALcsd7lc%7ac',
                                      host=host,
                                      database='ICSApplication')
        cursor = cnx.cursor(dictionary=True)

        # Check if a record already exists for this user
        cursor.execute("SELECT first_name, last_name, documentfile1, documentfile2, documentfile3, documentfile4, "
                       "documentfile5, documentfile6, documentfile7, documentfile8, signature, documentfile9, documentfile10,"
                       " documentfile11, documentfile12, documentfile13, documentfile14, documentfile15, documentfile16,"
                       "documentfile17, documentfile18, documentfile19, documentfile20, documentfile21, documentfile22,"
                       "documentfile23, documentfile24, documentfile25, documentfile26  FROM application_page WHERE email = %s",
                       (email,))
        existing_record = cursor.fetchone()
        print("existing_record", existing_record)

        if request.method == 'POST':

            cursor.execute("SELECT phd_registration_year, id FROM application_page WHERE email = %s", (email,))
            row = cursor.fetchone()
            unique_id = row['id']
            year = row['phd_registration_year']
            applicant_id = 'TRTI' + '/' + str(year) + '/' + str(unique_id)
            # Get current date
            current_date = datetime.now().strftime('%Y-%m-%d')
            # Get current time
            current_time = datetime.now().strftime('%H:%M:%S')
            print('Got Post request:')
            first_name = existing_record['first_name']
            last_name = existing_record['last_name']
            # Process the form data and files
            document1 = applicant_pdf_upload_section_five(request.files['documentfile1'], first_name, last_name)
            document2 = applicant_pdf_upload_section_five(request.files['documentfile2'], first_name, last_name)
            document3 = applicant_pdf_upload_section_five(request.files['documentfile3'], first_name, last_name)
            document4 = applicant_pdf_upload_section_five(request.files['documentfile4'], first_name, last_name)
            document5 = applicant_pdf_upload_section_five(request.files['documentfile5'], first_name, last_name)
            document6 = applicant_pdf_upload_section_five(request.files['documentfile6'], first_name, last_name)
            document7 = applicant_pdf_upload_section_five(request.files['documentfile7'], first_name, last_name)
            document8 = applicant_pdf_upload_section_five(request.files['documentfile8'], first_name, last_name)
            signature = applicant_pdf_upload_section_five(request.files['signature'], first_name, last_name)
            document9 = applicant_pdf_upload_section_five(request.files['documentfile9'], first_name, last_name)
            document10 = applicant_pdf_upload_section_five(request.files['documentfile10'], first_name, last_name)
            document11 = applicant_pdf_upload_section_five(request.files['documentfile11'], first_name, last_name)
            document12 = applicant_pdf_upload_section_five(request.files['documentfile12'], first_name, last_name)
            document13 = applicant_pdf_upload_section_five(request.files['documentfile13'], first_name, last_name)
            document14 = applicant_pdf_upload_section_five(request.files['documentfile14'], first_name, last_name)
            document15 = applicant_pdf_upload_section_five(request.files['documentfile15'], first_name, last_name)
            document16 = applicant_pdf_upload_section_five(request.files['documentfile16'], first_name, last_name)
            document17 = applicant_pdf_upload_section_five(request.files['documentfile17'], first_name, last_name)
            document18 = applicant_pdf_upload_section_five(request.files['documentfile18'], first_name, last_name)
            document19 = applicant_pdf_upload_section_five(request.files['documentfile19'], first_name, last_name)
            document20 = applicant_pdf_upload_section_five(request.files['documentfile20'], first_name, last_name)
            document21 = applicant_pdf_upload_section_five(request.files['documentfile21'], first_name, last_name)
            document22 = applicant_pdf_upload_section_five(request.files['documentfile22'], first_name, last_name)
            document23 = applicant_pdf_upload_section_five(request.files['documentfile23'], first_name, last_name)
            document24 = applicant_pdf_upload_section_five(request.files['documentfile24'], first_name, last_name)
            # document25 = applicant_pdf_upload_section_five(request.files['documentfile25'], first_name, last_name)
            document26 = applicant_pdf_upload_section_five(request.files['documentfile26'], first_name, last_name)
        else:
            document1 = ''
            document2 = ''
            document3 = ''
            document4 = ''
            document5 = ''
            document6 = ''
            document7 = ''
            document8 = ''
            signature = ''
            document9 = ''
            document10 = ''
            document11 = ''
            document12 = ''
            document13 = ''
            document14 = ''
            document15 = ''
            document16 = ''
            document17 = ''
            document18 = ''
            document19 = ''
            document20 = ''
            document21 = ''
            document22 = ''
            document23 = ''
            document24 = ''
            # document25 = ''
            document26 = ''

        # Check if any of the documents have been uploaded
        if any(doc for doc in
               [document1, document2, document3, document4, document5, document6, document7, document8, signature,
                document9,
                document10, document11, document12, document13, document14, document15, document16, document17,
                document18,
                document19, document20, document21, document22, document23, document24, document26]):
            # If any document is uploaded, update or insert into the database
            if all(value is None for value in existing_record.values()):
                print('In the second loop updating the documents')
                # Insert new records
                print('Inserting new record for:' + email)
                cursor.execute(
                    "UPDATE application_page SET documentfile1 = %s, documentfile2 = %s, documentfile3 = %s, documentfile4 = %s, "
                    "documentfile5 = %s, documentfile6 = %s, documentfile7 = %s, documentfile8 = %s, signature = %s, documentfile9 = %s, "
                    "documentfile10 = %s, documentfile11 = %s, documentfile12 = %s, documentfile13 = %s, documentfile14 = %s,"
                    "documentfile15 = %s, documentfile16 = %s, documentfile17 = %s, documentfile18 = %s, documentfile19 = %s, "
                    "documentfile20 = %s, documentfile21 = %s, documentfile22 = %s, documentfile23 = %s, documentfile24 = %s,"
                    "documentfile26 = %s WHERE email = %s",
                    (document1, document2, document3, document4, document5, document6, document7, document8, signature,
                     document9,
                     document10, document11, document12, document13, document14, document15, document16, document17,
                     document18, document19, document20, document21, document22, document23, document24, document26,
                     email))
                cnx.commit()
            else:
                # Update existing records
                print('Updating records for:' + email)
                cursor.execute(
                    "UPDATE application_page SET applicant_id = %s, form_filled = 1, documentfile1 = %s, documentfile2 = %s, documentfile3 = %s, documentfile4 = %s, "
                    "documentfile5 = %s, documentfile6 = %s, documentfile7 = %s, documentfile8 = %s, signature = %s, documentfile9 = %s,"
                    "documentfile10 = %s, documentfile11 = %s, documentfile12 = %s, documentfile13 = %s, documentfile14 = %s,"
                    "documentfile15 = %s, documentfile16 = %s, documentfile17 = %s, documentfile18 = %s, documentfile19 = %s, "
                    "documentfile20 = %s, documentfile21 = %s, documentfile22 = %s, documentfile23 = %s,  documentfile24 = %s,"
                    " documentfile26 = %s, application_date = %s, application_time =%s WHERE email = %s",
                    (applicant_id, document1, document2, document3, document4, document5, document6, document7,
                     document8, signature, document9,
                     document10, document11, document12, document13, document14, document15, document16, document17,
                     document18, document19, document20, document21, document22, document23, document24, document26,
                     current_date, current_time, email))
                cnx.commit()
            cursor.execute("SELECT * FROM application_page WHERE email = %s", (email,))
            records = cursor.fetchone()

            return render_template('Candidate/NewUser/ApplicationForm/submit_form.html', records=records)
        else:
            # Handle case where no files were uploaded
            # You can add appropriate logic here (e.g., show an error message)
            print('No files were uploaded')

        cursor.execute("SELECT have_you_qualified FROM application_page WHERE email = %s", (email,))
        mphil_selected = cursor.fetchone()

        return render_template('Candidate/NewUser/ApplicationForm/AForm_section5.html', existing_record=existing_record, mphil_selected=mphil_selected)

    def applicant_pdf_upload_section_five(file, firstname, lastname):
        if file:
            filename = f"{firstname}_{lastname}_{file.filename}"
            file.save(os.path.join(app.config['USER_DOC_SEC_FIVE'], filename))
            # return os.path.join(app.config['USER_DOC_SEC_FIVE'], filename)
            return '/static/uploads/user_doc_secfive/' + filename
        else:
            return "Save File"