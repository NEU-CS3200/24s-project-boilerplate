from src.blueprint_template import *
shifts = Blueprint('shifts', __name__)


# USER STORY 3.3, 3.2
# Get all shifts associated with a given user ID
@shifts.route('/shifts/user/<id>', methods = ['GET'])
def get_user_shifts(id):
    query = f'SELECT Sh.*, L.address1 FROM Shifts Sh \
        JOIN Schedules Sc ON Sh.schedule = Sc.id \
        JOIN Locations L ON Sc.location = L.id \
        WHERE Sh.employee = {id} \
        ORDER BY dayOfWeek, startTime, endTime'
    return get_helper(query)


# USER STORY 1.1, 2.1
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


# USER STORY 2.4
# Edit the shift associated with a given ID
@shifts.route('/shifts/<id>', methods = ['PUT'])
def put_shift(id):
    return put_helper('Shifts', id)


# Delete the shift associated with a given ID
@shifts.route('/shifts/<id>', methods = ['DELETE'])
def delete_shift(id):
    return delete_helper('Shifts', id)


# USER STORY 3.1
# Transfer all of an employee's shifts to another employee
@shifts.route('/transferShifts', methods = ['PUT'])
def transfer_shifts(id):
    if data is None: data = request.json
    current_app.logger.info(data)
    id1, id2 = data['fromEmployee'], data['toEmployee']
    query = f'UPDATE Shifts SET employee = {id2} WHERE employee = {id1}'
    execute(query, commit = True)
    return 'Success!'


# USER STORY 4.2
# Retrieve all tasks and display them
@shifts.route('/tasks', methods = ['GET'])
def get_tasks():
    return get_helper('SELECT * FROM Tasks')
