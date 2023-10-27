## IMPORTS ##

# Import modules
from flask import request, render_template, redirect, url_for, flash, session
from app import app
import configparser
import os

# Import functions
from .user_db_functions import create_user, validate_login, get_user_groups, read_users
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
        return redirect(url_for('profile', id = session['user_id']))
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

    groups_list = get_user_groups(id)

    # If the user is part of any group
    if groups_list:
        groups_details = read_group(groups_list)
    else:
        groups_details = ""

    # return render_template("profile/profile.html", name = session['name'], groups = groups_details)
    return render_template("profile/profile.html", groups = groups_details)

# See group details
@app.route('/group/<id>')
def group(id):

    group = read_group_by_id(id)
    list_users = read_users()

    return render_template("profile/group.html", group = group, users = list_users)

# Create group
@app.route('/create-group', methods =  ["POST"])
def create_group():

    group_name = request.form['group']

    result_msg = create_group_db(session['name'], session['user_id'], group_name)
    flash(result_msg)

    return redirect(url_for('profile', id = session['user_id']))