import mysql.connector
from classes.connection import HostConfig, ConfigPaths
import os
from fpdf import FPDF
from flask import Blueprint, render_template, session, request, redirect, url_for, flash, Response
from authentication.middleware import auth

awardletter_blueprint = Blueprint('awardletter', __name__)


def awardletter_auth(app):
    # ------ HOST Configs are in classes/connection.py
    host = HostConfig.host
    app_paths = ConfigPaths.paths.get(host)
    if app_paths:
        for key, value in app_paths.items():
            app.config[key] = value

    @awardletter_blueprint.route('/award_letter_AA')
    def award_letter_AA():
        try:
            email = session['email']
            output_filename = '/var/www/icswebapp/icswebapp/static/pdf_application_form/award_letter.pdf'
            # output_filename = 'static/pdf_application_form/award_letter.pdf'
            cnx = mysql.connector.connect(user='icswebapp', password='A9CALcsd7lc%7ac', host=host,
                                          database='ICSApplication')
            cursor = cnx.cursor(dictionary=True)
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
                "SELECT phd_registration_year FROM application_page WHERE email = %s",
                (email,))
            result = cursor.fetchone()
            year = result['phd_registration_year']
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

    def generate_award_letter_2022(data, filename):
        class PDF(FPDF):
            header_added = False  # To track whether the header is added to the first page

            def header(self):
                if not self.header_added:
                    var = get_base_url()
                    print(var)
                    # Add a header
                    self.set_font("Arial", "B", 12)
                    self.image('/var/www/icswebapp/icswebapp/static/Images/satya.png', 94, 10,
                               20)  # Replace with the path to your small imag
                    # Calculate the width of the image
                    image_width = 100  # Assuming the width of the image is 100 (adjust if different)
                    # Calculate the position for "Government of Maharashtra" text
                    text_x_position = self.get_x()  # Get current X position
                    text_y_position = self.get_y() + 20  # Set Y position below the image
                    # Set cursor position
                    self.set_xy(text_x_position, text_y_position)
                    self.image('/var/www/icswebapp/icswebapp/static/Images/newtrtiImage.png', 10, 10,
                               45)  # Replace with the path to your symbol image
                    self.image('/var/www/icswebapp/icswebapp/static/Images/mahashasn_new.png', 155, 10,
                               45)  # Replace with the path to your symbol image
                    self.ln(5)
                    self.ln(0)  # Reduce the space below the address
                    self.cell(0, 5, "Government of Maharashtra", align="C", ln=True)

                    self.cell(0, 5, "Tribal Research & Training Institute", align="C", ln=True)
                    self.cell(0, 10, "28, Queens Garden, Pune - 411001", align="C", ln=True)
                    self.dashed_line(10, self.get_y(), 200, self.get_y(), dash_length=3, space_length=1)

                    self.ln(5)  # Adjust this value to control the space after the line
                    self.set_font("Arial", "B", size=10)
                    self.cell(0, 10,
                              " Fellowship Award Letter",
                              align="C", ln=True)
                    self.ln(2)  # Adjust this value to control the space after the line

                    self.rotate(45)  # Rotate the text by 45 degrees
                    self.set_font('Arial', '', 45)
                    self.set_text_color(192, 192, 192)
                    self.text(-30, 195, "STRF FELLOWSHIP")  # Use text instead of rotated_text
                    self.rotate(0)  # Reset the rotation to 0 degrees

                    self.header_added = True  # Set to True after adding the header

            def to_name(self, data):
                # AWARD LETTER in the center

                # To, and Dear Candidate aligned to the left
                self.set_font("Arial", "", size=10)
                self.cell(0, 10, "To,", ln=True)
                self.set_font("Arial", "B", size=11)
                self.cell(0, 10, data['first_name'] + ' ' + data['middle_name'] + ' ' + data['last_name'], ln=True)

            def insert_static_data(self, data):
                # Insert your static data here
                self.set_font("Arial", "B", size=10)
                self.cell(0, 10, "Dear Candidate,", ln=True)
                self.set_font("Arial", "", 10)
                registration_year = data['phd_registration_year']
                fiscal_year = f"{registration_year} - {registration_year + 1}"
                self.multi_cell(0, 7,
                                "         We are delighted to inform you that you have been selected for the award of "
                                "a Fellowship for the year " + fiscal_year +
                                " for Ph.D. The Fellowship amount will be effective from the date of registration for Ph.D. Congratulations! "
                                )
                self.ln(3)  # Adjust this value to control the space before static data
                self.multi_cell(0, 7,
                                "       TRTI reserves all the rights to add terms and conditions as and when required, and "
                                "candidates are required to accept any changes in the terms and conditions of the fellowship."
                                )
                self.ln(3)  # Adjust this value to control the space before static data
                self.multi_cell(0, 7,
                                "       Attached with this letter is an undertaking stating that all the information provided "
                                "for the document verification is true to the best of my knowledge. Any discrepancy found "
                                "may result in the cancellation of the Fellowship. Please note that failure to submit the "
                                "undertaking will be assumed as non-acceptance of this offer, and the Fellowship will not "
                                "be  processed. "
                                )
                self.ln(3)  # Adjust this value to control the space before static data
                self.multi_cell(0, 7,
                                "       We believe this Fellowship will not only provide financial support but also contribute"
                                " to your academic growth. It will enable you to conduct research on your subject and "
                                "foster excellence in academia. Moreover, it will empower you to become an advocate for"
                                " equality, social justice, a contributor to peace, harmony and happiness within various"
                                " disadvantaged sections of society. "
                                )
                self.multi_cell(0, 20, "Wish you all the best. ")
                self.set_x(150)  # Adjust the x-coordinate as needed
                # self.image('static/Images/signature_awardletter.png', 20, 230, 30)
                self.image('/var/www/icswebapp/icswebapp/static/Images/sonanwanesir_signature.png', 125, 210, 50)
                self.ln(5)  # Adjust this value to control the space after static data

            def footer(self):
                # Add a footer
                self.set_y(-15)
                self.set_font("arial", "B", 8)
                self.cell(0, 10, f" {self.page_no()} ", align="C")

                # Center-align the "TRTI" text
                self.cell(0, 10, " TRTI  |  Fellowship | 2023 - 2024 ", align="R")

        pdf = PDF()
        pdf.add_page()
        pdf.header()
        pdf.to_name(data)
        # Insert static data
        pdf.insert_static_data(data)
        # Save the PDF to a file
        pdf.output(filename)

    def generate_award_letter_2023(data, filename):
        class PDF(FPDF):
            header_added = False  # To track whether the header is added to the first page

            def header(self):
                if not self.header_added:
                    var = get_base_url()
                    print(var)
                    # Add a header
                    self.set_font("Arial", "B", 12)
                    # self.image('static/Images/satya.png', 94, 10, 20)  # Replace with the path to your small imag
                    self.image('/var/www/icswebapp/icswebapp/static/Images/satya.png', 94, 10,
                               20)  # Replace with the path to your small imag
                    # Calculate the width of the image
                    image_width = 100  # Assuming the width of the image is 100 (adjust if different)
                    # Calculate the position for "Government of Maharashtra" text
                    text_x_position = self.get_x()  # Get current X position
                    text_y_position = self.get_y() + 20  # Set Y position below the image
                    # Set cursor position
                    self.set_xy(text_x_position, text_y_position)
                    # self.image('static/Images/newtrtiImage.png', 10, 10, 45)  # Replace with the path to your symbol image
                    self.image('/var/www/icswebapp/icswebapp/static/Images/newtrtiImage.png', 10, 10,
                               45)  # Replace with the path to your symbol image
                    # self.image('static/Images/mahashasn_new.png', 155, 10, 45)  # Replace with the path to your symbol image
                    self.image('/var/www/icswebapp/icswebapp/static/Images/mahashasn_new.png', 155, 10,
                               45)  # Replace with the path to your symbol image
                    self.ln(5)
                    self.ln(0)  # Reduce the space below the address
                    self.cell(0, 5, "Government of Maharashtra", align="C", ln=True)

                    self.cell(0, 5, "Tribal Research & Training Institute", align="C", ln=True)
                    self.cell(0, 10, "28, Queens Garden, Pune - 411001", align="C", ln=True)
                    self.dashed_line(10, self.get_y(), 200, self.get_y(), dash_length=3, space_length=1)

                    self.ln(5)  # Adjust this value to control the space after the line
                    self.set_font("Arial", size=10)
                    self.cell(0, 10, "No.: Research-2024/Case.No 9/Desk-4/1832",
                              ln=False)  # Add the number on the left without a line break

                    # Move to the right for the date
                    self.cell(0, 10, "Date: 2024-07-04", align="R",
                              ln=True)  # Add the date on the right with a line break

                    self.set_font("Arial", "B", size=10)
                    self.cell(0, 10,
                              " Fellowship Award Letter",
                              align="C", ln=True)
                    self.ln(2)  # Adjust this value to control the space after the line

                    self.rotate(45)  # Rotate the text by 45 degrees
                    self.set_font('Arial', '', 45)
                    self.set_text_color(192, 192, 192)
                    self.text(-30, 195, "STRF FELLOWSHIP")  # Use text instead of rotated_text
                    self.rotate(0)  # Reset the rotation to 0 degrees

                    self.header_added = True  # Set to True after adding the header

            def to_name(self, data):
                # AWARD LETTER in the center

                # To, and Dear Candidate aligned to the left
                self.set_font("Arial", "", size=10)
                self.cell(0, 10, "To,", ln=True)
                self.set_font("Arial", "B", size=11)
                self.cell(0, 10, data['first_name'] + ' ' + data['middle_name'] + ' ' + data['last_name'], ln=True)

            def insert_static_data(self, data):
                # Insert your static data here
                self.set_font("Arial", "B", size=10)
                self.cell(0, 10, "Dear Candidate,", ln=True)
                self.set_font("Arial", "", 10)
                registration_year = data['phd_registration_year']
                fiscal_year = f"{registration_year} - {registration_year + 1}"
                self.multi_cell(0, 7,
                                "         We are delighted to inform you that you have been selected for the award of "
                                "a Fellowship for the year " + fiscal_year +
                                " for Ph.D. The Fellowship amount will be effective from the date of registration for Ph.D. Congratulations! "
                                )
                self.ln(3)  # Adjust this value to control the space before static data
                self.multi_cell(0, 7,
                                "       TRTI reserves all the rights to add terms and conditions as and when required, and "
                                "candidates are required to accept any changes in the terms and conditions of the fellowship."
                                )
                self.ln(3)  # Adjust this value to control the space before static data
                self.multi_cell(0, 7,
                                "       Attached with this letter is an undertaking stating that all the information provided "
                                "for the document verification is true to the best of my knowledge. Any discrepancy found "
                                "may result in the cancellation of the Fellowship. Please note that failure to submit the "
                                "undertaking will be assumed as non-acceptance of this offer, and the Fellowship will not "
                                "be  processed. "
                                )
                self.ln(3)  # Adjust this value to control the space before static data
                self.multi_cell(0, 7,
                                "       We believe this Fellowship will not only provide financial support but also contribute"
                                " to your academic growth. It will enable you to conduct research on your subject and "
                                "foster excellence in academia. Moreover, it will empower you to become an advocate for"
                                " equality, social justice, a contributor to peace, harmony and happiness within various"
                                " disadvantaged sections of society. "
                                )
                self.multi_cell(0, 20, "Wish you all the best. ")
                self.set_x(150)  # Adjust the x-coordinate as needed
                # self.image('static/Images/signature_awardletter.png', 20, 230, 30)
                # self.image('static/Images/chanchalamam_signature.png', 125, 210, 50)
                self.image('/var/www/icswebapp/icswebapp/static/Images/chanchalamam_signature.png', 125, 210, 50)
                self.ln(5)  # Adjust this value to control the space after static data

            def footer(self):
                # Add a footer
                self.set_y(-15)
                self.set_font("arial", "B", 8)
                self.cell(0, 10, f" {self.page_no()} ", align="C")

                # Center-align the "TRTI" text
                self.cell(0, 10, " TRTI  |  Fellowship | 2023 - 2024 ", align="R")

        pdf = PDF()
        pdf.add_page()
        pdf.header()
        pdf.to_name(data)
        # Insert static data
        pdf.insert_static_data(data)
        # Save the PDF to a file
        pdf.output(filename)

    def get_base_url():
        base_url = request.url_root
        return base_url