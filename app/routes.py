## IMPORTS ##

# Import modules
from flask import request, render_template, redirect, url_for, flash, session
from app import app
import configparser
import os

# Import functions
from .modules.user_db_functions import create_user, validate_login, get_user_groups, read_users, update_user_groups
from .modules.group_db_functions import create_group_db, read_group, read_group_by_id, delete_group_db

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
    session['user_id'] = None
    session['name'] = None

    # Validate login
    result_msg = validate_login()

    # If login is successful
    if session['logged_in'] == True:
        return redirect(url_for('profile', id = session['user_id']))
    else:
        flash(result_msg)

    return redirect(url_for('home'))

# Logout
@app.route('/logout')
def logout():

    # Reset login cookie
    session['logged_in'] = False
    session['user'] = None

    return redirect(url_for('home'))

# Register
@app.route('/register')
def register():

    return render_template("public/register.html")

# Create account
@app.route('/users', methods =  ["POST"])
def create_account():

    # Create account and flash result message
    result_msg = create_user()
    flash(result_msg)

    return redirect(url_for('register'))

# Personal page
@app.route('/users/<id>')
def profile(id):

    # Validate if the uer is logged in. If not, redirect to homepage.
    if session['logged_in'] == True:
        groups_list = get_user_groups(id)

        # If the user is part of any group
        if groups_list:
            groups_details = read_group(groups_list)
        else:
            groups_details = ""

        # Validate if current user is admin
        for group in groups_details:
            if session['name'] == group['owner']:
                group['isAdmin'] = True
            else:
                group['isAdmin'] = False
    else:
        return redirect(url_for('home'))

    return render_template("profile/profile.html", groups = groups_details)

# See group details
@app.route('/groups/<id>')
def group(id):

    # Validate if the uer is logged in. If not, redirect to homepage.
    if session['logged_in'] == True:
        group = read_group_by_id(id)
        list_users = read_users()
        session['group'] = group
        session['group_id'] = id
    else:
        return redirect(url_for('home'))

    return render_template("profile/group.html", group = group, users = list_users)

# Create group
@app.route('/groups', methods =  ["POST"])
def create_group():

    group_name = request.form['group']

    result_msg = create_group_db(session['name'], session['user_id'], group_name)
    flash(result_msg)

    return redirect(url_for('profile', id = session['user_id']))

# Add user to group
@app.route('/groups', methods = ["POST"])
def add_user_group():

    user_to_add = request.form.get('user')
    update_user_groups(user_to_add, session['group'])

    return redirect(url_for('group', id = session['group_id']))

# Delete group
@app.route('/groups/delete/<id>')
def delete_group(id):

    delete_group_db(id)

    return redirect(url_for('profile'), id = session['user_id'])
