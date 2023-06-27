'''
    File that hosts all application misc functions:
        - password encryption;
        - get current date;
'''

## IMPORTS ##

# Import modules
import bcrypt
from datetime import datetime

## FUNCTIONS ##

# Password encryption
def hash_me(decrypted_pwd):

    # BCRYPT encryption
    encrypted_pwd = bcrypt.hashpw(decrypted_pwd.encode('utf-8'), bcrypt.gensalt())

    return encrypted_pwd

# Get current date
def get_current_date():

    '''
        Output example: '2022-10-28 13:48:41'
    '''

    # Current date
    current_date = datetime.now().replace(microsecond = 0)

    return current_date
