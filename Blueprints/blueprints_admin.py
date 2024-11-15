from PythonFiles.AdminPages.adminlogin import adminlogin_blueprint, adminlogin_auth


# Function to register admin blueprints
def admin_blueprints(app, mail):
    # Admin Login
    adminlogin_auth(app)
    app.register_blueprint(adminlogin_blueprint)