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
        print("result:", result)
        startDate = result[0]['final_approved_date']
        print("Start Date:", startDate)

        cursor.execute("SELECT * FROM payment_sheet WHERE email=%s", (email,))
        record = cursor.fetchall()
        print("record:", record)
        table_data = []

        for row in record:
            total_months = int(row['total_months'])
            print("Total Months:", total_months)
            start_date = startDate
            print("Start Date:", start_date)
            end_date = datetime.strptime(row['duration_date_to'], '%Y-%m-%d')
            print("End Date:", end_date)

            # First installment
            table_data.append({
                'sr_no': 1,
                'period': total_months,
                'start_period': start_date.strftime('%Y-%m-%d'),
                'end_period': end_date.strftime('%Y-%m-%d'),
                'due_date': (end_date + timedelta(days=60)).strftime('%Y-%m-%d'),
                'balance': 31000,
                'installment_number': 1,
                'paid': row['paid_or_not_installment_1']  # Assumes 'paid_or_not_installment_1' is a key in 'row'
            })

            # Generate next two installments
            for i in range(2, 4):
                next_start_date = end_date + timedelta(days=30 * (i - 1))
                next_end_date = next_start_date + timedelta(days=90)
                table_data.append({
                    'sr_no': i,
                    'period': total_months,
                    'start_period': next_start_date.strftime('%Y-%m-%d'),
                    'end_period': next_end_date.strftime('%Y-%m-%d'),
                    'due_date': (next_end_date + timedelta(days=60)).strftime('%Y-%m-%d'),
                    'balance': 31000,
                    'installment_number': i,
                    'paid': row[f'paid_or_not_installment_{i}']  # Adjust this based on your payment status logic
                })

            print('table_data:', table_data)
            total_period = sum(int(item['period']) for item in table_data)
            total_balance = sum(int(item['balance']) for item in table_data)
            print("Total Period:", total_period)

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
                               table_data=table_data, total_period=total_period, total_balance=total_balance,
                               # approve_pay=approve_pay
                               )

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