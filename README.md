**Flask Application with Class-Based and Blueprint Structure**

This project demonstrates a scalable structure for Fellowship Flask application using class-based views and blueprints. 
It is designed for ease of maintenance, modularity, and extensibility.

**Table of Contents**

    Project Overview
    Folder Structure
    Setup and Installation
    How It Works
    Adding New Features
    Known Issues
    Contributing


**PROJECT OVERVIEW**

This project organizes a Flask web application into a modular structure by utilizing:

    Class-Based Views for better encapsulation and reusability.
    Blueprints for grouping related routes and logic.
    Scalability Features to easily add new modules or extend existing ones.


**SETUP AND INSTALLATION**

Clone the repository:

    git clone <repository_url>
    cd <repository_directory>

Create and activate a virtual environment:

    python -m venv venv
    source venv/bin/activate  # For Linux/Mac
    venv\Scripts\activate     # For Windows

Install dependencies:

    pip install -r requirements.txt

Run the application:

    python app.py

**FOLDER STRUCTURE**

    project_root/
    ├── Authentication/         # Middleware for security
    │   ├── auth_middleware.py  # Security middleware logic
    │   └── ...
    ├── Blueprints/             # All blueprints and their respective routes
    │   ├── admin_blueprint.py  # Admin routes
    │   ├── candidate_blueprint.py  # Candidate routes
    │   └── ...
    ├── Classes/                # Predefined classes for direct use
    │   ├── Caste.py       # User-related class
    │   ├── database.py      # Admin-related class
    │   └── ...
    ├── Python_Files/           # Categorized Python files for modules you're working on
    │   ├── admin.py            # Admin module logic
    │   ├── candidate.py        # Candidate module logic
    │   └── homepage.py         # Homepage module logic
    ├── Static/                 # Static assets (CSS, JS, images, etc.)
    │   ├── css/                # CSS files
    │   ├── js/                 # JavaScript files
    │   └── images/             # Image files
    ├── Templates/              # HTML files for rendering views
    │   ├── index.html          # Homepage template
    │   ├── admin_dashboard.html  # Admin dashboard template
    │   └── ...
    ├── app.py                  # Main Flask application file (initializes app)
    └── README.md               # Project documentation (this file)

-----------------------------------------------------

    Authentication - Middleware for security 
    Blueprints - Consists all the blueprints and paths of respective .py files.
    Classes - Predefined classes which can be directly used in the code. 
    Python Files - All the .py files categroized into the module you are working (Admin, Candidate, Homepage)
    Static - CSS, JS, etc
    Templates - All HTML Files 
    app.py - The main Flask file where flask application is initialized. 


**HOW IT WORKS**

    App Initialization: The application is initialized in the app.py file, where configurations and blueprints are registered.
    Class-Based Views: Found in the Classes directory, these classes define the logic for handling requests.
    Blueprints: Found in the Blueprints directory. Each module is a blueprint that groups related views and routes for better modularity.
    Database Models: Directly called using mysql connector.


**Example for Better Understanding**

    Consider, you want to add a module in Homepage.
    Go inside the Blueprints Directory, find the blueprint which is for homepage. 
    Inside the homepage blueprint, register the blueprint for the new module.py file. 
    In the module.py file add all the classes, and define the blueprint. 
    Using that blueprint just give the route and render the html. 