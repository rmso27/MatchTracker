## IMPORTS ##

# Import modules
from flask import request, render_template, redirect, url_for, flash, session
from app import app
import configparser
import os

# Import functions
from .user_db_functions import create_user, validate_login

## MAIN VARS ##

# Session setup
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = os.urandom(12)

## ROUTES ##

# Home
@app.route('/')
def home():

    return render_template("public/index.html")

# Login
@app.route('/login', methods =  ["POST"])
def login():

    # Reset login cookie
    session['logged_in'] = False
    session['user'] = None

    # Validate login
    result_msg = validate_login()

    # If login is successful
    if session['logged_in'] == True:
        return redirect(url_for('profile', id = session['user']))
    else:
        flash(result_msg)

    return redirect(url_for('home'))

# Register
@app.route('/register')
def register():

    return render_template("public/register.html")

# Create account
@app.route('/create-account', methods =  ["POST"])
def create_account():

    # Create account and flash result message
    result_msg = create_user()
    flash(result_msg)

    return redirect(url_for('register'))

# Personal page
@app.route('/profile/<id>')
def profile(id):

    return render_template("public/profile.html", name = session['name'])

# See group details
@app.route('/group/1')
def group():

    return render_template("public/group.html")