## IMPORTS ##

# Import modules
import uuid
from flask import request

# Import functions
from .database import Database
from .misc_functions import get_current_date
from .user_db_functions import update_user_groups

def create_group_db(user_name, user_id, group_name):

    # Set timestamp
    timestamp = get_current_date()

    # Validate if group exists
    group_exists = validate_group(group_name)

    # If group doesn't exist, insert data into database
    if group_exists != 0:
        Database.insert_one('groups', {
            "group_id": uuid.uuid4().hex,
            "name": group_name,
            "owner": user_name, # same as the logged in user
            "owner_id": user_id,
            "createdAt": timestamp
        })
        update_user_groups(user_name, group_name)
        result_msg = "Grupo criado com sucesso."
    else:
        result_msg = "Grupo já existe."

    return result_msg

def read_group(groups):

    groups_details = []

    for group in groups:
        group_data = Database.find_one('groups', {"name": group})
        if group_data:
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

def create_group_player():

    group_id = 0
    player_id = 0

    Database.insert_one('groups_players', {
        "group_id": group_id,
        "player_id": player_id,
        "matches": 0,
        "wins": 0,
        "draws": 0,
        "losses": 0,
        "ratio": "0.00%",
        "points": 0,
    })

    return 0