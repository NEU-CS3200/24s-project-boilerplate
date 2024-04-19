from src.blueprint_template import *
users = Blueprint('users', __name__)


# NOTE: User story 4.4 about having a simple interface incorporates every single route in the REST API.
# # For simplicity, I will not be writing it under every single route.


# Gets all active users
@users.route('/users', methods = ['GET'])
def get_users():
    query = 'SELECT * FROM Users'
    return get_helper(query)


# Add a new user
@users.route('/users', methods = ['POST'])
def post_user():
    return post_helper('Users')


# USER STORY 1.2. Gets all users that are managers of other users
@users.route('/managers', methods = ['GET'])
def get_managers():
    query = 'SELECT M.*, COUNT(M.id) AS numEmployees \
        FROM UserManagers UM JOIN Users M \
        ON UM.manager = M.id GROUP BY M.id'
    return get_helper(query)


# Edits the user associated with a given ID
@users.route('/users/<id>', methods = ['PUT'])
def put_user(id):
    return put_helper('Users', id)


# USER STORY 2.4. Moving an employee's shifts to a new location
@users.route('/moveLocation', methods = ['PUT'])
def move_locations():
    data = request.json
    current_app.logger.info(data)
    userId, locationId = data['userId'], data['locationId']
    query = f'UPDATE Shifts \
        SET schedule = ( \
            SELECT MAX(Sc.id) \
            FROM Schedules Sc \
            WHERE location = {locationId}) \
        WHERE employee = {userId}'
    execute(query, commit = True)
    return 'Success!'


# Get the salaries of all employees during a given time interval
@users.route('/salaries', methods = ['GET'])
def get_salaries():
    data = request.json
    current_app.logger.info(data)
    startDate, endDate = data['startDate'], data['endDate']
    query = f"""WITH RECURSIVE Dates AS (
        SELECT '{startDate}' AS date UNION ALL
        SELECT ADDDATE(date, INTERVAL 1 DAY) FROM Dates
        WHERE Dates.date < '{endDate}'),
    UserTimes AS (
        SELECT R.createdBy, T.*
        FROM TimeOffRequests R JOIN Times T ON R.id = T.request
        WHERE R.approved AND NOT R.paid),
    TimeOverlaps AS (
        SELECT T1.id AS id1, T2.id AS id2
        FROM UserTimes T1 JOIN UserTimes T2
        ON T1.createdBy = T2.createdBy WHERE T1.id <= T2.id
        AND (T1.startDate BETWEEN T2.startDate AND T2.endDate
        OR T2.startDate BETWEEN T1.startDate AND T1.endDate)),
    TimeChains AS (
        SELECT * FROM TimeOverlaps UNION ALL
        SELECT T1.id1, T2.id2 FROM TimeOverlaps T1
        JOIN TimeChains T2 ON T1.id2 = T2.id1
        WHERE T1.id1 <> T2.id2),
    UniqueTimeChains AS (
        SELECT DISTINCT * FROM TimeChains WHERE id1 NOT IN
        (SELECT id2 FROM TimeChains WHERE id1 <> id2)),
    UniqueTimes AS (
        SELECT C.id1 AS id, T.createdBy,
            MIN(T.startDate) AS startDate, MAX(T.endDate) AS endDate
        FROM UniqueTimeChains C JOIN UserTimes T ON T.id = C.id2
        GROUP BY C.id1, T.createdBy),
    ShiftInstances AS (
        SELECT Sh.*, TIMESTAMP(D.date, Sh.startTime) AS startDate,
            TIMESTAMP(D.date, Sh.endTime) AS endDate
        FROM Shifts Sh JOIN (SELECT * FROM Dates) D
        ON WEEKDAY(D.date) = Sh.dayOfWeek),
    ShiftBreaks AS (
        SELECT Sh.*, LEAST(Sh.endDate, T.endDate) AS endBreak,
            GREATEST(Sh.startDate, T.startDate) AS startBreak
        FROM ShiftInstances Sh
        LEFT JOIN UniqueTimes T ON Sh.employee = T.createdBy
        WHERE T.id IS NULL
        OR T.startDate BETWEEN Sh.startDate AND Sh.endDate
        OR T.endDate BETWEEN Sh.startDate AND Sh.endDate),
    ShiftHours AS (
        SELECT id, employee, (1 + 0.5 * overtime) AS rateScalar,
            TIMESTAMPDIFF(SECOND, startDate, endDate) / 3600 AS hoursScheduled,
            SUM(TIMESTAMPDIFF(SECOND, startBreak, endBreak)) / 3600 AS hoursOff
        FROM ShiftBreaks GROUP BY id, startDate, endDate),
    ShiftInfo AS (
        SELECT Sh.*, U.firstName, U.lastName,
            hourlyRate * rateScalar AS hourlyRate,
            hoursScheduled - hoursOff AS hoursWorked
        FROM ShiftHours Sh JOIN Users U ON Sh.employee = U.id)
    SELECT U.id, U.firstName, U.lastName, COUNT(Sh.id) AS numShifts,
        SUM(Sh.hourlyRate * Sh.hoursWorked) AS totalPay
    FROM ShiftInfo Sh JOIN Users U on Sh.employee = U.id
    GROUP BY U.id"""
    return get_helper(query)


# Deletes the user associated with a given ID
@users.route('/users/<id>', methods = ['DELETE'])
def delete_user(id):
    return delete_helper('Users', id)


# Adds a new user-manager pair
@users.route('/userManagers', methods = ['POST'])
def post_user_manager():
    return post_helper('UserManagers')


# USER STORY 4.3. Transfer management of an employee
@users.route('/userManagers', methods = ['PUT'])
def put_user_manager():
    data = request.json
    current_app.logger.info(data)
    userId, managerId = data['userId'], data['managerId']
    query = f'UPDATE UserManagers \
        SET manager = {managerId} WHERE user = {userId}'
    execute(query, commit = True)
    return 'Success!'


# Removes a manager as manager of all of their employees
@users.route('/userManagers/<id>', methods = ['DELETE'])
def delete_user_manager(id):
    data = request.json
    current_app.logger.info(data)
    managerId = data['managerId']
    query = f'DELETE FROM UserManagers \
        WHERE manager = {managerId}'
    execute(query, commit = True)
    return delete_helper('UserManagers', id)


# USER STORY 4.1. Gets the number of hours each employee has been scheduled for
@users.route('/userHours', methods = ['GET'])
def get_user_hours():
    query = 'SELECT U.id, U.firstName, U.lastName, U.role, U.hourlyRate, COUNT(Sh.id) AS numShifts, \
            SUM(TIMESTAMPDIFF(SECOND, Sh.startTime, Sh.endTime)) / 3600 AS hoursScheduled \
        FROM Shifts Sh JOIN Users U ON Sh.employee = U.id \
        GROUP BY U.id ORDER BY hoursScheduled DESC'
    return get_helper(query)
