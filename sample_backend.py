from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS
import random
import string

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    return 'Hello, World!'

users = { 
    'users_list' : []
    # [
    #     { 
    #      'id' : 'xyz789',
    #      'name' : 'Charlie',
    #      'job': 'Janitor',
    #     },
    #     {
    #      'id' : 'abc123', 
    #      'name': 'Mac',
    #      'job': 'Bouncer',
    #     },
    #     {
    #      'id' : 'ppp222', 
    #      'name': 'Mac',
    #      'job': 'Professor',
    #     }, 
    #     {
    #      'id' : 'yat999', 
    #      'name': 'Dee',
    #      'job': 'Aspring actress',
    #     },
    #     {
    #      'id' : 'zap555', 
    #      'name': 'Dennis',
    #      'job': 'Bartender',
    #     }
    # ]
}

# Testing format: http://localhost:5000/users?name=Mac&job=Bouncer
@app.route('/users', methods=['GET', 'POST', 'DELETE'])
def get_users():
    if request.method == 'GET':
        search_username = request.args.get('name')
        search_job = request.args.get('job')
        if search_username and search_job:
            subdict = {'users_list' : []}
            for user in users['users_list']:
                if user['name'] == search_username and user['job'] == search_job:
                    subdict['users_list'].append(user)
            return subdict
        elif search_username:
            subdict = {'users_list' : []}
            for user in users['users_list']:
                if user['name'] == search_username:
                    subdict['users_list'].append(user)
            return subdict
        elif search_job:
            subdict = {'users_list' : []}
            for user in users['users_list']:
                if user['job'] == search_job:
                    subdict['users_list'].append(user)
            return subdict
        return users
    elif request.method == 'POST':
        userToAdd = request.get_json()
        userToAdd['id'] = generateID()
        users['users_list'].append(userToAdd)
        resp = jsonify(userToAdd)
        resp.status_code = 201 # set a response code. 
        return resp
    elif request.method == 'DELETE':
        userToDelete = request.get_json(silent=True)
        try:
            users['users_list'].remove(userToDelete)
            resp = jsonify(success=True)
            resp.status_code = 204 # set a response code. 
            return resp
        except:
            resp = jsonify(success=False)
            resp.status_code = 404 # set a response code. 
            return resp

@app.route('/users/<id>', methods=['GET', 'DELETE'])
def get_user(id):
    if id :
        for user in users['users_list']:
            if user['id'] == id:
                if request.method == 'GET':
                    return user
                elif request.method == 'DELETE':
                    users['users_list'].remove(user)
                    resp = jsonify(success=True)
                    resp.status_code = 204 # set a response code. 
                    return resp
        resp = jsonify(success=False)
        resp.status_code = 404 # set a response code.
        return resp
    return users


def generateID():
    userID = ''
    userID += "".join(random.choice(string.ascii_lowercase) for i in range(3))
    userID += "".join(random.choice(string.digits) for i in range(3))
    return userID
