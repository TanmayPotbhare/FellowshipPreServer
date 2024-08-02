from datetime import datetime
from PyFiles.Admin.dashboardCounts.applicationCounts import fetch_counts
from PyFiles.Admin.dashboardCounts.applicationCounts import applCounts_blueprint
from PyFiles.Admin.dashboardCounts.genderCounts import gender_count
from PyFiles.Admin.dashboardCounts.pvtgCounts import pvtg_count
from PyFiles.Admin.dashboardCounts.disableCounts import disabilityCount_blueprint
from classes.connection import HostConfig, ConfigPaths
import os
from flask import Blueprint, render_template, session, request, redirect, url_for, flash
from authentication.middleware import auth


index_blueprint = Blueprint('index', __name__)


def index_auth(app):
    # ------ HOST Configs are in classes/connection.py
    host = HostConfig.host
    app_paths = ConfigPaths.paths.get(host)
    if app_paths:
        for key, value in app_paths.items():
            app.config[key] = value

    @index_blueprint.route('/index', methods=['GET', 'POST'])
    def index():
        if not session.get('logged_in'):
            # Redirect to the admin login page if the user is not logged in
            return redirect(url_for('adminlogin.admin_login'))

        flash('Successfully logged in!', 'success')
        selected_year = None  # Initialize selected_year

        session['user_name'] = 'Admin'
        total_count = applCounts_blueprint.applications_today()
        accepted_count = applCounts_blueprint.accepted_applications()
        form_filled = applCounts_blueprint.form_filled_applications()
        form_incomplete = applCounts_blueprint.form_incomplete_applications()
        # -------------------For Year 2021---------------------
        accepted_counts_21 = {}
        for month in range(1, 13):
            accepted_counts_21[month] = applCounts_blueprint.year_wise_applications(2021, month)

        accepted_count_jan21 = accepted_counts_21[1]
        accepted_count_feb21 = accepted_counts_21[2]
        accepted_count_march21 = accepted_counts_21[3]
        accepted_count_april21 = accepted_counts_21[4]
        accepted_count_may21 = accepted_counts_21[5]
        accepted_count_june21 = accepted_counts_21[6]
        accepted_count_july21 = accepted_counts_21[7]
        accepted_count_aug21 = accepted_counts_21[8]
        accepted_count_sep21 = accepted_counts_21[9]
        accepted_count_oct21 = accepted_counts_21[10]
        accepted_count_nov21 = accepted_counts_21[11]
        accepted_count_dec21 = accepted_counts_21[12]
        # -------------------------------------------------------

        # -------------------For Year 2022---------------------
        accepted_counts_22 = {}
        for month in range(1, 13):
            accepted_counts_22[month] = applCounts_blueprint.year_wise_applications(2022, month)
        accepted_count_jan22 = accepted_counts_22[1]
        accepted_count_feb22 = accepted_counts_22[2]
        accepted_count_march22 = accepted_counts_22[3]
        accepted_count_april22 = accepted_counts_22[4]
        accepted_count_may22 = accepted_counts_22[5]
        accepted_count_june22 = accepted_counts_22[6]
        accepted_count_july22 = accepted_counts_22[7]
        accepted_count_aug22 = accepted_counts_22[8]
        accepted_count_sep22 = accepted_counts_22[9]
        accepted_count_oct22 = accepted_counts_22[10]
        accepted_count_nov22 = accepted_counts_22[11]
        accepted_count_dec22 = accepted_counts_22[12]
        # -------------------------------------------------------

        # -------------------For Year 2023---------------------
        accepted_counts_23 = {}
        for month in range(1, 13):
            accepted_counts_23[month] = applCounts_blueprint.year_wise_applications(2023, month)
        accepted_count_jan23 = accepted_counts_23[1]
        accepted_count_feb23 = accepted_counts_23[2]
        accepted_count_march23 = accepted_counts_23[3]
        accepted_count_april23 = accepted_counts_23[4]
        accepted_count_may23 = accepted_counts_23[5]
        accepted_count_june23 = accepted_counts_23[6]
        accepted_count_july23 = accepted_counts_23[7]
        accepted_count_aug23 = accepted_counts_23[8]
        accepted_count_sep23 = accepted_counts_23[9]
        accepted_count_oct23 = accepted_counts_23[10]
        accepted_count_nov23 = accepted_counts_23[11]
        accepted_count_dec23 = accepted_counts_23[12]

        # -------------------For Year 2024---------------------
        accepted_counts_24 = {}
        for month in range(1, 13):
            accepted_counts_24[month] = applCounts_blueprint.year_wise_applications(2024, month)
        accepted_count_jan24 = accepted_counts_24[1]
        accepted_count_feb24 = accepted_counts_24[2]
        accepted_count_march24 = accepted_counts_24[3]
        accepted_count_april24 = accepted_counts_24[4]
        accepted_count_may24 = accepted_counts_24[5]
        accepted_count_june24 = accepted_counts_24[6]
        accepted_count_july24 = accepted_counts_24[7]
        accepted_count_aug24 = accepted_counts_24[8]
        accepted_count_sep24 = accepted_counts_24[9]
        accepted_count_oct24 = accepted_counts_24[10]
        accepted_count_nov24 = accepted_counts_24[11]
        accepted_count_dec24 = accepted_counts_24[12]

        # -------------------------------------------------------
        rejected_count = applCounts_blueprint.rejected_applications()

        male_count = gender_count(None, 'male')  # Count of all male users
        male_count21 = gender_count(2021, 'male')
        male_count22 = gender_count(2022, 'male')
        male_count23 = gender_count(2023, 'male')

        female_count = gender_count(None, 'female')  # Count of all female users
        female_count21 = gender_count(2021, 'female')
        female_count22 = gender_count(2022, 'female')
        female_count23 = gender_count(2023, 'female')

        trans_count = gender_count(None, 'trans')
        # -------------------------------------------------------

        katkari = pvtg_count('None', 'Katkari')
        katkari21 = pvtg_count(2021, 'Katkari')
        katkari22 = pvtg_count(2022, 'Katkari')
        katkari23 = pvtg_count(2023, 'Katkari')

        kolam = pvtg_count(2023, 'Kolam')
        kolam21 = pvtg_count(2023, 'Kolam')
        kolam22 = pvtg_count(2023, 'Kolam')
        kolam23 = pvtg_count(2023, 'Kolam')

        madia = pvtg_count(2023, 'Madia')
        madia21 = pvtg_count(2023, 'Madia')
        madia22 = pvtg_count(2023, 'Madia')
        madia23 = pvtg_count(2023, 'Madia')

        twentyone_count = applCounts_blueprint.year_twentyone_count ()
        twentytwo_count = applCounts_blueprint.year_twentytwo_count()
        twentythree_count = applCounts_blueprint.year_twentythree_count()
        accept_23 = applCounts_blueprint.accept_twentythree_count()
        reject_23 = applCounts_blueprint.reject_twentythree_count()
        olduser_count = applCounts_blueprint.old_users_count_2021()
        olduser22_count = applCounts_blueprint.old_users_count_2022()
        old_user_accepted_22 = applCounts_blueprint.old_users_count_2022_accepted()
        old_user_accepted_21 = applCounts_blueprint.old_users_count_2021_accepted()

        disability_yes = disabilityCount_blueprint.disability_yes_count_report()
        disability_no = disabilityCount_blueprint.disability_no_count_report()

        priority_people_caste = applCounts_blueprint.priority_by_caste()
        maleDataByYear, femaleDataByYear = fetch_counts()
        current_year = datetime.now().year

        return render_template('Admin/index.html', katkari=katkari, kolam=kolam, madia=madia,
                               form_incomplete=form_incomplete, form_filled=form_filled, accept_23=accept_23,
                               reject_23=reject_23, selected_year=selected_year,
                               accepted_count_jan21=accepted_count_jan21, accepted_count_feb21=accepted_count_feb21,
                               accepted_count_march21=accepted_count_march21,
                               accepted_count_april21=accepted_count_april21, accepted_count_may21=accepted_count_may21,
                               accepted_count_june21=accepted_count_june21, accepted_count_july21=accepted_count_july21,
                               accepted_count_aug21=accepted_count_aug21, accepted_count_sep21=accepted_count_sep21,
                               accepted_count_oct21=accepted_count_oct21, accepted_count_nov21=accepted_count_nov21,
                               accepted_count_dec21=accepted_count_dec21,

                               accepted_count_jan22=accepted_count_jan22, accepted_count_feb22=accepted_count_feb22,
                               accepted_count_march22=accepted_count_march22,
                               accepted_count_april22=accepted_count_april22, accepted_count_may22=accepted_count_may22,
                               accepted_count_june22=accepted_count_june22, accepted_count_july22=accepted_count_july22,
                               accepted_count_aug22=accepted_count_aug22, accepted_count_sep22=accepted_count_sep22,
                               accepted_count_oct22=accepted_count_oct22, accepted_count_nov22=accepted_count_nov22,
                               accepted_count_dec22=accepted_count_dec22,

                               accepted_count_jan23=accepted_count_jan23, accepted_count_feb23=accepted_count_feb23,
                               accepted_count_march23=accepted_count_march23,
                               accepted_count_april23=accepted_count_april23, accepted_count_may23=accepted_count_may23,
                               accepted_count_june23=accepted_count_june23, accepted_count_july23=accepted_count_july23,
                               accepted_count_aug23=accepted_count_aug23, accepted_count_sep23=accepted_count_sep23,
                               accepted_count_oct23=accepted_count_oct23, accepted_count_nov23=accepted_count_nov23,
                               accepted_count_dec23=accepted_count_dec23,

                               accepted_count_jan24=accepted_count_jan24, accepted_count_feb24=accepted_count_feb24,
                               accepted_count_march24=accepted_count_march24,
                               accepted_count_april24=accepted_count_april24, accepted_count_may24=accepted_count_may24,
                               accepted_count_june24=accepted_count_june24, accepted_count_july24=accepted_count_july24,
                               accepted_count_aug24=accepted_count_aug24, accepted_count_sep24=accepted_count_sep24,
                               accepted_count_oct24=accepted_count_oct24, accepted_count_nov24=accepted_count_nov24,
                               accepted_count_dec24=accepted_count_dec24,
                               maleDataByYear =maleDataByYear, femaleDataByYear=femaleDataByYear,
                               total_count=total_count, accepted_count=accepted_count, rejected_count=rejected_count,
                               male_count=male_count, female_count=female_count, trans_count=trans_count,
                               disability_yes=disability_yes,
                               disability_no=disability_no,
                               priority_people_caste=priority_people_caste,
                               twentyone_count=twentyone_count, twentytwo_count=twentytwo_count,
                               olduser_count=olduser_count,
                               olduser22_count=olduser22_count, twentythree_count=twentythree_count,
                               old_user_accepted_22=old_user_accepted_22,
                               old_user_accepted_21=old_user_accepted_21, male_count21=male_count21,
                               male_count22=male_count22,
                               male_count23=male_count23, female_count21=female_count21, female_count22=female_count22,
                               female_count23=female_count23, katkari21=katkari21, katkari22=katkari22,
                               katkari23=katkari23,
                               madia21=madia21, madia22=madia22, madia23=madia23, kolam21=kolam21, kolam22=kolam22,
                               kolam23=kolam23,
                               current_year=current_year)