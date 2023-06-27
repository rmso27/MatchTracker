from flask import Flask
from .database import db_init

app = Flask(__name__)
db_init()

from app import routes