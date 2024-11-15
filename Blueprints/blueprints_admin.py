from PythonFiles.AdminPages.adminlogin import adminlogin_blueprint, adminlogin_auth
from PythonFiles.AdminPages.AdminLevels.admin_level_one import adminlevelone_blueprint, adminlevelone_auth
from PythonFiles.AdminPages.AdminLevels.admin_level_two import adminleveltwo_blueprint, adminleveltwo_auth
from PythonFiles.AdminPages.AdminLevels.admin_level_three import adminlevelthree_blueprint, adminlevelthree_auth


# Function to register admin blueprints
def admin_blueprints(app, mail):
    # Admin Login
    adminlogin_auth(app)
    app.register_blueprint(adminlogin_blueprint)

    # Admin Level One
    adminlevelone_auth(app, mail)
    app.register_blueprint(adminlevelone_blueprint)

    # Admin Level One
    adminleveltwo_auth(app, mail)
    app.register_blueprint(adminleveltwo_blueprint)

    # Admin Level Three
    adminlevelthree_auth(app, mail)
    app.register_blueprint(adminlevelthree_blueprint)