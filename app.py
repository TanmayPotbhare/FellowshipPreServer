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

# @app.route('/section4')
# def section4():
#     return render_template('CandidatePages/ApplicationForm/section4.html', title='Application Form (Parents and Bank Details)')


@app.route('/section5')
def section5():
    return render_template('CandidatePages/ApplicationForm/section5.html', title='Application Form (Documents)')


# ------------ Blueprint Registration --------------
homepage_blueprints(app, mail)    # These blueprints are in the file - (blueprints_homepage.py)
admin_blueprints(app, mail)     # These blueprints are in the file - (blueprints_admin.py)
candidate_blueprints(app, mail)     # These blueprints are in the file - (blueprints_admin.py)


if __name__ == '__main__':
    app.run(debug = True)
