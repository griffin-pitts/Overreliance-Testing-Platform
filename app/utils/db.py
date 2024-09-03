# Libraries
import os
import pprint

# Imports
from dotenv import load_dotenv, find_dotenv
from pymongo import MongoClient
from urllib.parse import quote_plus
from .encryption_utils import encrypt_email, decrypt_email



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
        # Decrypt email
        decrypted_email = decrypt_email(user.get("email"))

        # Compare email
        if decrypted_email == user_email:
            return True
  
    return False

def insert_user(user_email):
    users_collection = init_db()

    # Check if user already exists
    if find_user(user_email):
        print("User already exists!")
        return
    
    # Encrypt email otherwise
    encrypted_email = encrypt_email(user_email)

    data = {
        "email": encrypted_email
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

def insert_user_response(user_id, responses):
    users_collection = init_db()
    from bson.objectid import ObjectId
    _id = ObjectId(user_id)

    query = {"_id": _id}

    update = {"$set": {"responses": responses}}
    result = users_collection.update_one(query, update)

    if result:
        print("success!")
    else:
        print("failed!")


# Add more functions as needed


# Testing lines

user_id = "66bf718f19aab530b26cd132"

responses = {
    "question_1": "choice_d",
    "question_2": "choice_d",
}

# insert_user("user2@example.com")
insert_user_response(user_id, responses)

