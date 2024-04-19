# Some set up for the application 

from flask import Flask
from flaskext.mysql import MySQL

# Create a MySQL object that we will use in other parts of the API
db = MySQL()

def create_app():
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = 'someCrazyS3cR3T!Key.!'
    app.config['MYSQL_DATABASE_USER'] = 'root'
    app.config['MYSQL_DATABASE_PASSWORD'] = open('/secrets/db_root_password.txt').readline().strip()
    app.config['MYSQL_DATABASE_HOST'] = 'db'
    app.config['MYSQL_DATABASE_PORT'] = 3306
    app.config['MYSQL_DATABASE_DB'] = 'Scheduling'
    
    db.init_app(app)
    
    @app.route('/')
    def welcome():
        return "<h1>Welcome to the Shift Scheduling App</h1>"

    # Import the various Blueprint Objects
    from src.locations.locations import locations
    from src.shifts.shifts import shifts
    from src.torequests.torequests import torequests
    from src.users.users import users

    # Register the routes from each Blueprint with the app object
    app.register_blueprint(locations, url_prefix = '/l')
    app.register_blueprint(shifts, url_prefix = '/s')
    app.register_blueprint(torequests, url_prefix = '/r')
    app.register_blueprint(users, url_prefix = '/u')

    # Don't forget to return the app object
    return app