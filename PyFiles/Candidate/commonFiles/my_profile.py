from datetime import datetime, date
import mysql.connector
import requests
import os
from flask_mail import Mail, Message
from classes.connection import HostConfig, ConfigPaths
from flask import Blueprint, render_template, session, request, jsonify, flash, Response

my_profile_blueprint = Blueprint('my_profile', __name__)


def my_profile_auth(app, mail):
    # ------ HOST Configs are in classes/connection.py
    host = HostConfig.host
    app_paths = ConfigPaths.paths.get(host)
    if app_paths:
        for key, value in app_paths.items():
            app.config[key] = value

    @my_profile_blueprint.route('/user_profile', methods=['GET', 'POST'])
    def user_profile():
        flash_msg_profile = None
        flash_msg = None  # ----------------  USERS PROFILE USER SIDE PAGE
        email = session['email']
        if request.method == 'POST':
            if 'edit_profile' in request.form:
                submit_edit_profile()  # Call the edit profile function
                flash_msg_profile = "success"
            elif 'change_password' in request.form:
                change_password_user()  # Call the change password function
                flash_msg = "success"  # Flash a success message

        cnx = mysql.connector.connect(user='root', password='A9CALcsd7lc%7ac',
                                      host=host,
                                      database='ICSApplication')
        cursor = cnx.cursor(dictionary=True)

        sql = """SELECT * FROM application_page WHERE email = %s"""
        cursor.execute(sql, (email,))
        records = cursor.fetchall()
        cursor.close()
        cnx.close()
        if records:
            user = records[0]['first_name']
        else:
            user = 'Admin'

        return render_template('Candidate/commonFiles/users-profile.html', records=records, flash_msg=flash_msg,
                               flash_msg_profile=flash_msg_profile, user=user)

    def submit_edit_profile():  # ------------- SUBMIT EDIT PROFILE FOR MY PROFILE
        if request.method == 'POST':
            first_name = request.form['first_name']
            address = request.form['add_1']
            phone = request.form['mobile_number']
            email = session['email']
            cnx = mysql.connector.connect(user='root', password='A9CALcsd7lc%7ac',
                                          host=host,
                                          database='ICSApplication')
            cursor = cnx.cursor(dictionary=True)
            # Construct the SQL update query
            sql = f"UPDATE application_page SET first_name = '{first_name}', add_1 = '{address}', mobile_number = '{phone}' WHERE email = '{email}'"
            cursor.execute(sql)
            cnx.commit()
            cursor.close()
            cnx.close()
            flash('Record Updated successfully', 'success')

    def change_password_user():
        if request.method == 'POST':
            current_password = request.form['current_password']
            new_password = request.form['new_password']
            confirm_password = request.form['confirm_password']
            email = session['email']

            # Connect to the database
            cnx = mysql.connector.connect(user='root', password='A9CALcsd7lc%7ac', host=host, database='ICSApplication')
            cursor = cnx.cursor(dictionary=True)

            # Retrieve hashed password from the database
            query = 'SELECT password FROM signup WHERE email = %s'
            cursor.execute(query, (email,))
            result = cursor.fetchone()

            if result:
                stored_password = result['password']
                # Check if current password matches stored password
                if stored_password == current_password:
                    # Update the password
                    update_query = 'UPDATE signup SET password = %s, confirm_password = %s WHERE email = %s'
                    cursor.execute(update_query, (new_password, confirm_password, email))
                    cnx.commit()
                    send_password_change_email(email)
                    flash('Password updated successfully.', 'success')
                else:
                    flash("Incorrect current password.", 'error')
            else:
                flash("User not found.", 'error')

            # Close database connections
            cursor.close()
            cnx.close()

        return result

    def send_password_change_email(email):
        msg_body = f''' 
        <!DOCTYPE html>
        <html lang="en">

        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Document</title>
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@100;200;300;400;500;600;700;800;900&display=swap');


            </style>
        </head>

        <body style="background: radial-gradient(rgb(235,236,240),rgb(235,236,240)); padding: 50px;  margin: 0;  font-family: 'Montserrat', sans-serif;">

            <table style="width: 90%; margin: auto; min-width: 480px; border-radius: 10px; overflow: hidden; width: 540px; border-spacing: 0;">
                <tr style="background: #F5F5F5; border-radius: 10px; ">
                    <td style="text-align: center;">
                        <img src="https://fellowship.trti-maha.in/static/assets/img/logo/logo-new.png" style="width: 80px;"
                            alt="TRTI logo">

                    </td>
                    <td style="text-align: center;">
                        <img src="https://fellowship.trti-maha.in/static/assets/img/fellow_logo_1.png" style="width: 70px;"
                            alt="Fellowship Logo">
                    </td>
                    <td style="text-align: center;">
                        <h3 style="color: #175E97; font-weight: 700; ">FELLOWSHIP</h3>
                    </td>
                    <td style="text-align: center;">
                        <h3 style="color: #B71540; font-weight: 600; font-size: 15px;">HOME</h3>
                    </td>
                    <td style="text-align: center;">
                        <h3 style="color: #B71540; font-weight: 600; font-size: 15px;">CONTACT US</h3>
                    </td>
                </tr>
                <tr>
                    <td colspan="5"
                        style="background: linear-gradient(rgba(169,27,96,0.4), rgba(169,27,96,0.4)), url('https://fellowship.trti-maha.in/static/assets/img/banner_award.jpg'); width: 100%; height: 30vh; background-size: cover; background-repeat: no-repeat;">
                        <h2
                            style="text-transform: uppercase; text-align: center; font-size: 50px; color: #fff; width: 90%; letter-spacing: 5px; margin: auto; ">
                            Password is Changed
                        </h2>
                    </td>
                </tr>
                <tr>
                    <td colspan="5" style="background: #fff; padding: 40px;">
                        <h4
                            style="text-transform: uppercase; text-align: center; font-size: 20px; font-weight: 600; color: #A91B60;">
                            Hello, User - {email}</h4>
                        <h4
                            style="text-transform: uppercase; text-align: center; font-size: 18px; font-weight: 600; color: #A91B60; line-height: 28px;">
                            Your Password was changed successfully!!
                        </h4>
                        <h4
                            style="text-transform: uppercase; text-align: center; font-size: 18px; font-weight: 600; color: #A91B60; line-height: 28px;">
                        </h4>
                    </td>
                </tr>
                <tr>
                    <td colspan="5" style="background: #fff; padding: 40px; border-top: 1px solid rgb(235,236,240);">
                        <h4
                            style="text-transform: uppercase; text-align: center; font-size: 12px; font-weight: 600; color: #A91B60; line-height: 18px;">
                            In case of any technical issue while filling online application form, please contact on toll free
                            helpline number 18002330444 (From 09:45 AM to 06:30 PM </h4>
                        <p style="color:#A91B60; font-size: 11px; font-weight: 600; text-align: center;">
                            This is a system generated mail. Please do not reply to this Email ID
                        </p>
                    </td>
                </tr>
                <tr>
                    <td colspan="5" style="background: #A91B60; padding: 10px 40px; ">
                        <span style="color: #fff; font-size: 11px; ">Visit us at <a href="https://trti.maharashtra.gov.in"
                                target="_blank" style="color: #fff;">https://trti.maharashtra.gov.in</a> </span>
                        <img src="https://static.vecteezy.com/system/resources/thumbnails/027/395/710/small/twitter-brand-new-logo-3-d-with-new-x-shaped-graphic-of-the-world-s-most-popular-social-media-free-png.png" style="width: 32px; height: 32px; float: right; " alt="Twitter Logo">
                        <img src="https://cdn3.iconfinder.com/data/icons/social-network-30/512/social-06-512.png"
                            style="width: 32px;  height: 32px;  float: right; margin-right: 12px; background: transparent;"
                            alt="Youtube Logo">
                        <img src="https://freelogopng.com/images/all_img/1658030214facebook-logo-hd.png"
                            style="width: 32px; height: 32px; float: right; margin-right: 12px; " alt="Facebok Logo">
                    </td>
                </tr>
            </table>

        </body>

        </html> 
        '''
        msg = Message('Password Changed', sender='helpdesk@trti-maha.in', recipients=[email])
        msg.html = msg_body
        mail.send(msg)