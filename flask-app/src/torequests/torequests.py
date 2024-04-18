from src.blueprint_template import *
torequests = Blueprint('requests', __name__)


# USER STORY 1.3. Gets all unviewed time-off requests and additional information about them
@torequests.route('/unviewedRequests', methods = ['GET'])
def get_unapproved_requests():
    query = 'SELECT R.*, COUNT(R.id) AS numTimes, SUM(hours) AS hoursOff \
        FROM TimeOffRequests R JOIN (SELECT *, \
        TIMESTAMPDIFF(SECOND, startDate, endDate) / 3600 AS hours \
        FROM Times) T ON R.id = T.request \
        WHERE R.approved IS NULL GROUP BY R.id'
    return get_helper(query)


# USER STORY 2.2. Gets all unviewed time-off requests for a given location
@torequests.route('/unviewedRequests/<id>', methods = ['GET'])
def get_unapproved_requests(id):
    query = f"""SELECT R.id, U.firstName, U.lastName, R.reason, R.paid,
            R.submitDate, COUNT(R.id) AS numTimes, SUM(hours) AS hoursOff,
            MIN(startDate) AS startDate, MAX(endDate) AS endDate
        FROM TimeOffRequests R JOIN (SELECT *,
        TIMESTAMPDIFF(SECOND, startDate, endDate) / 3600 AS hours
        FROM Times) T ON R.id = T.request
        JOIN Users U ON R.createdBy = U.id
        JOIN Schedules Sc ON R.schedule = Sc.id
        WHERE R.approved IS True AND Sc.location = {id} GROUP BY R.id"""
    return get_helper(query)


# Gets all time-off requests associated with a given user ID
@torequests.route('/requests/<createdBy>', methods = ['GET'])
def get_user_requests(createdBy):
    query = f'SELECT *, COUNT(R.id) AS numTimes, SUM(hours) AS hoursOff \
        FROM TimeOffRequests R JOIN (SELECT *, \
        TIMESTAMPDIFF(SECOND, startDate, endDate) / 3600 AS hours \
        FROM Times) T ON R.id = T.request \
        WHERE R.createdBy = {createdBy} GROUP BY R.id'
    return get_helper(query)


# USER STORY 3.2. Adds a new time-off request
@torequests.route('/requests', methods = ['POST'])
def post_request():
    return post_helper('TimeOffRequests')


# USER STORY 1.3. Edit the time-off request associated with a given ID
@torequests.route('/requests/<id>', methods = ['PUT'])
def put_request(id):
    return put_helper('TimeOffRequests', id)


# USER STORY 3.2. Adds a new time interval
@torequests.route('/times', methods = ['POST'])
def post_time():
    return post_helper('Times')


# Edit the time interval associated with a given ID
@torequests.route('/times/id>', methods = ['PUT'])
def put_time(id):
    return put_helper('Times', id)


# Deletes a time interval
@torequests.route('/times/<id>', methods = ['DELETE'])
def delete_time(id):
    return delete_helper('Times', id)
