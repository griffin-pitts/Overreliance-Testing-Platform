from flask import Flask, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash, generate_password_hash
from wtforms.validators import DataRequired, Email, Length
from pymongo import MongoClient

client = MongoClient('your_mongo_uri')
db = client['Userdata']
usersCollection = db['Users']

def user_creation(email, password, usertype):
    post={"_id": email, "password": generate_password_hash(password)}

# username = email
def auth_user(username, password):
    user = usersCollection.find_one({"_id": username})
    if user and check_password_hash(user['password'], password):
        return True
    return False

def loginRequired(f):
    @wraps(f)
    def decor_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decor_function

def login(username, password):
    if auth_user(username, password):
        session['user'] = username
        return True
    else:
        flash('Invalid username or password')
        return False
    
def logout():
    session.pop('user', None)
