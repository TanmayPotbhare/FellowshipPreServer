import mysql.connector
from classes.connection import HostConfig, ConnectParam, ConfigPaths
from flask import Blueprint, render_template, session, request, redirect, url_for, flash

genderCounts_blueprint = Blueprint('genderCounts', __name__)


def gendercounts_auth(app):
    # ------ HOST Configs are in classes/connection.py
    host = HostConfig.host
    app_paths = ConfigPaths.paths.get(host)
    if app_paths:
        for key, value in app_paths.items():
            app.config[key] = value


def gender_count(year, gender):
    host = HostConfig.host
    connect_param = ConnectParam(host)
    cnx, cursor = connect_param.connect()

    query = """
    SELECT COUNT(*)
    FROM application_page
    WHERE phd_registration_year = %s AND gender = %s
    """

    cursor.execute(query, (year, gender))
    result = cursor.fetchone()
    cnx.close()

    return result[0]







# def male_count_report():       # ----- To count male users  ------
#     cnx = mysql.connector.connect(user='root', password='A9CALcsd7lc%7ac',
#                                   host=host,
#                                   database='ICSApplication')
#     cursor = cnx.cursor()
#     cursor.execute("SELECT COUNT(*) FROM application_page WHERE gender='male' ")
#     result = cursor.fetchone()
#     print(result)
#     return result[0]
#
#
# def male_count2021():       # ----- To count male users  ------
#     cnx = mysql.connector.connect(user='root', password='A9CALcsd7lc%7ac',
#                                   host=host,
#                                   database='ICSApplication')
#     cursor = cnx.cursor()
#     cursor.execute(" SELECT count(*) FROM application_page where phd_registration_year='2021' and gender='male' ")
#     result = cursor.fetchone()
#     print(result)
#     return result[0]
#
#
# def male_count2022():       # ----- To count male users  ------
#     cnx = mysql.connector.connect(user='root', password='A9CALcsd7lc%7ac',
#                                   host=host,
#                                   database='ICSApplication')
#     cursor = cnx.cursor()
#     cursor.execute(" SELECT COUNT(*) FROM application_page WHERE gender='male' and phd_registration_year='2022' ")
#     result = cursor.fetchone()
#     print(result)
#     return result[0]
#
#
# def male_count2023():       # ----- To count male users  ------
#     cnx = mysql.connector.connect(user='root', password='A9CALcsd7lc%7ac',
#                                   host=host,
#                                   database='ICSApplication')
#     cursor = cnx.cursor()
#     cursor.execute(" SELECT COUNT(*) FROM application_page WHERE gender='male' and phd_registration_year='2023' ")
#     result = cursor.fetchone()
#     print(result)
#     return result[0]
#
#
# def female_count_report():     # ----- To count female users  ------
#     cnx = mysql.connector.connect(user='root', password='A9CALcsd7lc%7ac',
#                                   host=host,
#                                   database='ICSApplication')
#     cursor = cnx.cursor()
#     cursor.execute("SELECT COUNT(*) FROM application_page WHERE gender='female'")
#     result = cursor.fetchone()
#     print(result)
#     return result[0]
#
#
# def female_count2021():     # ----- To count female users  ------
#     cnx = mysql.connector.connect(user='root', password='A9CALcsd7lc%7ac',
#                                   host=host,
#                                   database='ICSApplication')
#     cursor = cnx.cursor()
#     cursor.execute("SELECT COUNT(*) FROM application_page WHERE gender='female' and phd_registration_year='2021' ")
#     result = cursor.fetchone()
#     print(result)
#     return result[0]
#
#
# def female_count2022():     # ----- To count female users  ------
#     cnx = mysql.connector.connect(user='root', password='A9CALcsd7lc%7ac',
#                                   host=host,
#                                   database='ICSApplication')
#     cursor = cnx.cursor()
#     cursor.execute("SELECT COUNT(*) FROM application_page WHERE gender='female' and phd_registration_year='2022' ")
#     result = cursor.fetchone()
#     print(result)
#     return result[0]
#
#
# def female_count2023():     # ----- To count female users  ------
#     cnx = mysql.connector.connect(user='root', password='A9CALcsd7lc%7ac',
#                                   host=host,
#                                   database='ICSApplication')
#     cursor = cnx.cursor()
#     cursor.execute("SELECT COUNT(*) FROM application_page WHERE gender='female' and phd_registration_year='2023' ")
#     result = cursor.fetchone()
#     print(result)
#     return result[0]
#
#
# def trans_count_report():       # ----- To count trans_gender users  ------
#     cnx = mysql.connector.connect(user='root', password='A9CALcsd7lc%7ac',
#                                   host=host,
#                                   database='ICSApplication')
#     cursor = cnx.cursor()
#     cursor.execute("SELECT COUNT(*) FROM application_page WHERE gender='other'")
#     result = cursor.fetchone()
#     print(result)
#     return result[0]
