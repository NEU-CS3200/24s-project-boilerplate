from blueprint_template import *
torequests = Blueprint('requests', __name__)


# Gets all time-off requests and additional information about them
@torequests.route('/requests', methods = ['GET'])
def get_requests():
    query = 'SELECT *, COUNT(R.id) AS numTimes, SUM(hours) AS hoursOff \
        FROM TimeOffRequests R JOIN (SELECT *, \
        TIMEDIFF(endTime, startDate) / 3600 AS hours \
        FROM Times) T ON R.id = T.request GROUP BY R.id'
    return get_helper(query)


# Adds a new time-off requests
@torequests.route('/requests', methods = ['POST'])
def post_request():
    return post_helper('Requests')


# Edit the time-off request associated with a given ID
@torequests.route('/requests/<id>', methods = ['PUT'])
def put_request(id):
    return put_helper('TimeOffRequests', id)


# Deletes a time-off request (and all associated times)
@torequests.route('/requests/<id>', methods = ['DELETE'])
def delete_request(id):
    delete_helper('Times', id, 'request')
    return delete_helper('TimeOffRequests', id)
