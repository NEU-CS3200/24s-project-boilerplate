from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db


def execute(query, commit = False):
    current_app.logger.info(query)
    cursor = db.get_db().cursor()
    cursor.execute(query)
    if commit: db.get_db().commit()
    return cursor


def get_helper(query):
    cursor = execute(query)
    cols = [x[0] for x in cursor.description]
    data = [dict(zip(cols, row)) for row in cursor.fetchall()]
    return jsonify(data)


def post_helper(table, return_data = False):
    def to_str(val):
        s = isinstance(val, str)
        return ('\'{}\'','{}')[s].format(val)
    data = request.json
    current_app.logger.info(data)
    cols = ', '.join(data.keys())
    vals = ', '.join([to_str(v) for v in data.values()])
    query = f'INSERT INTO {table} ({cols}) VALUES ({vals})'
    execute(query, commit = True)
    return data if return_data else 'Success!'


def put_helper(table, val, key = 'id', data = None, return_data = False):
    if data is None: data = request.json
    current_app.logger.info(data)
    pairs = ', '.join([f'{k} = {v}' for k, v in data.items() if k != key])
    query = f'UPDATE {table} SET {pairs} WHERE {key} = {val}'
    execute(query, commit = True)
    return data if return_data else 'Success!'


def delete_helper(table, val, key = 'id'):
    query = f'DELETE FROM {table} WHERE {key} = {val}'
    execute(query, commit = True)
    return 'Success!'


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
