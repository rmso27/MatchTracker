## IMPORTS ##

# Import modules
import uuid
from flask import request

# Import functions
from .database import Database
from .misc_functions import get_current_date
from .user_db_functions import update_user

def create_group_db():

    # Set timestamp
    timestamp = get_current_date()

    group_name = "Manquilha"
    owner = "Ruben Oliveira"

    # Validate if user exists
    group_exists = validate_group(group_name)

    # If user doesn't exist, insert data into database
    if group_exists != 0:
        Database.insert_one('groups', {
            "group_id": uuid.uuid4().hex,
            "name": group_name,
            "owner": owner, # same as the logged in user
            "createdAt": timestamp
        })
        result_msg = "Grupo criado com sucesso."
    else:
        result_msg = "Grupo já existe."

    return result_msg

def read_group(groups):

    groups_details = []

    for group in groups:
        group_data = Database.find_one('groups', {"name": group})
        groups_details += [{
            "id": group_data['group_id'],
            "name": group_data['name'],
            "owner": group_data['owner'],
            "createdAt": group_data['createdAt']
        }]

    return groups_details

def read_group_by_id(id):

    group_data = Database.find_one('groups', {"group_id": id})

    print(f"DATA: {group_data}")

    group = group_data['name']

    return group

def update_group():

    return 0

def delete_group():

    return 0

def validate_group(name):

    return 1