from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db
from datetime import timedelta


# Execute a SQL query/statement
def execute(query, commit = False):
    current_app.logger.info(query)
    cursor = db.get_db().cursor()
    cursor.execute(query)
    if commit: db.get_db().commit()
    return cursor


# Helper function for GET requests
def get_helper(query):
    cursor = execute(query)
    cols = [x[0] for x in cursor.description]
    data = [dict(zip(cols, row)) for row in cursor.fetchall()]
    return jsonify(data)


# Places quotations around a value if it's a string
def to_sql_str(val):
    s = isinstance(val, str)
    return ('{}','\'{}\'')[s].format(val)


# Helper function for POST requestions adding a row to a table
def post_helper(table, return_data = False):
    data = request.json
    current_app.logger.info(data)
    cols = ', '.join(data.keys())
    vals = ', '.join([to_sql_str(v) for v in data.values()])
    query = f'INSERT INTO {table} ({cols}) VALUES ({vals})'
    execute(query, commit = True)
    return data if return_data else 'Success!'


# Helper function for PUT requests on an ID from a table
def put_helper(table, val, key = 'id', data = None, return_data = False):
    if data is None: data = request.json
    current_app.logger.info(data)
    if len(data) == 0: return 'Success!'
    pairs = ', '.join([f'{k} = {to_sql_str(v)}' for k, v in data.items() if k != key])
    query = f'UPDATE {table} SET {pairs} WHERE {key} = {val}'
    execute(query, commit = True)
    return data if return_data else 'Success!'


# Helper function for DELETE requests of an ID from a table
def delete_helper(table, val, key = 'id'):
    query = f'DELETE FROM {table} WHERE {key} = {val}'
    execute(query, commit = True)
    return 'Success!'
