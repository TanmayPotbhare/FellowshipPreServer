import requests
from flask import Flask, request, redirect, session, render_template, jsonify
from flask_mail import Mail
import mysql.connector
from Blueprints.blueprints_homepage import homepage_blueprints
from Blueprints.blueprints_admin import admin_blueprints
from Blueprints.blueprints_candidate import candidate_blueprints
from Classes.caste import casteController
from Classes.university import universityController

# ----------- Flask Instance --------------
app = Flask(__name__)
app.config['SECRET_KEY'] = 'FellowApp123@#$*&'
# -----------------------------------------


# ------- All configurations ----------------
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_KEY_PREFIX'] = 'session:'  # Optional, to prevent conflicts
# -----------------------------------------


# ------------- Email API Configurations ------------
# Outlook Mail
# app.config['MAIL_SERVER'] = 'us2.smtp.mailhostbox.com'
app.config['MAIL_SERVER'] = 'smtp.mailgun.org'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'helpdesk@trti-maha.in'
app.config['MAIL_PASSWORD'] = 'Wonder@#$123'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_DEBUG'] = app.debug
mail = Mail(app)
# -----------------------------------------

# ------------------ Database Configuration --------------------
from Classes.database import HostConfig, ConfigPaths

host = HostConfig.host
app_paths = ConfigPaths.paths.get(host)

if app_paths:
    for key, value in app_paths.items():
        app.config[key] = value

cnx = mysql.connector.connect(user='root', password='A9CALcsd7lc%7ac',  # --------  DATABASE CONNECTION
                              host=host,
                              database='ICSApplication')
cursor = cnx.cursor()
# ---------------------- End Configurations ------------------------


# ------------- To Set the Session -------------
@app.route('/set_session/<value>')
def set_session(value):
    """
        Required to set the session or else it will give Build Error.
    """
    session['language'] = value
    return redirect(request.referrer)


@app.route('/section1')
def test_form():
    caste_class = casteController(host)
    all_caste = caste_class.get_all_caste_details()
    return render_template('CandidatePages/ApplicationForm/section1.html', title='Application Form (Personal Details)',
                           all_caste=all_caste)


@app.route('/get_subcastes/<int:unique_number>', methods=['GET'])
def get_subcastes(unique_number):
    caste_class = casteController(host)
    subcastes = caste_class.get_subcastes_by_unique_number(unique_number)
    return jsonify({'subcastes': subcastes})


@app.route('/section2')
def section2():
    cnx = mysql.connector.connect(user='root', password='A9CALcsd7lc%7ac',  # --------  DATABASE CONNECTION
                                  host=host,
                                  database='ICSApplication')
    cursor = cnx.cursor(dictionary=True)
    email = 'tupotbhare@gmail.com'
    university_data = universityController(host)
    university_names = university_data.get_all_university()
    cursor.execute('SELECT YEAR(date_of_birth) AS birth_year FROM application_page where email = %s', (email,))
    dob_year = cursor.fetchone()
    print('DOB', dob_year)
    cnx.close()
    cursor.close()
    return render_template('CandidatePages/ApplicationForm/section2.html', university_data=university_names,
                           title='Application Form (Qualification Details)', dob_year=dob_year)


@app.route('/get_college_data_by_university', methods=['GET','POST'])
def get_college_data_by_university():
    u_id = request.form.get('u_id')
    print(u_id)
    college_obj = universityController(host)
    college_name = college_obj.get_college_name(u_id)
    return jsonify(college_name)


@app.route('/section3')
def section3():
    cnx = mysql.connector.connect(user='root', password='A9CALcsd7lc%7ac',  # --------  DATABASE CONNECTION
                                  host=host,
                                  database='ICSApplication')
    cursor = cnx.cursor(dictionary=True)
    cursor.execute(" SELECT * from districts ")
    districts = cursor.fetchall()
    print(districts)

    caste_class = casteController(host)
    validity = caste_class.get_all_caste_validity_auth()

    cursor.close()
    cnx.close()
    return render_template('CandidatePages/ApplicationForm/section3.html', districts=districts,
                           title='Application Form (Certificate Details)', validity=validity)


@app.route('/get_talukas/<int:district_id>', methods=['GET'])
def get_talukas(district_id):
    # Assuming you have a function to get talukas from the district ID
    caste_class = casteController(host)
    talukas = caste_class.get_taluka_from_district(district_id)
    return jsonify({'talukas': talukas})


@app.route('/get_ifsc_data', methods=['GET'])
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


@app.route('/section4')
def section4():
    return render_template('CandidatePages/ApplicationForm/section4.html', title='Application Form (Parents and Bank Details)')


@app.route('/section5')
def section5():
    return render_template('CandidatePages/ApplicationForm/section5.html', title='Application Form (Documents)')


# ------------ Blueprint Registration --------------
homepage_blueprints(app, mail)    # These blueprints are in the file - (blueprints_homepage.py)
admin_blueprints(app, mail)     # These blueprints are in the file - (blueprints_admin.py)
candidate_blueprints(app, mail)     # These blueprints are in the file - (blueprints_admin.py)


if __name__ == '__main__':
    app.run(debug = True)
