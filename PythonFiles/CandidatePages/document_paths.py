import os
from Classes.database import HostConfig, ConfigPaths, ConnectParam
from flask import Blueprint, render_template, session, request, redirect, url_for, flash, make_response


section1_blueprint = Blueprint('section1', __name__)


def section1_auth(app):
    # ------ HOST Configs are in classes/connection.py
    host = HostConfig.host
    app_paths = ConfigPaths.paths.get(host)
    if app_paths:
        for key, value in app_paths.items():
            app.config[key] = value

def save_applicant_photo(file, firstname, lastname):
    if file:
        filename = f"{firstname}_{lastname}_{file.filename}"
        file.save(os.path.join(app.config['UPLOAD_PHOTO_SECTION1'], filename))
        # return os.path.join(app.config['UPLOAD_PHOTO_SECTION1'], filename)
        return '/static/uploads/image_retrive/' + filename
    else:
        return "Save File"