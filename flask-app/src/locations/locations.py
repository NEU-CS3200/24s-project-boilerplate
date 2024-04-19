from src.blueprint_template import *
locations = Blueprint('locations', __name__)


# Get all locations and their owners
@locations.route('/locations', methods = ['GET'])
def get_locations():
    query = 'SELECT L.*, U.firstName, U.lastName \
        FROM Locations L JOIN Users U ON L.owner = U.id'
    return get_helper(query)


# Add a new location (and associated schedule)
@locations.route('/locations', methods = ['POST'])
def post_location():
    data = post_helper('Locations', True)
    id = '(SELECT MAX(id) FROM Locations)'
    if data.get('id'): id = f'VALUES ({data["id"]})'
    execute(f'INSERT INTO Schedules (location) {id}')
    return 'Success!'
    

# Edit the location associated with a given ID
@locations.route('/locations/<id>', methods = ['PUT'])
def put_location(id):
    return put_helper('Locations', id)


# Delete a location and all associated shifts
@locations.route('/locations/<id>', methods = ['DELETE'])
def delete_location(id):
    query = 'DELETE FROM Shifts WHERE id IN \
        (SELECT Sh.id FROM Shifts Sh \
        JOIN Schedules Sc ON Sh.schedule = Sc.id)'
    execute(query, commit = True)
    delete_helper('Schedules', id, 'location')
    return delete_helper('Locations', id)


# USER STORY 2.3. Gets the number of hours scheduled at each location
@locations.route('/locations/hours', methods = ['GET'])
def get_location_hours():
    query = """SELECT L.id, L.address1, L.address2, L.city, L.state,
        SUM(TIMESTAMPDIFF(SECOND, startTime, endTime)) / 3600 AS hoursScheduled,
        COUNT(Sh.id) AS numShifts
    FROM Shifts Sh
    JOIN Schedules Sc ON Sh.schedule = Sc.id
    JOIN Locations L ON Sc.location = L.id
    GROUP BY L.id ORDER BY hoursScheduled DESC"""
    return get_helper(query)


# USER STORY 2.1. Gets all locations associated with a given owner ID
@locations.route('/owners/<id>', methods = ['GET'])
def get_owner_locations(id):
    query = f'SELECT * FROM Locations WHERE owner = {id}'
    return get_helper(query)
