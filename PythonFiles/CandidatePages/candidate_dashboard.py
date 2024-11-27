from Classes.database import HostConfig, ConfigPaths, ConnectParam
from flask import Blueprint, render_template, session, request, redirect, url_for, flash, make_response
from Authentication.middleware import auth

candidate_dashboard_blueprint = Blueprint('candidate_dashboard', __name__)


def candidate_dashboard_auth(app):
    # ------ HOST Configs are in classes/connection.py
    host = HostConfig.host
    app_paths = ConfigPaths.paths.get(host)
    if app_paths:
        for key, value in app_paths.items():
            app.config[key] = value

    @candidate_dashboard_blueprint.route('/candidate_dashboard')
    def candidate_dashboard():
        return render_template('CandidatePages/candidate_dashboard.html', title="My Profile")

    @candidate_dashboard_blueprint.route('/installment_details')
    def installment_details():
        return render_template('CandidatePages/installment_details.html', title="Installment Details")

    @candidate_dashboard_blueprint.route('/logout')
    def logout():
        return redirect(url_for('login_signup.login'))
