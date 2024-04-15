########################################################
# Sample customers blueprint of endpoints
# Remove this file if you are not using it in your project
########################################################
from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db


customers = Blueprint('customers', __name__)

# Get all customers from the DB
@customers.route('/customers', methods=['GET'])
def get_customers():
    cursor = db.get_db().cursor()
    cursor.execute('SELECT id, company, last_name, first_name, job_title, business_phone FROM customers')
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Get customer detail for customer with particular userID
@customers.route('/customers/<userID>', methods=['GET'])
def get_customer(userID):
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM customers WHERE id = {0}'.format(userID))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Update customer information based on ID
@customers.route('/customers/<userID>', methods=['PUT'])
def new_customer():
    data = request.json
    current_app.logger.info(data)
    phone = data['business_phone']
    id = data['id']
    company = data['company']
    lname = data['last_name']
    fname = data['first_name']
    job = data['job_title']

    query = 'insert into customers (business_phone, company, first_name, id, job_title, last_name) values ("'
    query += str(phone)+ '", "'
    query += company + '", "'
    query += fname + '", "'
    query += str(id)+ '", "'
    query += job + '", '
    query += lname + ')'
    current_app.logger.info(query)

# executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Success!'