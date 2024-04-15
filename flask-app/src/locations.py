from blueprint_template import *
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
    id = data.get("id") or get_max_value('Locations')
    execute(f'INSERT INTO Schedules (location) VALUES ({id})')
    return 'Success!'
    

# Edit the location associated with a given ID
@locations.route('/locations/<id>', methods = ['PUT'])
def put_location(id):
    return put_helper('Locations', id)


# Delete a location and all associated shifts
@locations.route('/locations/<id>', methods = ['DELETE'])
def delete_shift(id):
    query = 'DELETE FROM Shifts WHERE id IN \
        (SELECT Sh.id FROM Shifts Sh \
        JOIN Schedules Sc ON Sh.schedule = Sc.id)'
    execute(query, commit = True)
    delete_helper('Schedules', id, 'location')
    return delete_helper('Locations', id)