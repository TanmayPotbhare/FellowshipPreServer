from datetime import date, timedelta
import mysql.connector
from classes.connection import HostConfig, ConfigPaths, ConnectParam
import os
from flask_mail import Mail, Message
from flask import Blueprint, render_template, session, request, redirect, url_for, flash
from authentication.middleware import auth

bulkemails_blueprint = Blueprint('bulkemails', __name__)


def bulkemails_auth(app, mail):
    # ------ HOST Configs are in classes/connection.py
    host = HostConfig.host
    app_paths = ConfigPaths.paths.get(host)
    if app_paths:
        for key, value in app_paths.items():
            app.config[key] = value

    @bulkemails_blueprint.route('/sendbulkEmails', methods=['GET', 'POST'])
    def sendbulkEmails():
        if not session.get('logged_in'):
            # Redirect to the admin login page if the user is not logged in
            return redirect(url_for('adminlogin.admin_login'))
        cnx = mysql.connector.connect(user='root', password='A9CALcsd7lc%7ac',
                                      host=host,
                                      database='ICSApplication')
        cursor = cnx.cursor(dictionary=True)
        record = None  # Initialize record with a default value or None
        email_list = None
        if request.method == 'POST':
            year = request.form['year']
            print(year)
            sql = """ SELECT email FROM signup WHERE year=%s"""
            cursor.execute(sql, (year,))
            record = cursor.fetchall()
            print(record)
            # Process the records as needed
            email_list = [entry['email'] for entry in record]
            print(email_list)
        cursor.close()
        cnx.close()

        return render_template('Admin/sendbulkEmails.html', record=record, email_list=email_list)

    @bulkemails_blueprint.route('/send_bulk_email', methods=['GET', 'POST'])
    def send_bulk_emails():
        cnx = mysql.connector.connect(user='root', password='A9CALcsd7lc%7ac',
                                      host=host,
                                      database='ICSApplication')

        cursor = cnx.cursor(dictionary=True)
        if request.method == 'POST':
            print(request.form)
            # Get the email list, message, and subject from the form submission
            email_list = request.form.getlist('email_list[]')

            message = request.form.get('message', '')
            subject = request.form.get('subject', '')
            # attachment = request.files['attachment']
            # attachment_path = save_bulk_email_file(attachment)
            # print("Routing Attachment -", attachment_path)
            print(message, subject)
            # Send emails
            send_bulk_email(message, subject, email_list)

        cursor.close()
        cnx.close()

        return render_template('Admin/BulkEmailSent.html')

    def send_bulk_email(message, subject, email_list):
        msg = Message(subject=subject, sender='helpdesk@trti-maha.in', recipients=email_list)
        msg_body = message
        msg.html = msg_body
        # Attach file
        # print(attachment_path)
        # with open(attachment_path, 'rb') as f:
        #     file_data = f.read()
        # # Get the file name from the attachment_path
        # filename = os.path.basename(attachment_path)
        # # Determine the MIME type based on the file extension
        # mime_type, _ = mimetypes.guess_type(filename)
        # # If MIME type is not detected, set a default value
        # if not mime_type:
        #     mime_type = 'application/octet-stream'
        # print(attachment_path)
        # Add the attachment to the email message
        # msg.attach(filename, mime_type, file_data)
        mail.send(msg)