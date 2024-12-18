from PythonFiles.CandidatePages.candidate_dashboard import candidate_dashboard_blueprint, candidate_dashboard_auth
from PythonFiles.CandidatePages.manage_profile import manage_profile_blueprint, manage_profile_auth
from PythonFiles.CandidatePages.ApplicationForm.section1 import section1_blueprint, section1_auth
from PythonFiles.CandidatePages.joining_report import joining_report_blueprint, joining_report_auth
from PythonFiles.CandidatePages.undertaking_report import undertaking_report_blueprint, undertaking_report_auth
from PythonFiles.CandidatePages.assessment_report import assessment_report_blueprint, assessment_report_auth
from PythonFiles.CandidatePages.withdraw_fellowship import withdraw_fellowship_blueprint, withdraw_fellowship_auth
from PythonFiles.CandidatePages.change_guide import change_guide_blueprint, change_guide_auth
from PythonFiles.CandidatePages.change_center import change_center_blueprint, change_center_auth
from PythonFiles.CandidatePages.upload_phd import upload_phd_blueprint, upload_phd_auth
from PythonFiles.CandidatePages.upload_thesis import upload_thesis_blueprint, upload_thesis_auth


# Function to register homepage blueprints
def candidate_blueprints(app, mail):
    # Candidate Dashboard Page
    candidate_dashboard_auth(app)
    app.register_blueprint(candidate_dashboard_blueprint)

    # Candidate Dashboard Page
    manage_profile_auth(app)
    app.register_blueprint(manage_profile_blueprint)

    # Section1 Application form
    section1_auth(app)
    app.register_blueprint(section1_blueprint)

    # Candidate Joining Report
    joining_report_auth(app)
    app.register_blueprint(joining_report_blueprint)

    # Candidate Undertaking Report
    undertaking_report_auth(app)
    app.register_blueprint(undertaking_report_blueprint)

    # Candidate Assessment Report
    assessment_report_auth(app)
    app.register_blueprint(assessment_report_blueprint)

    # Candidate Withdraw Fellowship
    withdraw_fellowship_auth(app)
    app.register_blueprint(withdraw_fellowship_blueprint)

    # Candidate Change Guide Fellowship
    change_guide_auth(app)
    app.register_blueprint(change_guide_blueprint)

    # Candidate Change Center Fellowship
    change_center_auth(app)
    app.register_blueprint(change_center_blueprint)

    # Candidate Upload Ph.D. Fellowship
    upload_phd_auth(app)
    app.register_blueprint(upload_phd_blueprint)

    # Candidate Upload Thesis Fellowship
    upload_thesis_auth(app)
    app.register_blueprint(upload_thesis_blueprint)



