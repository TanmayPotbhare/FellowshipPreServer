import mysql.connector
from classes.connection import HostConfig, ConfigPaths, ConnectParam
import os
from flask import Blueprint, render_template, session, request, redirect, url_for, flash
from authentication.middleware import auth


applCounts_blueprint = Blueprint('applCounts', __name__)


def applCounts_auth(app):
    # ------ HOST Configs are in classes/connection.py
    host = HostConfig.host
    app_paths = ConfigPaths.paths.get(host)
    if app_paths:
        for key, value in app_paths.items():
            app.config[key] = value


def applications_today():
    host = HostConfig.host
    connect_param = ConnectParam(host)
    cnx, cursor = connect_param.connect()
    cursor.execute(" SELECT COUNT(*) FROM application_page ")
    result = cursor.fetchone()
    print(result)
    return result[0]


applCounts_blueprint.applications_today = applications_today


def accepted_applications():    # ----- To count accepted applications  ------
    host = HostConfig.host
    connect_param = ConnectParam(host)
    cnx, cursor = connect_param.connect()
    cursor.execute(" SELECT COUNT(*) FROM application_page WHERE final_approval='accepted' ")
    result = cursor.fetchone()
    print(result)
    return result[0]


applCounts_blueprint.accepted_applications = accepted_applications


def form_filled_applications():
    host = HostConfig.host
    connect_param = ConnectParam(host)
    cnx, cursor = connect_param.connect()
    cursor.execute(" SELECT COUNT(*) FROM application_page where form_filled='1' and phd_registration_year>='2023' ")
    result = cursor.fetchone()
    print(result)
    return result[0]


applCounts_blueprint.form_filled_applications = form_filled_applications


def form_incomplete_applications():
    host = HostConfig.host
    connect_param = ConnectParam(host)
    cnx, cursor = connect_param.connect()
    cursor.execute(" SELECT COUNT(*) FROM application_page where form_filled='0' and phd_registration_year>='2023' ")
    result = cursor.fetchone()
    print(result)
    return result[0]


applCounts_blueprint.form_incomplete_applications = form_incomplete_applications


def year_wise_applications(year, month):
    host = HostConfig.host
    connect_param = ConnectParam(host)
    cnx, cursor = connect_param.connect()

    query = """
    SELECT gender, COUNT(*) AS count
    FROM application_page
    WHERE phd_registration_year = %s AND phd_registration_month = %s
    GROUP BY gender
    """

    cursor.execute(query, (year, month))
    results = cursor.fetchall()
    cnx.close()

    if not results:
        return {}

    # Convert results to a dictionary
    return {row[0]: row[1] for row in results}  # row[0] is gender, row[1] is count


applCounts_blueprint.year_wise_applications = year_wise_applications


def fetch_counts():
    accepted_counts = {year: {} for year in [2021, 2022, 2023, 2024]}

    for year in accepted_counts.keys():
        for month in range(1, 13):
            counts = year_wise_applications(year, month)
            accepted_counts[year][month] = counts

    maleDataByYear = {
        year: [accepted_counts[year].get(month, {}).get('male', 0) for month in range(1, 13)]
        for year in accepted_counts
    }

    femaleDataByYear = {
        year: [accepted_counts[year].get(month, {}).get('female', 0) for month in range(1, 13)]
        for year in accepted_counts
    }

    return maleDataByYear, femaleDataByYear

def rejected_applications():    # ----- To count accepted applications  ------
    host = HostConfig.host
    connect_param = ConnectParam(host)
    cnx, cursor = connect_param.connect()
    cursor.execute(" SELECT COUNT(*) FROM application_page WHERE final_approval='rejected' ")
    result = cursor.fetchone()
    print(result)
    return result[0]


applCounts_blueprint.rejected_applications = rejected_applications


def year_twentyone_count():      #----- To count users from 2021
    host = HostConfig.host
    connect_param = ConnectParam(host)
    cnx, cursor = connect_param.connect()
    cursor.execute("SELECT COUNT(*) FROM application_page WHERE phd_registration_year='2021'")
    result = cursor.fetchone()
    print(result)
    return result[0]


applCounts_blueprint.year_twentyone_count = year_twentyone_count


def year_twentytwo_count():       #----- To count users from 2022
    host = HostConfig.host
    connect_param = ConnectParam(host)
    cnx, cursor = connect_param.connect()
    cursor.execute("SELECT COUNT(*) FROM application_page WHERE phd_registration_year='2022'")
    result = cursor.fetchone()
    print(result)
    return result[0]


applCounts_blueprint.year_twentytwo_count = year_twentytwo_count


def year_twentythree_count():     #----- To count users from 2023
    host = HostConfig.host
    connect_param = ConnectParam(host)
    cnx, cursor = connect_param.connect()
    cursor.execute("SELECT COUNT(*) FROM application_page WHERE phd_registration_year='2023'")
    result = cursor.fetchone()
    print(result)
    return result[0]


applCounts_blueprint.year_twentythree_count = year_twentythree_count


def accept_twentythree_count():     #----- To count users from 2023
    host = HostConfig.host
    connect_param = ConnectParam(host)
    cnx, cursor = connect_param.connect()
    cursor.execute("SELECT COUNT(*) FROM application_page WHERE phd_registration_year='2023' and final_approval='accepted' ")
    result = cursor.fetchone()
    print(result)
    return result[0]


applCounts_blueprint.accept_twentythree_count = accept_twentythree_count


def reject_twentythree_count():     #----- To count users from 2023
    host = HostConfig.host
    connect_param = ConnectParam(host)
    cnx, cursor = connect_param.connect()
    cursor.execute("SELECT COUNT(*) FROM application_page WHERE phd_registration_year='2023' and final_approval='rejected' ")
    result = cursor.fetchone()
    print(result)
    return result[0]


applCounts_blueprint.reject_twentythree_count = reject_twentythree_count


def old_users_count_2021():                                                  #----- To count old users
    host = HostConfig.host
    connect_param = ConnectParam(host)
    cnx, cursor = connect_param.connect()
    cursor.execute("SELECT COUNT(*) FROM old_users where phd_registration_year='2021'")
    result = cursor.fetchone()
    print(result)
    return result[0]


applCounts_blueprint.old_users_count_2021 = old_users_count_2021


def old_users_count_2022():                                                  #----- To count old users
    host = HostConfig.host
    connect_param = ConnectParam(host)
    cnx, cursor = connect_param.connect()
    cursor.execute("SELECT COUNT(*) FROM old_users where phd_registration_year='2022'")
    result = cursor.fetchone()
    print(result)
    return result[0]


applCounts_blueprint.old_users_count_2022 = old_users_count_2022


def old_users_count_2022_accepted():                                                  #----- To count old users
    host = HostConfig.host
    connect_param = ConnectParam(host)
    cnx, cursor = connect_param.connect()
    cursor.execute("SELECT COUNT(*) FROM application_page where final_approval='accepted' AND phd_registration_year='2022'")
    result = cursor.fetchone()
    print(result)
    return result[0]


applCounts_blueprint.old_users_count_2022_accepted = old_users_count_2022_accepted


def old_users_count_2021_accepted():                                                  #----- To count old users
    host = HostConfig.host
    connect_param = ConnectParam(host)
    cnx, cursor = connect_param.connect()
    cursor.execute("SELECT COUNT(*) FROM application_page where final_approval='accepted' AND phd_registration_year='2021'")
    result = cursor.fetchone()
    print(result)
    return result[0]


applCounts_blueprint.old_users_count_2021_accepted = old_users_count_2021_accepted


def priority_by_caste():              # ----- To count users with caste "Katkari , Kolam , madia"------
    host = HostConfig.host
    connect_param = ConnectParam(host)
    cnx, cursor = connect_param.connect(use_dict=True)  # Pass the use_dict flag here
    cursor.execute("SELECT * FROM application_page WHERE your_caste IN ('katkari', 'kolam', 'madia')")
    result = cursor.fetchall()
    print(result)
    return result


applCounts_blueprint.priority_by_caste = priority_by_caste
