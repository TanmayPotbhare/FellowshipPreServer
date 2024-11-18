from datetime import date, timedelta, datetime
import mysql.connector
from Classes.database import HostConfig, ConfigPaths, ConnectParam
import os
from flask_mail import Mail, Message
from flask import Blueprint, render_template, session, request, redirect, url_for, flash
from Authentication.middleware import auth

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
            return redirect(url_for('admin_login'))
        user_records = []
        if request.method == 'GET':
            # Establish a database connection
            host = HostConfig.host
            connect_param = ConnectParam(host)
            cnx, cursor = connect_param.connect(use_dict=True)
            # print('I have made connection')

            # Fetch user data based on the email
            cursor.execute("""

                        SELECT * 
                        FROM application_page 
                        WHERE final_approval = 'accepted' 
                          AND phd_registration_year >= '2023'

                        UNION

                        SELECT * 
                        FROM application_page 
                        WHERE phd_registration_year > '2020' 
                          AND aadesh = 1;

            """)
            user_data = cursor.fetchall()  # Use fetchall to retrieve all rows
            # print('user data:', user_data)

            for row in user_data:
                # Calculate values based on user data
                applicant_id = row['applicant_id']
                faculty = row["faculty"]
                # print('faculty', faculty)
                joining_date = row["phd_registration_date"]
                city = row['city']
                bank_name = row['bank_name']
                account_number = row['account_number']
                ifsc = row['ifsc_code']
                year = '2023'
                # print(joining_date)

                # Calculate Count Yearly
                if faculty == "Arts":
                    count_yearly = 20500
                elif faculty == "Law":
                    count_yearly = 20500
                elif faculty == "Commerce":
                    count_yearly = 20500
                elif faculty == "Other":
                    count_yearly = 20500
                elif faculty == "Science":
                    count_yearly = 25000
                else:
                    count_yearly = 0  # Handle other faculty values as needed

                if city in ['Ahmedabad', 'Bengaluru', 'Chennai', 'Delhi', 'Hyderabad', 'Kolkata', 'Mumbai', 'Pune']:
                    rate = '30%'
                elif city in ['Agra', 'Ajmer', 'Aligarh', 'Amravati', 'Amritsar', 'Anand', 'Asansol', 'Aurangabad',
                              'Bareilly',
                              'Belagavi', 'Brahmapur', 'Bhavnagar', 'Bhiwandi', 'Bhopal', 'Bhubaneswar', 'Bikaner',
                              'Bilaspur',
                              'Bokaro Steel City', 'Burdwan', 'Chandigarh', 'Coimbatore', 'Cuttack', 'Dahod',
                              'Dehradun',
                              'Dombivli',
                              'Dhanbad', 'Bhilai', 'Durgapur', 'Erode', 'Faridabad', 'Ghaziabad', 'Gorakhpur', 'Guntur',
                              'Gurgaon',
                              'Guwahati', 'Gwalior', 'Hamirpur', 'Hubballi–Dharwad', 'Indore', 'Jabalpur', 'Jaipur',
                              'Jalandhar',
                              'Jalgaon', 'Jammu', 'Jamshedpur', 'Jhansi', 'Jodhpur', 'Kalaburagi', 'Kakinada', 'Kannur',
                              'Kanpur',
                              'Karnal', 'Kochi', 'Kolhapur', 'Kollam', 'Kota', 'Kozhikode', 'Kumbakonam', 'Kurnool',
                              'Ludhiana',
                              'Lucknow', 'Madurai', 'Malappuram', 'Mathura', 'Mangaluru', 'Meerut', 'Moradabad',
                              'Mysuru',
                              'Nagpur',
                              'Nanded', 'Nadiad', 'Nashik', 'Nellore', 'Noida', 'Patna', 'Puducherry', 'Purlia',
                              'Prayagraj', 'Raipur',
                              'Rajkot', 'Rajamahendravaram', 'Ranchi', 'Rourkela', 'Ratlam', 'Saharanpur', 'Salem',
                              'Sangli', 'Shimla',
                              'Siliguri', 'Solapur', 'Srinagar', 'Surat', 'Thanjavur', 'Thiruvananthapuram', 'Thrissur',
                              'Tiruchirappalli', 'Tirunelveli', 'Tiruvannamalai', 'Ujjain', 'Vijayapura', 'Vadodara',
                              'Varanasi',
                              'Vasai-Virar', 'Vijayawada', 'Visakhapatnam', 'Vellore', 'Warangal']:
                    rate = '20%'
                else:
                    rate = '10%'

                # print("Rate:", rate)

                # Initialize the "from" and "to" date to empty strings
                duration_date_from = ""
                duration_date_to = ""

                if joining_date:  # Check if joining_date is not None
                    # Calculate Duration Date (adding 3 months to joining date)
                    duration_date_from = joining_date  # Assuming this is a datetime object
                    duration_date_to = joining_date + timedelta(days=90)  # Adding 90 days to joining date
                    # Extract day, month, and year
                    day = duration_date_to.day
                    month = duration_date_to.month
                    year = duration_date_to.year

                    # Print the stripped day, month, and year
                    # print(f"Day: {day}, Month: {month}, Year: {year}")
                    # Format the dates for display in the desired format
                    duration_date_from_str = duration_date_from.strftime('%d/%m/%Y')  # "17 Aug 2023"
                    duration_date_to_str = duration_date_to.strftime('%d/%m/%Y')  # "15 Nov 2023"

                # Calculate Total Months
                total_months = 3

                # Calculate Fellowship
                fellowship = 42000  # Fixed value for 3 months

                # Calculate Total Fellowship
                total_fellowship = fellowship * total_months

                rate_str = float(rate.rstrip('%'))
                convert_rate = (rate_str / 100)
                hra_amount = convert_rate * fellowship

                months = total_months

                total_hra = hra_amount * months

                total = total_fellowship + total_hra

                # Calculate the date 2 years after duration_date_from
                two_years_later = duration_date_from + timedelta(days=730)  # 2 years = 730 days

                joiningDate = row['phd_registration_date'].strftime('%d/%m/%Y')

                # Get the current date
                current_date = datetime.now().date()

                # Check the category based on 2 years difference
                if current_date >= two_years_later:
                    category = "SRF"  # Senior Research Fellowship
                else:
                    category = "JRF"  # Junior Research Fellowship

                # Create a record dictionary for the user
                record = {
                    "applicant_id": row['applicant_id'],
                    "full_name": str(row['first_name']) + ' ' + str(row['middle_name']) + ' ' + str(row['last_name']),
                    "first_name": row['first_name'],
                    "last_name": row['last_name'],
                    "middle_name": row['middle_name'],
                    "email": row["email"],
                    "faculty": row['faculty'],
                    "joining_date": joiningDate,
                    "city": row['city'],
                    "duration": f"{duration_date_from_str} <span class='fw-bold'>to</span> {duration_date_to_str}",
                    "rate": rate,
                    "count": count_yearly,
                    "amount": hra_amount,
                    "months": months,
                    "total_hra": total_hra,
                    "total": total,
                    "duration_date_from": duration_date_from,
                    "duration_date_to": duration_date_to,
                    "duration_day": day,
                    "duration_month": month,
                    "duration_year": year,
                    "total_months": total_months,
                    "fellowship": fellowship,
                    "to_fellowship": total_fellowship,
                    "phd_registration_year": row['phd_registration_year'],
                    "id": row['id'],
                    "account_number": account_number,
                    "ifsc": ifsc,
                    "bank_name": bank_name,
                    "year": year,
                    "jrf_srf": category
                }

                user_records.append(record)

                email = record['email']

                host = HostConfig.host
                connect_param = ConnectParam(host)
                cnx, cursor = connect_param.connect()

                cursor.execute(" SELECT * FROM payment_sheet where email=%s", (email,))
                result = cursor.fetchone()

                if result:
                    pass
                    # print("Existing Record:", email)
                    # Record already exists, do not insert again
                else:
                    # print("Record not found, proceeding with the INSERT query")
                    # Insert values into the payment_sheet table
                    host = HostConfig.host
                    connect_param = ConnectParam(host)
                    cnx, cursor = connect_param.connect()

                    insert_query = """
                        INSERT INTO payment_sheet (
                            full_name, faculty, city, date, jrf_srf, duration_date_from, duration_date_to, duration_day, duration_month, duration_year, 
                            rate, count, amount, months, total_hra, total,
                            total_months, fellowship,
                            to_fellowship, bank_name, ifsc_code, account_number, fellowship_awarded_year, email
                        )
                        VALUES (%(full_name)s, %(faculty)s, %(city)s, %(joining_date)s, %(jrf_srf)s, %(duration_date_from)s, %(duration_date_to)s,
                                %(duration_day)s, %(duration_month)s, %(duration_year)s,
                                %(rate)s, %(count)s, %(amount)s, %(months)s, %(total_hra)s, %(total)s, 
                                %(total_months)s, %(fellowship)s, %(to_fellowship)s, %(bank_name)s, %(ifsc)s,
                                %(account_number)s, %(year)s, %(email)s)         
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

        return render_template('AdminPages/PaymentSheet/payment_sheet.html', user_records=user_records)