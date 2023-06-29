## IMPORTS ##

# Import modules
from flask import request, render_template, redirect, url_for, flash, session
from app import app
import configparser
import os

# Import functions
from .user_db_functions import create_user, validate_login, get_user_groups
from .group_db_functions import create_group_db, read_group, read_group_by_id

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

    # groups_list = get_user_groups(id)

    # print(f"GROUPS LIST: {groups_list}")

    groups_details = read_group('Manquilha')

    print(f"GROUP DETAILS: {groups_details}")

    return render_template("profile/profile.html", name = session['name'], groups = groups_details)

# See group details
@app.route('/group/<id>')
def group(id):

    group = read_group_by_id(id)

    return render_template("profile/group.html", group = group)

# Create group
@app.route('/create-group', methods =  ["POST"])
def create_group():

    create_group_db()

    return redirect(url_for('profile', id = session['user']))