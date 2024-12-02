# blueprints_homepage.py

from PythonFiles.CandidatePages.candidate_dashboard import candidate_dashboard_blueprint, candidate_dashboard_auth
from PythonFiles.CandidatePages.ApplicationForm.section1 import section1_blueprint, section1_auth

# Function to register homepage blueprints
def candidate_blueprints(app, mail):
    # Homepage
    candidate_dashboard_auth(app)
    app.register_blueprint(candidate_dashboard_blueprint)

    # Section1 Application form
    section1_auth(app)
    app.register_blueprint(section1_blueprint)
