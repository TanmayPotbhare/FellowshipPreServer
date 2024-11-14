from datetime import date, timedelta, datetime
import mysql.connector
from classes.connection import HostConfig, ConfigPaths, ConnectParam
import os
from flask_mail import Mail, Message
from flask import Blueprint, render_template, session, request, redirect, url_for, flash
from authentication.middleware import auth

installments_blueprint = Blueprint('installments', __name__)


def installments_auth(app):
    # ------ HOST Configs are in classes/connection.py
    host = HostConfig.host
    app_paths = ConfigPaths.paths.get(host)
    if app_paths:
        for key, value in app_paths.items():
            app.config[key] = value

    @installments_blueprint.route('/installment_userpage', methods=['GET', 'POST'])
    def installment_userpage():
        email = session['email']

        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)

        cursor.execute("SELECT * FROM application_page WHERE email=%s", (email,))
        result = cursor.fetchall()
        year = result[0]['phd_registration_year']
        startDate = result[0]['final_approved_date']
        if result:
            user = result[0]['first_name']
        else:
            user = 'Admin'

        cursor.execute("SELECT * FROM installments WHERE email=%s", (email,))
        installments = cursor.fetchone()
        print(installments)

        cursor.execute("SELECT * FROM payment_sheet WHERE email=%s", (email,))
        record = cursor.fetchall()

        for row in record:
            total_months = int(row['total_months'])
            start_date = startDate
            end_date = datetime.strptime(row['duration_date_to'], '%Y-%m-%d')

            # First Installment
            installment_1 = {
                'sr_no': 1,
                'period': total_months,
                'start_period': start_date.strftime('%Y-%m-%d'),
                'end_period': end_date.strftime('%Y-%m-%d'),
                'due_date': (end_date + timedelta(days=60)).strftime('%Y-%m-%d'),
                'balance': 31000,
                'installment_number': 1,
                'paid': row['paid_or_not_installment_1']
            }

            # Second Installment
            next_start_date_2 = end_date + timedelta(days=30)
            next_end_date_2 = next_start_date_2 + timedelta(days=90)
            installment_2 = {
                'sr_no': 2,
                'period': total_months,
                'start_period': next_start_date_2.strftime('%Y-%m-%d'),
                'end_period': next_end_date_2.strftime('%Y-%m-%d'),
                'due_date': (next_end_date_2 + timedelta(days=60)).strftime('%Y-%m-%d'),
                'balance': 31000,
                'installment_number': 2,
                'paid': row['paid_or_not_installment_1']
            }

            # Third Installment
            next_start_date_3 = next_end_date_2 + timedelta(days=30)
            next_end_date_3 = next_start_date_3 + timedelta(days=90)
            installment_3 = {
                'sr_no': 3,
                'period': total_months,
                'start_period': next_start_date_3.strftime('%Y-%m-%d'),
                'end_period': next_end_date_3.strftime('%Y-%m-%d'),
                'due_date': (next_end_date_3 + timedelta(days=60)).strftime('%Y-%m-%d'),
                'balance': 31000,
                'installment_number': 3,
                'paid': row['paid_or_not_installment_1']
            }

            total_period = installment_1['period'] + installment_2['period'] + installment_3['period']
            total_balance = installment_1['balance'] + installment_2['balance'] + installment_3['balance']

        # approve_pay = approve_payment(email)

        cursor.execute("SELECT * FROM award_letter WHERE email=%s", (email,))
        solution = cursor.fetchall()
        print("solution:", solution)

        cursor.execute("SELECT fellowship_withdrawn FROM signup WHERE email=%s", (email,))
        output = cursor.fetchall()
        print("output:", output)

        cnx.commit()
        cursor.close()
        cnx.close()

        return render_template('Candidate/AcceptedUserDashboard/Installments/installment_userpage.html',
                               result=result, record=record, output=output, solution=solution,
                               installment_1=installment_1,
                               installment_2=installment_2,
                               installment_3=installment_3, total_period=total_period, total_balance=total_balance,
                               year=year, installments=installments, user=user)

    def approve_payment(email):
        cnx = mysql.connector.connect(user='root', password='A9CALcsd7lc%7ac',
                                      host=host,
                                      database='ICSApplication')
        cursor = cnx.cursor(dictionary=True)
        # Update the 'paid' column for the specified email
        cursor.execute("UPDATE payment_sheet SET paid_or_not_installment_1='Paid' WHERE email=%s", (email,))
        cnx.commit()
        cursor.close()
        cnx.close()

    @installments_blueprint.route('/submit_installments', methods=['GET', 'POST'])
    def submit_installments():
        host = HostConfig.host
        connect_param = ConnectParam(host)
        cnx, cursor = connect_param.connect(use_dict=True)

        if request.method == 'POST':
            email = session.get('email')  # Use .get() to avoid KeyError if 'email' is not in session
            start_period = request.form.get('start_period')
            end_period = request.form.get('end_period')
            recieved_pay = request.form.get('recieved_pay')
            recieved_date = request.form.get('recieved_date')

            try:
                # Check if the email already exists in the installments table
                check_query = "SELECT * FROM installments WHERE email = %s"
                cursor.execute(check_query, (email,))
                result = cursor.fetchone()

                if result:
                    # Check if each installment slot is completely filled
                    installment_2_filled = (result['start_period_2'] and
                                            result['end_period_2'] and
                                            result['recieved_pay_2'] and
                                            result['recieved_date_2'])
                    installment_3_filled = (result['start_period_3'] and
                                            result['end_period_3'] and
                                            result['recieved_payy_3'] and
                                            result['recieved_date_3'])
                    installment_4_filled = (result['start_period_4'] and
                                            result['end_period_4'] and
                                            result['recieved_pay_4'] and
                                            result['recieved_date_4'])

                    if not installment_2_filled:
                        update_query = """
                            UPDATE installments
                            SET inst_num_2 = %s, start_period_2 = %s, end_period_2 = %s, 
                                recieved_pay_2 = %s, recieved_date_2 = %s, status_paid_2 = %s
                            WHERE email = %s
                        """
                        values = (2, start_period, end_period, recieved_pay, recieved_date, 'Paid', email)
                    elif not installment_3_filled:
                        update_query = """
                            UPDATE installments
                            SET inst_num_3 = %s, start_period_3 = %s, end_period_3 = %s, 
                                recieved_pay_3 = %s, recieved_date_3 = %s, status_paid_3 = %s
                            WHERE email = %s
                        """
                        values = (3, start_period, end_period, recieved_pay, recieved_date, 'Paid', email)
                    elif not installment_4_filled:
                        update_query = """
                            UPDATE installments
                            SET inst_num_4 = %s, start_period_4 = %s, end_period_4 = %s, 
                                recieved_pay_4 = %s, recieved_date_4 = %s, status_paid_4 = %s
                            WHERE email = %s
                        """
                        values = (4, start_period, end_period, recieved_pay, recieved_date, 'Paid', email)
                    else:
                        return "Maximum installments reached", 400

                    cursor.execute(update_query, values)
                    message = "Installment updated successfully"
                    flash(message, 'success')
                else:
                    # If email does not exist, insert a new record
                    insert_query = """
                        INSERT INTO installments (email, inst_num, start_period, end_period, 
                                                  recieved_pay, recieved_date, status_paid)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """
                    values = (email, 1, start_period, end_period, recieved_pay, recieved_date, 'Paid')
                    cursor.execute(insert_query, values)
                    message = "Installment submitted successfully"
                    flash(message, 'success')

                cnx.commit()
                return redirect(url_for('installments.installment_userpage'))
            except Exception as e:
                cnx.rollback()
                return f"An error occurred: {str(e)}", 500
            finally:
                cursor.close()
                cnx.close()

        return redirect(url_for('installments.installment_userpage'))
