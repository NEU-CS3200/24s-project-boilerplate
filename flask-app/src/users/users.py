from blueprint_template import *
users = Blueprint('users', __name__)


# Gets all active users
@users.route('/users', methods = ['GET'])
def get_users():
    query = 'SELECT * FROM Users WHERE U.active'
    return get_helper(query)


# Add a new user
@users.route('/users', methods = ['POST'])
def post_user():
    return post_helper('Users')


# Gets all users that are managers of other users
@users.route('/managers', methods = ['GET'])
def get_managers():
    query = 'SELECT M.*, COUNT(M.id) AS numEmployees \
        FROM UserManagers UM JOIN Users M \
        ON UM.manager = M.id GROUP BY M.id'
    return get_helper(query)


# Edits the user associated with a given ID
@users.route('/users/<id>', methods = ['PUT'])
def put_user(id):
    return put_helper('Users', id)
