import mysql.connector
from classes.connection import HostConfig, ConfigPaths, ConnectParam
import os
from flask import Blueprint, render_template, session, request, redirect, url_for, flash
from authentication.middleware import auth


pvtgCounts_blueprint = Blueprint('pvtgCounts', __name__)


def pvtgCounts_auth(app):
    # ------ HOST Configs are in classes/connection.py
    host = HostConfig.host
    app_paths = ConfigPaths.paths.get(host)
    if app_paths:
        for key, value in app_paths.items():
            app.config[key] = value

def pvtg_count(year, caste):
    host = HostConfig.host
    connect_param = ConnectParam(host)
    cnx, cursor = connect_param.connect()

    query = """
    SELECT COUNT(*)
    FROM application_page
    WHERE phd_registration_year = %s AND your_caste = %s
    """

    cursor.execute(query, (year, caste))
    result = cursor.fetchone()
    cnx.close()

    return result[0]

