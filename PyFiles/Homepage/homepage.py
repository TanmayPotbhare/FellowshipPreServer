import folium
import mysql.connector
from classes.connection import HostConfig, ConfigPaths, ConnectParam
from flask import Blueprint, render_template, session, request, redirect, url_for, jsonify
from PyFiles.Homepage.multilingual_content import multilingual_content

homepage_blueprint = Blueprint('homepage', __name__)


def init_auth(app):
    # ------ HOST Configs are in classes/connection.py
    host = HostConfig.host
    app_paths = ConfigPaths.paths.get(host)
    if app_paths:
        for key, value in app_paths.items():
            app.config[key] = value

    # ---------------------------------
    #           HOMEPAGE
    # ---------------------------------
    @homepage_blueprint.route('/', methods=['GET', 'POST'])
    def home_page():
        if 'language' in session:
            language = session['language']
        else:
            language = 'marathi'

        # --------------------------  HOME PAGE
        total_count = applications_today()
        fellow_awarded = fellow_awarded_count()
        total_appl_22 = total_appl_22_count()
        total_appl_23 = total_appl_23_count()

        # print("old user 2022",old_user_22)
        news_record = news_fetch()
        return render_template('Homepage/home-page.html', total_count=total_count, fellow_awarded=fellow_awarded,
                               total_appl_22=total_appl_22, total_appl_23=total_appl_23,
                               language=language, multilingual_content=multilingual_content)

    @homepage_blueprint.route('/pythonConnector', methods=['GET', 'POST'])
    def pythonConnector():
        import subprocess
        import time

        # Variables defined in PHP
        number = "882284367228"
        RefNum = "1291304087928938496"
        setAc = "A100098"
        setSA = "A100098"
        setLK = "260288bb-f12c-4955-a2b6-94b77f98236b"
        # opr = "getrefnum"
        opr = "getuid"
        keyType = "aes"
        tokenType = "soft"
        url = "https://sp.epramaan.in:8038/vault/"
        idType = "uid"

        # Generate the current Unix timestamp in seconds
        timestamp = int(time.time())

        # Prepare the arguments array for the Java command
        args = [
            "java", "-jar", "/var/www/fellowship/fellowship/cdac/wrapper.jar",
            number, RefNum, setAc, setSA, setLK,
            opr, keyType, tokenType, url, idType, str(timestamp)
        ]

        # Run the Java command using subprocess
        process = subprocess.run(args, capture_output=True, text=True)

        # Output the results
        print("OUTPUT: ")
        print(process.stdout)

        # If there are errors, print them too
        if process.stderr:
            print("ERROR: ")
            print(process.stderr)

        return render_template('pythonConnector.html', jsonify(process))

    # --------------------------- Definitions of Counts in Homepage -------------------------------------
    def applications_today():
        cnx = mysql.connector.connect(user='root', password='A9CALcsd7lc%7ac',
                                      host=host,
                                      database='ICSApplication')
        cursor = cnx.cursor()
        cursor.execute(" SELECT COUNT(*) FROM application_page where phd_registration_year>=2023 ")
        result = cursor.fetchone()
        print(result)
        return result[0]

    def fellow_awarded_count():
        cnx = mysql.connector.connect(user='root', password='A9CALcsd7lc%7ac',
                                      host=host,
                                      database='ICSApplication')
        cursor = cnx.cursor()
        cursor.execute(
            " SELECT COUNT(*) FROM application_page where phd_registration_year='2023' and final_approval='accepted' ")
        result = cursor.fetchone()
        print(result)
        return result[0]

    def total_appl_22_count():
        cnx = mysql.connector.connect(user='root', password='A9CALcsd7lc%7ac',
                                      host=host,
                                      database='ICSApplication')
        cursor = cnx.cursor()
        cursor.execute(" SELECT COUNT(*) FROM application_page where phd_registration_year='2022' ")
        result = cursor.fetchone()
        print(result)
        return result[0]

    def total_appl_23_count():
        cnx = mysql.connector.connect(user='root', password='A9CALcsd7lc%7ac',
                                      host=host,
                                      database='ICSApplication')
        cursor = cnx.cursor()
        cursor.execute(" SELECT COUNT(*) FROM application_page where phd_registration_year='2023' ")
        result = cursor.fetchone()
        print(result)
        return result[0]

    def news_fetch():
        cnx = mysql.connector.connect(user='root', password='A9CALcsd7lc%7ac',
                                      host=host,
                                      database='ICSApplication')
        cursor = cnx.cursor(dictionary=True)
        cursor.execute(" SELECT * FROM news_and_updates ORDER BY id DESC LIMIT 5 ")
        result = cursor.fetchall()
        return result

    @homepage_blueprint.route('/viewallnews', methods=['GET', 'POST'])
    def viewallnews():
        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)

        cursor.execute(" SELECT * FROM news_and_updates ")
        result = cursor.fetchall()
        return render_template('Homepage/viewallnews.html', result=result)

    # -------------------- End of Definitions of Counts in Homepage ---------------------------------
    #           END HOMEPAGE
    # ---------------------------------

    # ---------------------------------
    #           ABOUT US
    # ---------------------------------
    @homepage_blueprint.route('/aboutus')
    def aboutus():
        if 'language' in session:
            language = session['language']
        else:
            language = 'marathi'
        return render_template('Homepage/AboutUs.html', language=language, multilingual_content=multilingual_content)
    # ---------------------------------
    #           END ABOUT US
    # ---------------------------------

    # ---------------------------------
    #           GR PAGE
    # ---------------------------------
    @homepage_blueprint.route('/gr_page')
    def gr_page():
        if 'language' in session:
            language = session['language']
        else:
            language = 'marathi'
        return render_template('Homepage/gr_page.html', language=language, multilingual_content=multilingual_content)
    # ---------------------------------
    #           END GR PAGE
    # ---------------------------------

    # ---------------------------------
    #           CONTACT US
    # ---------------------------------
    @homepage_blueprint.route('/contact')
    def contact_us():  # --------------------------  CONTACT US PAGE
        if 'language' in session:
            language = session['language']
        else:
            language = 'marathi'
        # Create a folium map centered at Pune, India
        m = folium.Map(location=[18.5204, 73.8567], zoom_start=12)
        # Add a marker at Pune, India
        folium.Marker(location=[18.5204, 73.8567], popup="Pune, India").add_to(m)
        # Render the map in the template
        map_html = m._repr_html_()
        # Pass the map HTML to the template
        return render_template('Homepage/contact.html', map=map_html, language=language,
                               multilingual_content=multilingual_content)

    # Submit Form on Contact Us Page
    @homepage_blueprint.route('/contact_submit', methods=['GET', 'POST'])
    def contact_submit():
        if 'language' in session:
            language = session['language']
        else:
            language = 'marathi'
        cnx = mysql.connector.connect(user='root', password='A9CALcsd7lc%7ac',  # --------  DATABASE CONNECTION
                                      host=host,
                                      database='ICSApplication')
        cursor = cnx.cursor()
        if request.method == 'POST':
            ticket = 'Contact Us'
            fullname = request.form['fullname']
            email = request.form['email']
            issue_subject = request.form['issue_subject']
            description = request.form['description']

            sql = "INSERT INTO issue_raised (ticket, fullname, email, issue_subject, description) " \
                  "VALUES (%s, %s, %s, %s, %s)"
            # Execute the SQL statement with the data
            cursor.execute(sql, (ticket, fullname, email, issue_subject, description))
            cnx.commit()
            cursor.close()
            cnx.close()
            return render_template('Homepage/contact.html', language=language, multilingual_content=multilingual_content)
        return redirect(url_for('homepage.contact_us'))
    # ---------------------------------
    #           END CONTACT US
    # ---------------------------------

    # ---------------------------------
    #           REPORTS PAGE
    # ---------------------------------
    @homepage_blueprint.route('/charts')
    def reports():
        if 'language' in session:
            language = session['language']
        else:
            language = 'marathi'
        # twentyone_count = year_twentyone_count()
        # twentytwo_count = year_twentytwo_count()
        # twentythree_count = year_twentythree_count()
        # male_count = male_count_report()
        # female_count = female_count_report()
        # trans_count = trans_count_report()
        # disability_yes = disability_yes_count_report()
        # disability_no = disability_no_count_report()
        return render_template('Homepage/report_homepage.html',
                               multilingual_content=multilingual_content,  language=language)
    # ---------------------------------
    #           END REPORTS PAGE
    # ---------------------------------

    # ---------------------------------
    #           FAQ PAGE
    # ---------------------------------
    @homepage_blueprint.route('/faq')
    def faq():
        if 'language' in session:
            language = session['language']
        else:
            language = 'marathi'
        return render_template('Homepage/FAQ.html', multilingual_content=multilingual_content, language=language)
    # ---------------------------------
    #           END FAQ PAGE
    # ---------------------------------