# blueprints_homepage.py

from PythonFiles.CandidatePages.candidate_dashboard import candidate_dashboard_blueprint, candidate_dashboard_auth


# Function to register homepage blueprints
def candidate_blueprints(app, mail):
    # Homepage
    candidate_dashboard_auth(app)
    app.register_blueprint(candidate_dashboard_blueprint)
