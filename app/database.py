## IMPORTS ##

# Import modules
import pymongo
from pymongo.errors import ServerSelectionTimeoutError
import configparser

# Read configuration file
config = configparser.ConfigParser()
config.read('configs/configs.ini')

# Database object
class Database(object):
    mongodb_conn_string = config['database']['MONGODB_CONN_SRTING']
    DATABASE = None

    # Initiate DB connection
    @staticmethod
    def initialize():
        mongodb = pymongo.MongoClient(Database.mongodb_conn_string, tls = True, tlsCertificateKeyFile = 'configs/mongodb_cert.pem')
        Database.DATABASE = mongodb['MatchTracker']

    # Insert many method
    @staticmethod
    def insert(collection, data):
        Database.DATABASE[collection].insert(data)

    # Insert one method
    @staticmethod
    def insert_one(collection, data):
        Database.DATABASE[collection].insert_one(data)

    # Find many method
    @staticmethod
    def find(collection, query, projection):
        return Database.DATABASE[collection].find(query, projection)

    # Find many method
    @staticmethod
    def find_one(collection, query):
        return Database.DATABASE[collection].find_one(query)

    # Delete one method
    @staticmethod
    def delete_one(collection, data):
        Database.DATABASE[collection].delete_one(data)

    # Update one method
    @staticmethod
    def update_one(collection, query, data):
        Database.DATABASE[collection].update_one(query, data)

# Database initialization
def db_init():
    print("Initializing database...")
    Database.initialize()

# Build database
'''
    NOTE: ONLY FOR MANUAL EXECUTION!!!
'''
def build_database():

    return 0