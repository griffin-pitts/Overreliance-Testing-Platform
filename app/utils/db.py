# Libraries
import os
import pprint

# Imports
from dotenv import load_dotenv, find_dotenv
from pymongo import MongoClient
from urllib.parse import quote_plus


# Functions for interacting with MongoDB
def init_db():
    # Load .env variables
    load_dotenv(find_dotenv())

    # Variables
    username = os.getenv('MONGODB_UID')
    cluster = os.getenv('MONGODB_CLUSTER_NAME')
    authSource = os.getenv('MONGODB_AUTH')
    password = quote_plus(os.getenv('MONGODB_PWD'))

    # URI string
    uri = username + ':' + password + '@' + cluster + authSource

    # Initialize MongoDB client
    client = MongoClient(uri)

    # Update later in production environment ---------------------------------- <<<
    # Connect to database
    users_db = client.test
    # ------------------------------------------------------------------------- <<<

    # Define your collections
    return users_db.users


def find_user(user_email):

    users_collection = init_db()
    users = users_collection.find()

    for user in users:
        # Assign email
        email = user.get("email")

        # Compare email
        if email == user_email:
            return True
  
    return False

def insert_user(user_email):
    users_collection = init_db()

    # Check if user already exists
    if find_user(user_email):
        print("User already exists!")
        return (-1)
    
    # Assign email otherwise
    email = user_email

    data = {
        "email": email
    }

    # Insert a new user into the database
    result = users_collection.insert_one(data)
    print("User successfully added!")
    return result.inserted_id

def update_user(user_email, updated_data):
    users_collection = init_db()
    # Update user data by email
    return users_collection.update_one({"_id": user_email}, {"$set": updated_data})

def delete_user(user_email):
    users_collection = init_db()
    # Delete a user by email
    return users_collection.delete_one({"_id": user_email})

def insert_user_response(responses):

    _id = insert_user(responses["email"])

    if (_id == -1):
        print("User already exist!")
        return

    responses["email"]
    responses["uf_id"]
    responses["question_order"]
    responses["answers"]
    responses["post_survey_answers"]
    responses["final_survey_answers"]


    users_collection = init_db()
    from bson.objectid import ObjectId
   

    query = {"_id": _id}

    update = {
        "$set": {
            "uf_id": responses["uf_id"],
            "question_order": responses["question_order"],
            "answers": responses["answers"],
            "post_survey_answers": responses["post_survey_answers"],
            "final_survey_answers": responses["final_survey_answers"]
        }
    }
    result = users_collection.update_one(query, update)

    if result:
        print("success!")
    else:
        print("failed!")


# Add more functions as needed
