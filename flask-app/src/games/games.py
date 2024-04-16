from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db


games = Blueprint('games', __name__)

# Get all the games from the database
@games.route('/games', methods=['GET'])
def get_products():
    # get a cursor object from the database
    cursor = db.get_db().cursor()
 
    # create a query to get the games with the teams names and sport
    query = """SELECT g.gameID AS gameID, g.dateTime AS dateTime, g.location AS location, t1.name AS 'Team 1',
            g.team1_score AS 'Team 1 Score', t2.name AS 'Team 2', g.team2_score AS 'Team 2 Score', s.name AS Sport
            FROM games AS g 
            JOIN teams AS t1 ON g.team1_ID = t1.teamID AND g.team1_sportID = t1.sportID
            JOIN teams AS t2 ON g.team2_ID = t2.teamID AND g.team2_sportID = t2.sportID
            JOIN sports AS s ON s.sportID = t1.sportID;"""
    # use cursor to query the database for a list of games
    cursor.execute(query)

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