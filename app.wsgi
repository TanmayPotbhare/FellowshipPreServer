import sys
import logging

# Activate the virtual environment (if you are using one)
# activate_this = '/path/to/your/virtualenv/bin/activate_this.py'
# with open(activate_this) as file_:
# exec(file_.read(), dict(__file__=activate_this))

# Adjust the path to your application
# sys.path.insert(0, '/var/www/fellowship/fellowship/FellowshipPreServer')
sys.path.insert(0, '/var/www/fellowship/fellowship/cdac/wrapper.jar')


from app import app as application
# Import your Flask app instance

# Configure logging if needed
# For example, you can set up a log file:
# logging.basicConfig(filename='/path/to/your/log/file.log', level=logging.INFO)

# Optionally, configure additional settings here if needed

if __name__ == "__main__":
    application.run()





define PROJECT_PATH /var/www/fellowship/fellowship/cdac

<VirtualHost *:8080>
    ServerName localhost
    # Tell Apache and Passenger where your app's code directory is
    #DocumentRoot /var/www/icswebapp/icswebapp
    #PassengerAppRoot /var/www/icswebapp/icswebapp

    # Tell Passenger that your app is a Python app
    #PassengerAppType wsgi
    #PassengerStartupFile passenger_wsgi.py

    # wsgi settings
    WSGIDaemonProcess FellowshipPreServer python-path=/var/www/fellowship/fellowship/FellowshipPreServer/myenv/lib/python3.10/site-packages:${PROJECT_PATH}
    WSGIProcessGroup FellowshipPreServer
    WSGIScriptAlias / /var/www/fellowship/fellowship/cdac/api_cdac.py

    # map server side static directory to {ip or domain_name}/static
    #Alias /static  ${PROJECT_PATH}/static

    # allow all requests to access this project file
    <Directory ${PROJECT_PATH}/>
        Allow from all
        AllowOverride All
        Require all granted
        Options -MultiViews
    </Directory>

    # set log saved path
    ErrorLog ${PROJECT_PATH}/log/error_python.log
    CustomLog ${PROJECT_PATH}/log/access.log combined
        # Commented following lines
    # Relax Apache security settings
    #<Directory /var/www/icswebapp/icswebapp>
    #  Allow from all
    #  Options -MultiViews
    #  # Uncomment this if you're on Apache ≥ 2.4:
    #  #Require all granted
    #</Directory>
</VirtualHost>












