import requests

from Classes.caste import casteController
from Classes.database import HostConfig, ConfigPaths, ConnectParam
from flask import Blueprint, render_template, session, request, redirect, url_for, flash, make_response, jsonify
from PythonFiles.CandidatePages.document_paths import save_applicant_photo


section1_blueprint = Blueprint('section1', __name__)


def section1_auth(app):
    # ------ HOST Configs are in classes/connection.py
    host = HostConfig.host
    app_paths = ConfigPaths.paths.get(host)
    if app_paths:
        for key, value in app_paths.items():
            app.config[key] = value

    @section1_blueprint.route('/get_pincode_data', methods=['GET'])
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

    @section1_blueprint.route('/section1', methods=['GET', 'POST'])
    def section1():
        if not session.get('logged_in_from_login'):
            # Redirect to the admin login page if the user is not logged in
            return redirect(url_for('login_signup.login'))

        email = session['email']

        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)

        # Check if a record already exists for this user
        cursor.execute("SELECT applicant_photo, first_name, final_approval,"
                       "middle_name, last_name, mobile_number, email, date_of_birth, gender, age, caste, your_caste, subcaste,"
                       "pvtg, pvtg_caste, marital_status, add_1, add_2, pincode, village, taluka, district, state, city"
                       " FROM application_page WHERE email = %s", (email,))
        record = cursor.fetchone()
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

        caste_class = casteController(host)
        all_caste = caste_class.get_all_caste_details()
        # print(all_caste)
        # print('I am here')
        return render_template('CandidatePages/section1.html', record=record, all_caste=all_caste,
                               finally_approved=finally_approved, user=user, photo=photo,
                               title='Application Form (Personal Details)')

    @section1_blueprint.route('/section1_submit', methods=['GET', 'POST'])
    def section1_submit():
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
        print(record)
        if record['final_approval'] == 'accepted':
            finally_approved = 'approved'
        else:
            finally_approved = 'pending'

        if record:
            user = record['first_name'] + ' ' + record['last_name']
            photo = record['applicant_photo']
        else:
            user = "Admin"
            photo = '/static/assets/img/default_user.png'

        caste_class = casteController(host)
        all_caste = caste_class.get_all_caste_details()
        print(all_caste)
        # Initialize an empty dictionary if no record is found
        if record is None:
            record = {}

        if request.method == 'POST':
            #
            adhaar_number = request.form['adhaar_number']
            adhaar_seeding = request.form['adhaar_seeding']
            first_name = request.form['first_name']
            middle_name = request.form['middle_name']
            last_name = request.form['last_name']
            mobile_number = request.form['mobile_number']
            email = session['email']
            date_of_birth = request.form['date_of_birth']
            gender = request.form['gender']
            age = request.form['age']
            caste = request.form['caste']
            your_caste = request.form['your_caste']
            pvtg = request.form['pvtg']
            pvtg_caste = request.form['pvtg_caste']
            marital_status = request.form['marital_status']
            add_1 = request.form['add_1']
            add_2 = request.form['add_2']
            pincode = request.form['pincode']
            village = request.form['village']
            taluka = request.form['taluka']
            district = request.form['district']
            state = request.form['state']
            city = request.form['city']
            subcaste = request.form['subcaste']
            # Access other fields in a similar manner
            # Handle file upload (applicant's photo)
            photo = request.files['applicant_photo']
            photo_path = save_applicant_photo(photo, first_name, last_name)

            if not record:
                # Save the form data to the database
                print('Inserting new record for:' + email)
                cursor.execute(
                    "INSERT INTO application_page (applicant_photo, adhaar_number, adhaar_seeding,  first_name, "
                    "middle_name, last_name, mobile_number, email, date_of_birth, gender, age,pvtg, pvtg_caste, caste, your_caste,"
                    "marital_status, add_1, add_2, pincode, village, taluka, district, state, city,subcaste) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s)",
                    (photo_path, adhaar_number, adhaar_seeding, first_name, middle_name, last_name, mobile_number,
                     email, date_of_birth, gender, age, pvtg, pvtg_caste, caste, your_caste, marital_status, add_1,
                     add_2,
                     pincode, village, taluka, district, state, city, subcaste))
                cnx.commit()
                return redirect(url_for('section2.section2'))
                # Check if the user is approved for fellowship no matter the year to show the desired sidebar.

        return render_template('CandidatePages/section1.html', record=record, all_caste=all_caste,
                               finally_approved=finally_approved, user=user, photo=photo,
                               title='Application Form (Personal Details)')