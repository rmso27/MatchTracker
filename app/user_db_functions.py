## IMPORTS ##

# Import modules
import bcrypt
import uuid
from flask import request, session

# Import functions
from .database import Database
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
    user_exists = validate_user(request.form['email'])

    # If user doesn't exist, insert data into database
    if user_exists != 0:
        Database.insert_one('users', {
            "_id": uuid.uuid4().hex,
            "user_id": "1",
            "name": request.form['name'],
            "email": request.form['email'],
            "password": hash_me(request.form['password']),
            "createdAt": timestamp
        })
        result_msg = "Account created successfully."
    else:
        result_msg = "Account already exists."

    return result_msg

def read_user():

    return 0

def delete_user():

    Database.delete_one('users', {"email": email})

    return 0

# Validate user
def validate_user(email):

    # Query database for user data
    if Database.find_one('users', {"email": email}):
        user_exists = 0
    else:
        user_exists = 1

    return user_exists

# Validate login
def validate_login():

    # Query database for user data
    user = Database.find_one('users', {"email": request.form['email']})

    # If the user exists, validate password and set login status
    if user and bcrypt.checkpw(request.form['password'].encode('utf-8'), user['password']):
        session['logged_in'] = True
        session['user'] = user['user_id']
        session['name'] = user['name']
    else:
        result_msg = "Authentication failed."
        return result_msg
