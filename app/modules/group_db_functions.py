## IMPORTS ##

# Import modules
import uuid
from flask import request

# Import functions
from app.database import Database
from .misc_functions import get_current_date
from .user_db_functions import update_user_groups

def create_group_db(user_name, user_id, group_name):

    # Set timestamp
    timestamp = get_current_date()

    # Validate if group exists
    group_exists = validate_group(group_name)

    # If group doesn't exist, insert data into database
    if group_exists != 0:
        Database.insert_one('Groups', {
            "group_id": uuid.uuid4().hex,
            "name": group_name,
            "owner": user_name, # same as the logged in user
            "owner_id": user_id,
            "members": [],
            "createdAt": timestamp
        })
        update_user_groups(user_name, group_name)
        result_msg = "Grupo criado com sucesso."
    else:
        result_msg = "Grupo já existe."

    return result_msg

def read_group_db(groups):

    print(f"I'M HERE!!! 2")

    groups_details = []

    for group in groups:
        print(f"GROUP: {group}")
        group_data = Database.find_one('Groups', {"name": group})
        if group_data:
            groups_details += [{
                "id": group_data['group_id'],
                "name": group_data['name'],
                "owner": group_data['owner'],
                "createdAt": group_data['createdAt']
            }]

    print(f"GROUPS DETAILS: {groups_details}")

    return groups_details

def read_group_by_id(id):

    group_data = Database.find_one('Groups', {"group_id": id})

    group = group_data['name']

    return group

def update_group():

    return 0

def delete_group_db(id):

    Database.delete_one('Groups', {"group_id": id})

    return 0

def validate_group(name):

    return 1

def create_group_player():

    group_id = 0
    player_id = 0

    Database.insert_one('Groups_players', {
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