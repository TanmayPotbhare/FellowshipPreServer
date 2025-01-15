from datetime import datetime
import requests
import os
from fpdf import FPDF
from Classes.caste import casteController
from Classes.database import HostConfig, ConfigPaths, ConnectParam
from flask import Blueprint, render_template, session, request, redirect, url_for, flash, make_response, jsonify, \
    Response

app_pdf_blueprint = Blueprint('app_pdf', __name__)


def app_pdf_auth(app):
    # ------ HOST Configs are in classes/connection.py
    host = HostConfig.host
    app_paths = ConfigPaths.paths.get(host)
    if app_paths:
        for key, value in app_paths.items():
            app.config[key] = value

    @app_pdf_blueprint.route('/generate_pdf', methods=['GET', 'POST'])
    def generate_pdf():
        email = session['email']
        output_filename = app.config['PDF_STORAGE_PATH']
        # output_filename = 'static/pdf_application_form/pdfform.pdf'

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
            response.headers['Content-Disposition'] = 'inline; filename=Application Form.pdf'

        return response

    def generate_pdf_with_styling(data, filename):
        class PDF(FPDF):
            header_added = False  # To track whether the header is added to the first page

            def header(self):
                if not self.header_added:
                    # /
                    self.set_font("Arial", "B", 12)
                    self.cell(0, 10, "Fellowship ", align="C",
                              ln=True)  # Add space by changing the second parameter (e.g., 20)
                    # Insert an image (symbol) at the center of the header
                    # self.image('static/Images/trti.jpeg', 10, 10, 20)
                    self.image('/var/www/fellowship/fellowship/FellowshipPreServer/static/Images/trti.jpeg', 10, 10, 20)
                    # Insert an image (symbol) at the right of the header
                    self.image('/var/www/fellowship/fellowship/FellowshipPreServer/static/Images/satya.png', 155, 10, 20)
                    # self.image('static/Images/satya.png', 155, 10, 20)
                    self.image('/var/www/fellowship/fellowship/FellowshipPreServer/static/Images/maharashtra_shasn.png', 175, 10, 20)
                    # self.image('static/Images/maharashtra_shasn.png', 175, 10, 20)
                    self.cell(0, 10, "Tribal Research & Training Institute, Pune ", align="C", ln=True)
                    self.cell(0, 1, "Government of Maharashtra ", align="C", ln=True)
                    self.set_font("Arial", "B", size=8)
                    self.cell(0, 10,
                              "28, Queen's Garden, Bund Garden Rd, near Old Circuit House, Camp, Pune, Maharashtra 411001 ",
                              align="C", ln=True)
                    self.set_font("Arial", "B", 13)
                    self.cell(0, 10,
                              " Fellowship Application Form 2023 - 2024",
                              align="C", ln=True)
                    self.ln(2)  # Adjust this value to control the space after the line
                    self.line(10, self.get_y(), 200, self.get_y())  # Draw a line from left (10) to right (200)
                    self.header_added = True  # Set to True after adding the header

            def image_and_date(self, data):
                # Date and Applicant ID Section
                self.set_font("Arial", "B", size=11)

                # Applicant ID
                applicant_id = "TRTI/" + str(data.get('phd_registration_year', 'XXXX')) + "/" + str(
                    data.get('id', 'XXXX'))
                self.cell(50, 10, "Applicant ID: " + applicant_id, ln=False)

                self.cell(80)

                # Full Name
                full_name = f"{data.get('first_name', '')} {data.get('middle_name', '')} {data.get('last_name', '')}"
                self.set_font("Arial", size=10)
                self.cell(0, 10, "Full Name: " + full_name, ln=True)

                # Submitted Date and Time
                if 'application_date' in data and 'application_time' in data:
                    self.cell(50, 10, "Submitted Date: " + str(data['application_date']), ln=True)
                    # self.cell(100)  # Add space
                    self.cell(50, 10, "Submitted Time: " + str(data['application_time']), ln=True)

                # Applicant Photo
                if 'applicant_photo' in data:
                    photo = '/var/www/fellowship/fellowship/FellowshipPreServer' + data['applicant_photo']
                    try:
                        # Insert the applicant photo (adjust coordinates and size as needed)
                        self.image(photo, 165, 65, 30, 35)  # X=165, Y=65, Width=30, Height=35
                        self.rect(165, 65, 30, 35)  # Draw a border around the photo
                    except RuntimeError:
                        print(f"Error loading image: {photo}")

                self.ln(10)  # Add space between this section and the next content

            def footer(self):
                # Add a footer
                self.set_y(-15)
                self.set_font("Arial", "B", 8)
                self.cell(0, 10, f" {self.page_no()} ", align="C")

                # Center-align the "TRTI" text
                self.cell(0, 10, " TRTI  |  Fellowship | 2023 - 2024 ", align="R")

        personal_details = {
            "Adhaar Number": data['adhaar_number'],
            "First Name": data['first_name'],
            "Middle Name": data['middle_name'],
            "Last Name": data['last_name'],
            "Mobile Number": data['mobile_number'],
            "Email": data['email'],
            "Date of Birth": data['date_of_birth'],
            "Gender": data['gender'],
            "Age": data['age'],
            "Category": data['caste'],
            "Caste/Tribe ": data['your_caste'],
            "Sub Caste/Tribe": data['subcaste'],
            "Do you belong to PVTG?": data['pvtg'],
            "Which caste/tribe you belong in PVTG?": data['pvtg_caste']

            # Add more fields as needed
        }

        address_details = {
            "Main Address": data['add_1'],
            "Postal Address": data['add_2'],
            "Pincode": data['pincode'],
            "Village": data['village'],
            "Taluka": data['taluka'],
            "District": data['district'],
            "City": data['city'],
            "State": data['state']
        }

        # qualification_details = {
        # SSC
        ssc = {
            "SSC Passing Year": data['ssc_passing_year'],
            "SSC School Name": data['ssc_school_name'],
            "SSC Stream": data['ssc_stream'],
            "SSC Attempts": data['ssc_attempts'],
            "SSC Total Marks": data['ssc_total'],
            "SSC Percentage": data['ssc_percentage']
        }

        hsc = {
            "HSC Passing Year": data['hsc_passing_year'],
            "HSC School Name": data['hsc_school_name'],
            "HSC Stream": data['hsc_stream'],
            "HSC Attempts": data['hsc_attempts'],
            "HSC Total Marks": data['hsc_total'],
            "HSC Percentage": data['hsc_percentage']
        }

        grad = {
            "Graduation Passing Year": data['graduation_passing_year'],
            "Graduation College Name": data['graduation_school_name'],
            "Graduation Stream": data['grad_stream'],
            "Graduation Attempts": data['grad_attempts'],
            "Graduation Total Marks": data['grad_total'],
            "Graduation Percentage": data['graduation_percentage']
        }

        postgrad = {
            "Post Graduation Passing Year": data['phd_passing_year'],
            "Post Graduation College Name": data['phd_school_name'],
            "Post Graduation Stream": data['pg_stream'],
            "Post Graduation Attempts": data['pg_attempts'],
            "Post Graduation Total Marks": data['pg_total'],
            "Post Graduation Percentage": data['phd_percentage'],

            "What have you Qualified?": data['have_you_qualified']
            # Add more fields as needed
        }

        phd_details = {
            "P.H.D Registration Date": data['phd_registration_date'],
            "P.H.D Registration Year": data['phd_registration_year'],
            "Age at Ph.D. Registration": data['phd_registration_age'],
            "University Name": data['concerned_university'],
            "Name of College": data['name_of_college'],
            "Department Name": data['department_name'],
            "Topic of Ph.D.": data['topic_of_phd'],
            "Name of Guide": data['name_of_guide'],
            "Faculty/Stream": data['faculty']
            # Add more fields as needed
        }

        income_details = {
            "Family Annual Income": data['family_annual_income'],
            "Income Certificate Number": data['income_certificate_number'],
            "Income Certificate Issuing Authority": data['issuing_authority'],
            "Income Certificate Issuing District": data['income_issuing_district'],
            "Income Certificate Issuing Taluka": data['income_issuing_taluka']
        }

        caste = {
            "Are you Domicile of Maharashtra": data['domicile'],
            "Domicile Certificate": data['domicile_certificate'],
            "Domicile Certificate Number": data['domicile_number'],
            "Do you have Caste/Tribe Certificate": data['caste_certf'],
            "Caste | Tribe": data['your_caste'],
            "Sub Caste/Tribe": data['subcaste'],
            "Caste Certificate Number": data['caste_certf_number'],
            "Caste Certificate Issuing District": data['issuing_district'],
            "Caste Certificate Issuing Authority": data['caste_issuing_authority'],
            "Validity Certificate": data['validity_certificate'],
            "Validity Certificate Number": data['validity_cert_number'],
            "Validity Certificate Issuing District": data['validity_issuing_district'],
            "Validity Certificate Issuing Taluka": data['validity_issuing_taluka'],
            "Validity Certificate Issuing Authority": data['validity_issuing_authority']
        }

        parent_details = {
            "Salaried": data['salaried'],
            "Disability": data['disability'],
            "Type of Disability": data['type_of_disability'],
            "Father Name": data['father_name'],
            "Mother Name": data['mother_name'],
            "Anyone Work in Government": data['work_in_government'],
            "Department in Government": data['gov_department'],
            "Post in Government": data['gov_position']
        }

        bank_details = {
            "IFSC Code": data['ifsc_code'],
            "Account Number": data['account_number'],
            "Bank Name": data['bank_name'],
            "Account Holder Name": data['account_holder_name'],
            "MICR Code": data['micr']
        }

        pdf = PDF(orientation='P', format='A4')
        pdf.add_page()
        pdf.header()
        pdf.image_and_date(data)

        if pdf.get_y() > 270:  # Prevent overflow
            pdf.add_page()
        pdf.set_font("Arial", "B", size=12)
        pdf.cell(0, 10, "Personal Details", ln=True)
        pdf.ln(2)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.set_font("Arial", size=10)
        pdf.ln(3)
        for field, value in personal_details.items():
            if pdf.get_y() > 270:
                pdf.add_page()
            pdf.cell(70, 8, str(field), border=0)
            pdf.multi_cell(0, 8, str(value), border=0)
        pdf.ln(5)

        # Personal Details
        if pdf.get_y() > 270:  # Prevent overflow
            pdf.add_page()
        pdf.set_font("Arial", "B", size=12)
        pdf.cell(0, 10, "Address Details", ln=True)
        pdf.ln(2)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.set_font("Arial", size=10)
        pdf.ln(3)
        for field, value in address_details.items():
            if pdf.get_y() > 270:
                pdf.add_page()
            pdf.cell(70, 8, str(field), border=0)
            pdf.multi_cell(0, 8, str(value), border=0)
        pdf.ln(5)

        pdf.set_font("Arial", "B", size=12)
        pdf.cell(0, 10, "Qualification Details", ln=True)

        pdf.ln(10)  # Increase this value to shift the content further down

        # SSC Details
        if pdf.get_y() > 270:  # Prevent overflow
            pdf.add_page()
        pdf.set_font("Arial", "B", size=12)
        pdf.cell(0, 10, "S.S.C Details", ln=True)
        pdf.ln(2)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.set_font("Arial", size=10)
        pdf.ln(3)
        for field, value in ssc.items():
            if pdf.get_y() > 270:
                pdf.add_page()
            pdf.cell(70, 8, str(field), border=0)
            pdf.multi_cell(0, 8, str(value), border=0)
        pdf.ln(5)

        # HSC Details
        if pdf.get_y() > 270:  # Prevent overflow
            pdf.add_page()
        pdf.set_font("Arial", "B", size=12)
        pdf.cell(0, 10, "H.S.C Details", ln=True)
        pdf.ln(2)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.set_font("Arial", size=10)
        pdf.ln(3)
        for field, value in hsc.items():
            if pdf.get_y() > 270:
                pdf.add_page()
            pdf.cell(70, 8, str(field), border=0)
            pdf.multi_cell(0, 8, str(value), border=0)
        pdf.ln(5)

        # Graduation Details
        if pdf.get_y() > 270:  # Prevent overflow
            pdf.add_page()
        pdf.set_font("Arial", "B", size=12)
        pdf.cell(0, 10, "Graduation Details", ln=True)
        pdf.ln(2)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.set_font("Arial", size=10)
        pdf.ln(3)
        for field, value in grad.items():
            if pdf.get_y() > 270:
                pdf.add_page()
            pdf.cell(70, 8, str(field), border=0)
            pdf.multi_cell(0, 8, str(value), border=0)
        pdf.ln(5)

        # Post Graduation Details
        if pdf.get_y() > 270:  # Prevent overflow
            pdf.add_page()
        pdf.set_font("Arial", "B", size=12)
        pdf.cell(0, 10, "Post Graduation Details", ln=True)
        pdf.ln(2)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.set_font("Arial", size=10)
        pdf.ln(3)
        for field, value in postgrad.items():
            if pdf.get_y() > 270:
                pdf.add_page()
            pdf.cell(70, 8, str(field), border=0)
            pdf.multi_cell(0, 8, str(value), border=0)
        pdf.ln(5)

        # Personal Details
        if pdf.get_y() > 270:  # Prevent overflow
            pdf.add_page()
        pdf.set_font("Arial", "B", size=12)
        pdf.cell(0, 10, "P.H.D Details", ln=True)
        pdf.ln(2)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.set_font("Arial", size=10)
        pdf.ln(3)
        for field, value in phd_details.items():
            if pdf.get_y() > 270:
                pdf.add_page()
            pdf.cell(70, 8, str(field), border=0)
            pdf.multi_cell(0, 8, str(value), border=0)
        pdf.ln(5)

        # Personal Details
        if pdf.get_y() > 270:  # Prevent overflow
            pdf.add_page()
        pdf.set_font("Arial", "B", size=12)
        pdf.cell(0, 10, "Income Details", ln=True)
        pdf.ln(2)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.set_font("Arial", size=10)
        pdf.ln(3)
        for field, value in income_details.items():
            if pdf.get_y() > 270:
                pdf.add_page()
            pdf.cell(70, 8, str(field), border=0)
            pdf.multi_cell(0, 8, str(value), border=0)
        pdf.ln(5)

        pdf.ln(21)

        # Personal Details
        if pdf.get_y() > 270:  # Prevent overflow
            pdf.add_page()
        pdf.set_font("Arial", "B", size=12)
        pdf.cell(0, 10, "Caste/Tribe Details", ln=True)
        pdf.ln(2)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.set_font("Arial", size=10)
        pdf.ln(3)
        for field, value in caste.items():
            if pdf.get_y() > 270:
                pdf.add_page()
            pdf.cell(70, 8, str(field), border=0)
            pdf.multi_cell(0, 8, str(value), border=0)
        pdf.ln(5)

        # Personal Details
        if pdf.get_y() > 270:  # Prevent overflow
            pdf.add_page()
        pdf.set_font("Arial", "B", size=12)
        pdf.cell(0, 10, "Parent Details", ln=True)
        pdf.ln(2)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.set_font("Arial", size=10)
        pdf.ln(3)
        for field, value in parent_details.items():
            if pdf.get_y() > 270:
                pdf.add_page()
            pdf.cell(70, 8, str(field), border=0)
            pdf.multi_cell(0, 8, str(value), border=0)
        pdf.ln(5)

        # Personal Details
        if pdf.get_y() > 270:  # Prevent overflow
            pdf.add_page()
        pdf.set_font("Arial", "B", size=12)
        pdf.cell(0, 10, "Bank Details", ln=True)
        pdf.ln(2)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.set_font("Arial", size=10)
        pdf.ln(3)
        for field, value in bank_details.items():
            if pdf.get_y() > 270:
                pdf.add_page()
            pdf.cell(70, 8, str(field), border=0)
            pdf.multi_cell(0, 8, str(value), border=0)
        pdf.ln(5)

        # Applicant's Signature
        text = (
            "I hereby declare by signing below that the above particulars are true and correct to the best of my knowledge "
            "and belief and nothing has been concealed therein.")
        # Define the width for text wrapping
        width = 400  # Adjust this width according to your requirement
        # Draw the text with wrapping
        pdf.multi_cell(0, 7, text)
        pdf.set_font("Arial", size=12)

        # Assuming data['signature'] contains the path to the image file
        signature_path = '/var/www/fellowship/fellowship/FellowshipPreServer/' + data['signature']
        # Determine the current position
        x = pdf.get_x()
        y = pdf.get_y()
        # Set position for the image
        pdf.set_xy(x + 10, y + 5)  # Adjust position as needed
        # Add the image
        pdf.image(signature_path, x + 50, y + 10, 50)  # Adjust width (50) as needed
        # Move to a new line
        pdf.ln(15)  # Adjust as needed
        pdf.cell(0, 10, "Applicant's Signature:", ln=True)
        pdf.ln(15)  # Adjust this value to control the space after the line

        current_date = datetime.now().strftime("%Y-%m-%d")  # You can change the date format as needed
        pdf.cell(0, 10, "Date:" + ' ' + current_date, ln=True)
        pdf.cell(0, 10, "Place:" + ' ' + str(data['district']) + ', ' + str(data['state']), ln=True)

        # Save the PDF to a file
        pdf.output(filename)
