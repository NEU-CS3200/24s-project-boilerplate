from src.blueprint_template import *
torequests = Blueprint('requests', __name__)


# USER STORY 1.3
# Gets all unviewed time-off requests and additional information about them
@torequests.route('/requests', methods = ['GET'])
def get_unapproved_requests():
    query = 'SELECT *, COUNT(R.id) AS numTimes, SUM(hours) AS hoursOff \
        FROM TimeOffRequests R JOIN (SELECT *, \
        TIMEDIFF(endDate, startDate) / 3600 AS hours \
        FROM Times) T ON R.id = T.request \
        WHERE R.approved is NULL GROUP BY R.id'
    return get_helper(query)


# Gets all time-off requests associated with a given user ID
@torequests.route('/requests/<createdBy>', methods = ['GET'])
def get_user_requests(createdBy):
    query = f'SELECT *, COUNT(R.id) AS numTimes, SUM(hours) AS hoursOff \
        FROM TimeOffRequests R JOIN (SELECT *, \
        TIMEDIFF(endDate, startDate) / 3600 AS hours \
        FROM Times) T ON R.id = T.request \
        WHERE R.createdBy = {createdBy} GROUP BY R.id'
    return get_helper(query)


# USER STORY 3.1
# Adds a new time-off requests
@torequests.route('/requests', methods = ['POST'])
def post_request():
    return post_helper('TimeOffRequests')


# USER STORY 1.3
# Edit the time-off request associated with a given ID
@torequests.route('/requests/<id>', methods = ['PUT'])
def put_request(id):
    return put_helper('TimeOffRequests', id)


# Adds a new time interval
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
