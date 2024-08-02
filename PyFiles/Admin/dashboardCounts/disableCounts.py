import mysql.connector
from classes.connection import HostConfig, ConfigPaths, ConnectParam
import os
from flask import Blueprint, render_template, session, request, redirect, url_for, flash
from authentication.middleware import auth


disabilityCount_blueprint = Blueprint('disabilityCount', __name__)


def disabilityCount_auth(app):
    # ------ HOST Configs are in classes/connection.py
    host = HostConfig.host
    app_paths = ConfigPaths.paths.get(host)
    if app_paths:
        for key, value in app_paths.items():
            app.config[key] = value


def disability_no_count_report():       # ----- To count users with NO disability  ------
    host = HostConfig.host
    connect_param = ConnectParam(host)
    cnx, cursor = connect_param.connect()
    cursor.execute("SELECT COUNT(*) FROM application_page WHERE disability='no'")
    result = cursor.fetchone()
    print(result)
    return result[0]


disabilityCount_blueprint.disability_no_count_report = disability_no_count_report


def disability_yes_count_report():       # ----- To count users with NO disability  ------
    host = HostConfig.host
    connect_param = ConnectParam(host)
    cnx, cursor = connect_param.connect()
    cursor.execute("SELECT COUNT(*) FROM application_page WHERE disability='Yes'")
    result = cursor.fetchone()
    print(result)
    return result[0]


disabilityCount_blueprint.disability_yes_count_report = disability_yes_count_report