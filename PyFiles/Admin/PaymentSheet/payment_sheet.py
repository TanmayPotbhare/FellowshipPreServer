from datetime import date, timedelta, datetime
import mysql.connector
from classes.connection import HostConfig, ConfigPaths, ConnectParam
import os
from flask_mail import Mail, Message
from flask import Blueprint, render_template, session, request, redirect, url_for, flash
from authentication.middleware import auth

payment_sheet_blueprint = Blueprint('payment_sheet', __name__)


def payment_sheet_auth(app):
    # ------ HOST Configs are in classes/connection.py
    host = HostConfig.host
    app_paths = ConfigPaths.paths.get(host)
    if app_paths:
        for key, value in app_paths.items():
            app.config[key] = value

    @payment_sheet_blueprint.route('/payment_sheet', methods=['GET', 'POST'])
    def payment_sheet():
        if not session.get('logged_in'):
            # Redirect to the admin login page if the user is not logged in
            return redirect(url_for('adminlogin.admin_login'))
        user_records = []
        if request.method == 'GET':
            # Establish a database connection
            host = HostConfig.host
            connect_param = ConnectParam(host)
            cnx, cursor = connect_param.connect(use_dict=True)

            # Fetch user data based on the email
            cursor.execute(
                "SELECT * FROM application_page where final_approval='accepted' and phd_registration_year>='2023' ")
            user_data = cursor.fetchall()  # Use fetchall to retrieve all rows

            for row in user_data:
                # Calculate values based on user data
                applicant_id = row['applicant_id']
                faculty = row["faculty"]

                joining_date = row["phd_registration_date"]
                city = row['city']


                # Calculate Count Yearly
                if faculty == "Arts":
                    count_yearly = 20500
                elif faculty == "Other":
                    count_yearly = 20500
                elif faculty == "Commerce":
                    count_yearly = 20500
                elif faculty == "Science":
                    count_yearly = 25000
                else:
                    count_yearly = 0  # Handle other faculty values as needed

                if city in ['AHMEDABAD', 'BENGALURU', 'CHENNAI', 'DELHI', 'HYDERABAD', 'KOLKATA', 'MUMBAI', 'PUNE']:
                    rate = '24%'
                elif city in ['AGRA', 'AJMER', 'ALIGARH', 'AMRAVATI', 'AMRITSAR', 'ANAND', 'ASANSOL', 'AURANGABAD',
                              'BAREILLY', 'BELAGAVI', 'BRAHMAPUR', 'BHAVNAGAR', 'BHIWANDI', 'BHOPAL', 'BHUBANESWAR',
                              'BIKANER', 'BILASPUR', 'BOKARO STEEL CITY', 'BURDWAN', 'CHANDIGARH', 'COIMBATORE',
                              'CUTTACK',
                              'DAHOD', 'DEHRADUN', 'DOMBIVLI', 'DHANBAD', 'BHILAI', 'DURGAPUR', 'ERODE', 'FARIDABAD',
                              'GHAZIABAD', 'GORAKHPUR', 'GUNTUR', 'GURGAON', 'GUWAHATI', 'GWALIOR', 'HAMIRPUR',
                              'HUBBALLI–DHARWAD', 'INDORE', 'JABALPUR', 'JAIPUR', 'JALANDHAR', 'JALGAON', 'JAMMU',
                              'JAMSHEDPUR', 'JHANSI', 'JODHPUR', 'KALABURAGI', 'KAKINADA', 'KANNUR', 'KANPUR', 'KARNAL',
                              'KOCHI', 'KOLHAPUR', 'KOLLAM', 'KOTA', 'KOZHIKODE', 'KUMBAKONAM', 'KURNOOL', 'LUDHIANA',
                              'LUCKNOW', 'MADURAI', 'MALAPPURAM', 'MATHURA', 'MANGALURU', 'MEERUT', 'MORADABAD',
                              'MYSURU',
                              'NAGPUR', 'NANDED', 'NADIAD', 'NASHIK', 'NELLORE', 'NOIDA', 'PATNA', 'PUDUCHERRY',
                              'PURLIA',
                              'PRAYAGRAJ', 'RAIPUR', 'RAJKOT', 'RAJAMAHENDRAVARAM', 'RANCHI', 'ROURKELA', 'RATLAM',
                              'SAHARANPUR', 'SALEM', 'SANGLI', 'SHIMLA', 'SILIGURI', 'SOLAPUR', 'SRINAGAR', 'SURAT',
                              'THANJAVUR', 'THIRUVANANTHAPURAM', 'THRISSUR', 'TIRUCHIRAPPALLI', 'TIRUNELVELI',
                              'TIRUVANNAMALAI', 'UJJAIN', 'VIJAYAPURA', 'VADODARA', 'VARANASI', 'VASAI-VIRAR',
                              'VIJAYAWADA',
                              'VISAKHAPATNAM', 'VELLORE', 'WARANGAL']:
                    rate = '16%'
                else:
                    rate = '8%'


                # Initialize the "from" and "to" date to empty strings
                duration_date_from = ""
                duration_date_to = ""

                if joining_date:  # Check if joining_date is not None
                    # The "from" date is the final approved date as a datetime object
                    duration_from = row['final_approved_date']  # Ensure this is used correctly


                    # Calculate Duration Date (adding 3 months to the final approved date)
                    duration_to = duration_from + timedelta(days=90)

                    # Format both dates as strings if needed
                    duration_date_from = duration_from.strftime('%Y-%m-%d')
                    duration_date_to = duration_to.strftime('%Y-%m-%d')

                # Calculate Total Months
                total_months = 3

                # Calculate Fellowship
                fellowship = 31000  # Fixed value for 3 months

                # Calculate Total Fellowship
                total_fellowship = fellowship * total_months

                rate_str = float(rate.rstrip('%'))
                convert_rate = (rate_str / 100)
                hra_amount = convert_rate * fellowship

                months = total_months

                total_hra = hra_amount * months

                total = total_fellowship + total_hra

                period_installment_1 = '3 Months'
                period_installment_2 = '3 Months'
                period_installment_3 = '3 Months'

                # Create a record dictionary for the user
                record = {
                    "applicant_id": row['applicant_id'],
                    "full_name": str(row['first_name']) + ' ' + str(row['last_name']),
                    "first_name": row['first_name'],
                    "last_name": row['last_name'],
                    "email": row["email"],
                    "faculty": row['faculty'],
                    "joining_date": row['phd_registration_date'],
                    "city": row['city'],
                    "duration": duration_date_from + ' ' + duration_date_to,
                    "rate": rate,
                    "count": count_yearly,
                    "amount": hra_amount,
                    "months": months,
                    "total_hra": total_hra,
                    "total": total,
                    "duration_date_from": duration_date_from,
                    "duration_date_to": duration_date_to,
                    "total_months": total_months,
                    "fellowship": fellowship,
                    "to_fellowship": total_fellowship,
                    "phd_registration_year": row['phd_registration_year'],
                    "id": row['id'],
                    'period_installment_1': period_installment_1,
                    'period_installment_2': period_installment_2,
                    'period_installment_3': period_installment_3,
                    'balance_installment_1': 31000,
                    'balance_installment_2': 31000,
                    'balance_installment_3': 31000
                }

                user_records.append(record)

                email = record['email']

                host = HostConfig.host
                connect_param = ConnectParam(host)
                cnx, cursor = connect_param.connect(use_dict=True)

                cursor.execute(" SELECT * FROM payment_sheet where email=%s", (email,))
                result = cursor.fetchone()

                if result:
                    pass
                    # Record already exists, do not insert again
                else:
                    # Insert values into the payment_sheet table
                    insert_query = """
                        INSERT INTO payment_sheet (
                            full_name, faculty, city, duration_date_from, duration_date_to,
                            rate, count, amount, months, total_hra, total,
                            total_months, fellowship,
                            to_fellowship, email, 
                            period_installment_1, period_installment_2, period_installment_3, 
                            balance_installment_1, balance_installment_2, balance_installment_3
                        )
                        VALUES (
                            %(full_name)s, %(faculty)s, %(city)s, %(duration_date_from)s, %(duration_date_to)s,
                            %(rate)s, %(count)s, %(amount)s, %(months)s, %(total_hra)s, %(total)s, 
                            %(total_months)s, %(fellowship)s, %(to_fellowship)s, %(email)s, 
                            %(period_installment_1)s, %(period_installment_2)s, %(period_installment_3)s,
                            %(balance_installment_1)s, %(balance_installment_2)s, %(balance_installment_3)s
                        )       
                    """
                    # Execute the INSERT query

                    cursor.execute(insert_query, record)

                    # Commit the changes to the database
                    cnx.commit()

                # Close the database cursor and connection
                cursor.close()
                cnx.close()
            # Close the database cursor and connection
            cursor.close()
            cnx.close()

        return render_template('Admin/PaymentSheet/payment_sheet.html', user_records=user_records)