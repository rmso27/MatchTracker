## IMPORTS ##

# Import modules
import bcrypt
import uuid
from flask import request, session

# Import functions
from app.database import Database
from .misc_functions import get_current_date, hash_me

## FUNCTIONS ##

# # Initialize database
# def db_init():
#     Database.initialize()

# Create user
def create_user():

    # Set timestamp
    timestamp = get_current_date()

    # Validate if user exists
    # user_exists = validate_user(request.form['user'])
    user_exists = 1

    # If user doesn't exist, insert data into database
    if user_exists != 0:
        Database.insert_one('Users', {
            "user_id": uuid.uuid4().hex,
            "name": request.form['name'],
            "email": request.form['email'],
            "user": request.form['user'],
            "password": hash_me(request.form['password']),
            "groups": [],
            "createdAt": timestamp,
        })
        result_msg = "A sua conta foi criada com sucesso."
    else:
        result_msg = "A conta já existe."

    return result_msg

# Read user
def read_user():

    return 0

# Update user groups
def update_user_groups(user_name, group_name):

    '''
        This function is used when we add a user to a group.
        An object is created with the group name and with the values wins, draws and loses
        set to 0.
    '''

    groups_data = {"group": group_name, "wins": 0, "draws": 0, "loses": 0}
    Database.update_one('Users', {"name": user_name}, {"$push": {"groups": groups_data}})

# Delete user
def delete_user():

    return 0

# # Validate user
# def validate_user(user):

#     # Query database for user data
#     if Database.find_one('Users', {"user": user}):
#         user_exists = 0
#     else:
#         user_exists = 1

#     return user_exists

def read_users():

    list_users = []
    users = Database.find('Users', {}, {'name': 1})
    for user in users:
        list_users += [user['name']]

    return list_users

# Validate login
def validate_login():

    # Query database for user data
    user = Database.find_one('Users', {"user": request.form['user']})

    # If the user exists, validate password and set login status
    if user and bcrypt.checkpw(request.form['password'].encode('utf-8'), user['password']):
        session['logged_in'] = True
        session['user_id'] = user['user_id']
        session['name'] = user['name']
    else:
        result_msg = "Autenticação falhou."
        return result_msg

def get_user_groups(user_id):

    # Query database for user data
    user = Database.find_one('Users', {"user_id": user_id})

    groups_list = user['groups']

    return groups_list
