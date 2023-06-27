## IMPORTS ##

# Import modules
import uuid
from flask import request

# Import functions
from .database import Database
from .misc_functions import get_current_date

def create_group():

    # Set timestamp
    timestamp = get_current_date()

    # Validate if user exists
    group_exists = validate_group(request.form['name'])

    # If user doesn't exist, insert data into database
    if group_exists != 0:
        Database.insert_one('groups', {
            "_id": uuid.uuid4().hex,
            "group_id": "1",
            "name": request.form['name'],
            "owner": request.form['owner'], # same as the logged in user
            "members": "",
            "createdAt": timestamp
        })
        result_msg = "Grupo criado com sucesso."
    else:
        result_msg = "Grupo já existe."

    return result_msg

    return 0

def read_group():

    return 0

def update_group():

    return 0

def delete_group():

    return 0

def validate_group():

    return 0