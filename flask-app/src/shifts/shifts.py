from blueprint_template import *
shifts = Blueprint('shifts', __name__)


# Get all shifts associated with a given user ID
@shifts.route('/shifts/user/<id>', methods = ['GET'])
def get_user_shifts(id):
    query = f'SELECT Sh.*, L.address1 FROM Shifts Sh \
        JOIN Schedules Sc ON Sh.schedule = Sc.id \
        JOIN Locations L ON Sc.location = L.id \
        WHERE Sh.employee = {id}'
    return get_helper(query)


# Get all shifts associated with a given location ID
@shifts.route('/shifts/location/<id>', methods = ['GET'])
def get_location_shifts(id):
    query = f'SELECT Sh.*, U.firstName, U.lastName FROM Shifts Sh \
        JOIN Schedules Sc ON Sh.schedule = Sc.id \
        JOIN Users U ON Sh.employee = U.id \
        WHERE Sc.location = {id}'
    return get_helper(query)


# Add a new shift
@shifts.route('/shifts', methods = ['POST'])
def post_shift():
    return post_helper('Shifts')


# Edit the shift associated with a given ID
@shifts.route('/shifts/<id>', methods = ['PUT'])
def put_shift(id):
    return put_helper('Shifts', id)


# Delete the shift associated with a given ID
@shifts.route('/shifts/<id>', methods = ['DELETE'])
def delete_shift(id):
    return delete_helper('Shifts', id)
