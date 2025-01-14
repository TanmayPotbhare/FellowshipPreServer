from Classes.database import HostConfig, ConfigPaths, ConnectParam
from flask import Blueprint, render_template, session, request, redirect, url_for, flash, make_response, jsonify
import os
from functools import wraps

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

    def login_required(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Check if the user is logged in (session contains 'user')
            if 'user' not in session:
                flash('You need to log in to access this page.', 'danger')
                return redirect(url_for('login'))
            return f(*args, **kwargs)

        return decorated_function

