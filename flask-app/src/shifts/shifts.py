from src.blueprint_template import *
shifts = Blueprint('shifts', __name__)


# Helper function for GET requests
# Turns startTime and endTime into JSON-compatible types
def shifts_get_helper(query):
    cursor = execute(query)
    cols = [x[0] for x in cursor.description]
    data = [dict(zip(cols, row)) for row in cursor.fetchall()]
    for i in range(len(data)):
        # Extract total seconds and convert to hours
        start_seconds = data[i]['startTime'].total_seconds()
        end_seconds = data[i]['endTime'].total_seconds()
        data[i]['startTime'] = start_seconds / 3600
        data[i]['endTime'] = end_seconds / 3600
    return jsonify(data)
    

# USER STORY 3.3. Get all shifts associated with a given user ID
# Also used for user story 3.4, proving clarity on pay, hours, and role
@shifts.route('/shifts/user/<id>', methods = ['GET'])
def get_user_shifts(id):
    query = f"""WITH ShiftHours AS (
        SELECT *, (1 + 0.5 * overtime) AS rateScalar,
            TIMESTAMPDIFF(SECOND, startTime, endTime) / 3600 AS hours
        FROM Shifts)
    SELECT Sh.dayOfWeek, Sh.startTime, Sh.endTime,
        Sh.duty, L.address1, Sh.hours,
        Sh.rateScalar * Sh.hours * U.hourlyRate AS pay
    FROM ShiftHours Sh
    JOIN Schedules Sc ON Sh.schedule = Sc.id
    JOIN Locations L ON Sc.location = L.id
    JOIN Users U ON Sh.employee = U.id
    WHERE Sh.employee = {id}
    ORDER BY dayOfWeek, startTime, endTime"""
    return shifts_get_helper(query)


# USER STORY 2.1. Get all shifts associated with a given location ID
@shifts.route('/shifts/location/<id>', methods = ['GET'])
def get_location_shifts(id):
    query = f'SELECT Sh.*, U.firstName, U.lastName FROM Shifts Sh \
        JOIN Schedules Sc ON Sh.schedule = Sc.id \
        JOIN Users U ON Sh.employee = U.id \
        WHERE Sc.location = {id}'
    return shifts_get_helper(query)


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


# USER STORY 3.1. Transfer an employees shifts to another employee
@shifts.route('/transferShifts/<fromId>/<toId>', methods = ['PUT'])
def transfer_shifts(fromId, toId):
    query = f'UPDATE Shifts SET employee = {fromId} WHERE employee = {toId}'
    execute(query, commit = True)
    return 'Success!'


# USER STORY 4.2. Retrieve all tasks and associated information
@shifts.route('/tasks', methods = ['GET'])
def get_tasks():
    query = 'SELECT T.*, U.firstName, U.lastName \
        FROM Tasks T JOIN Users U ON T.user = U.id'
    return get_helper(query)


# USER STORY 1.4. Adds a new task
@shifts.route('/tasks', methods = ['POST'])
def post_task():
    return post_helper('Tasks')


# Edit the task associated with the given ID
@shifts.route('/tasks/<id>', methods = ['PUT'])
def put_task(id):
    return put_helper('Tasks', id)


# Deletes the task associated with the given ID
@shifts.route('/tasks/<id>', methods = ['DELETE'])
def delete_task(id):
    return delete_helper('Tasks', id)
