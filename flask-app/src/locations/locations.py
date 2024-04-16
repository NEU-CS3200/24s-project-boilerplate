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
def delete_shift(id):
    query = 'DELETE FROM Shifts WHERE id IN \
        (SELECT Sh.id FROM Shifts Sh \
        JOIN Schedules Sc ON Sh.schedule = Sc.id)'
    execute(query, commit = True)
    delete_helper('Schedules', id, 'location')
    return delete_helper('Locations', id)
