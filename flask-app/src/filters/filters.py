from flask import Blueprint, request, jsonify, make_response
import json
from src import db


filters = Blueprint('filters', __name__)

# Get all the searches from the database
@filters.route('/filters', methods=['GET'])
def get_keywords_in():
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    # use cursor to query the database for a list of keywords to filter into search
    cursor.execute('SELECT Filter_Id, Keyword_One, Keyword_Two, Keyword_Three, Keyword_Four, Keyword_Five, Keyword_Six, Keyword_Seven, Keyword_Eight, Keyword_Nine, Keyword_Ten FROM Keywords_In')

    # grab the column headers from the returned data
    column_headers = [x[0] for x in cursor.description]

    # create an empty dictionary object to use in 
    # putting column headers together with data
    json_data = []

    # fetch all the data from the cursor
    theData = cursor.fetchall()

    # for each of the rows, zip the data elements together with
    # the column headers. 
    for row in theData:
        json_data.append(dict(zip(column_headers, row)))

    return jsonify(json_data)