from Classes.database import HostConfig, ConfigPaths, ConnectParam
from flask import Blueprint, render_template, session, request, redirect, url_for, flash, Response
from PythonFiles.AdminPages.PDFfile import *


fellowship_awarded_blueprint = Blueprint('fellowship_awarded', __name__)


def fellowship_awarded_auth(app):
    # ------ HOST Configs are in classes/connection.py
    host = HostConfig.host
    app_paths = ConfigPaths.paths.get(host)
    if app_paths:
        for key, value in app_paths.items():
            app.config[key] = value

    @fellowship_awarded_blueprint.route('/fellowship_awarded', methods=['GET', 'POST'])
    def fellowship_awarded():
        if not session.get('logged_in'):
            # Redirect to the admin login page if the user is not logged in
            return redirect(url_for('adminlogin.admin_login'))

        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)

        sql = """ 

                    SELECT * 
                    FROM application_page 
                    WHERE final_approval = 'accepted' 
                      AND phd_registration_year >= '2023'

                    UNION

                    SELECT * 
                    FROM application_page 
                    WHERE phd_registration_year > '2020' 
                      AND aadesh = 1; 

            """
        cursor.execute(sql)
        result = cursor.fetchall()
        # print(result)
        cursor.close()
        cnx.close()
        return render_template('AdminPages/fellowship_awarded.html', result=result)

    @fellowship_awarded_blueprint.route('/generate_pdf_application/<string:email>', methods=['GET', 'POST'])
    def generate_pdf_application(email):
        # email = session['email']
        output_filename = app.config['PDF_STORAGE_PATH']
        # output_filename = '/static/pdf_application_form/pdfform.pdf'

        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)

        cursor.execute(" SELECT * FROM signup WHERE year IN ('2020', '2021', '2022') and email = %s ", (email,))
        output = cursor.fetchall()

        if output:
            cursor.execute(
                "SELECT * FROM application_page WHERE email = %s", (email,))
            old_user_data = cursor.fetchone()
            print(old_user_data)
            # Generate a styled PDF
            print(output_filename)
            generate_pdf_with_styling(old_user_data, output_filename)
        else:
            cursor.execute("SELECT * FROM application_page WHERE email = %s", (email,))
            data = cursor.fetchone()
            print(data)
            # Generate a styled PDF
            generate_pdf_with_styling(data, output_filename)

        # Serve the generated PDF as a response
        with open(output_filename, "rb") as pdf_file:
            response = Response(pdf_file.read(), content_type="application/pdf")
            response.headers['Content-Disposition'] = 'inline; filename=pdfform.pdf'

        return response

    @fellowship_awarded_blueprint.route('/generate_award_letter_AA/<string:email>')
    def generate_award_letter_AA(email):
        try:
            # email = session['email']
            output_filename = '/static/pdf_application_form/award_letter.pdf'
            # output_filename = '/static/pdf_application_form/award_letter.pdf'

            host = HostConfig.host
            connect_param = ConnectParam(host)
            cnx, cursor = connect_param.connect(use_dict=True)

            cursor.execute(
                "SELECT id, applicant_photo, applicant_id, adhaar_number, first_name, last_name, middle_name, mobile_number,"
                " email, date_of_birth, gender, age, caste, your_caste, marital_status, dependents, state, district,"
                " taluka, village, city, add_1, add_2, pincode, ssc_passing_year,"
                " ssc_percentage, ssc_school_name, hsc_passing_year, hsc_percentage, hsc_school_name,"
                " graduation_passing_year, graduation_percentage, graduation_school_name, phd_passing_year,"
                " phd_percentage, phd_school_name,have_you_qualified, name_of_college, name_of_guide, topic_of_phd,"
                " concerned_university, faculty, phd_registration_date, phd_registration_year,"
                " family_annual_income, "
                " income_certificate_number, issuing_authority, domicile, domicile_certificate, domicile_number,"
                " caste_certf, issuing_district, caste_issuing_authority, salaried, disability, type_of_disability,"
                " father_name, mother_name, work_in_government, bank_name, account_number, ifsc_code,"
                " account_holder_name, application_date FROM application_page WHERE email = %s", (email,))
            data = cursor.fetchone()

            cursor.execute(
                "SELECT id, phd_registration_year FROM application_page WHERE email = %s",
                (email,))
            result = cursor.fetchone()
            year = result['phd_registration_year']
            id = result['id']

            if (year >= 2023):
                generate_award_letter_2023(data, output_filename)
            else:
                generate_award_letter_2022(data, output_filename)

            # Serve the generated PDF as a response
            with open(output_filename, "rb") as pdf_file:
                response = Response(pdf_file.read(), content_type="application/pdf")
                response.headers['Content-Disposition'] = 'inline; filename=award_letter.pdf'
        except BrokenPipeError:
            # Handle broken pipe error, e.g., log it
            pass

        return response



