from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db


def execute(query, commit = False):
    current_app.logger.info(query)
    cursor = db.get_db().cursor()
    cursor.execute(query)
    if commit: db.get_db().commit()
    return cursor


from datetime import timedelta

def convert_time_to_number(data):
    for row in data:
        # Extract total seconds and convert to hours
        start_seconds = row['startTime'].total_seconds()
        end_seconds = row['endTime'].total_seconds()
        
        # Convert to hours
        row['startTime'] = start_seconds / 3600
        row['endTime'] = end_seconds / 3600
        
    return data


def get_helper(query):
    cursor = execute(query)
    cols = [x[0] for x in cursor.description]
    data = [dict(zip(cols, row)) for row in cursor.fetchall()]
    data = convert_time_to_number(data)
    
    return jsonify(data)


def to_str(val):
    s = isinstance(val, str)
    return ('{}','\'{}\'')[s].format(val)


def post_helper(table, return_data = False):
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
    if len(data) == 0: return 'Success!'
    pairs = ', '.join([f'{k} = {to_str(v)}' for k, v in data.items() if k != key])
    query = f'UPDATE {table} SET {pairs} WHERE {key} = {val}'
    execute(query, commit = True)
    return data if return_data else 'Success!'


def delete_helper(table, val, key = 'id'):
    query = f'DELETE FROM {table} WHERE {key} = {val}'
    execute(query, commit = True)
    return 'Success!'
