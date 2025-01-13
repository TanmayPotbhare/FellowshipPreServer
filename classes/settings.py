from Classes.database import HostConfig, ConfigPaths, ConnectParam
from flask import Blueprint, render_template, session, request, redirect, url_for, flash, make_response, jsonify
import os

settings_blueprint = Blueprint('settings', __name__)


def settings_auth(app):
    # ------ HOST Configs are in classes/connection.py
    host = HostConfig.host
    app_paths = ConfigPaths.paths.get(host)

    if app_paths:
        for key, value in app_paths.items():
            app.config[key] = value
    else:
        flash("Error: Could not load configuration for the host.")
        return redirect(url_for('error_page'))  # Or whatever error handling you prefer

    # Using environment variable for sensitive data
    ZEPTOMAIL_URL = "https://api.zeptomail.in/v1.1/email"
    ZEPTOMAIL_API_KEY = os.getenv("Zoho-enczapikey PHtE6r0PFOjriWB+oRJR5f+wR5L2No0n9O1nfwZG4tkWDKJXGk1d/tosxjO+rhZ/BvlGQPPKmd5gsOvJuuqDJm68NGgdXWqyqK3sx/VYSPOZsbq6x00asF4YdkTVVoPpdtNi0iDfuNuX", "default_api_key_if_not_set")

    if ZEPTOMAIL_API_KEY == "default_api_key_if_not_set":
        flash("Warning: ZeptoMail API Key not set, using default key.")

    app.config['ZEPTOMAIL_API_KEY'] = ZEPTOMAIL_API_KEY
    app.config['ZEPTOMAIL_URL'] = ZEPTOMAIL_URL

