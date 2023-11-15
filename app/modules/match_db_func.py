## IMPORTS ##

# Import modules
import uuid

# Import functions
from app.database import Database
from .misc_functions import get_current_date

def create_match_db():

    # Set timestamp
    timestamp = get_current_date()

    Database.insert_one('matches', {
        "match_id": uuid.uuid4().hex,
        "date": "",
        "teamA": [], # same as the logged in user
        "teamB":  [],
        "result": [],
        "creator": "",
        "createdAt": timestamp
    })
    result_msg = "Grupo criado com sucesso."

    return result_msg