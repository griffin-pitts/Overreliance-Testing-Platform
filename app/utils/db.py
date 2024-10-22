import os
import pprint
from dotenv import load_dotenv, find_dotenv
from pymongo import MongoClient
from urllib.parse import quote_plus

def init_db():
    # Temporarily return None for testing
    return None

def find_user(user_email):
    # Temporarily return False for testing
    return False

def insert_user(user_email):
    # Temporarily return None for testing
    return None

def update_user(user_email, updated_data):
    # Temporarily return None for testing
    return None

def delete_user(user_email):
    # Temporarily return None for testing
    return None

def insert_user_response(user_id, responses):
    # Temporarily print responses for testing
    print("Would save to DB:", responses)
    return None
