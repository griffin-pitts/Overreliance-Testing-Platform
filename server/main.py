import os
import pprint

from dotenv import load_dotenv, find_dotenv
from pymongo import MongoClient

load_dotenv(find_dotenv())

password = os.environ.get("MONGO_PWD")

connection_string = f"""mongodb+srv://weedguetmildort:{password}@data-collection-cluster.vm2mi2k.mongodb.net/?retryWrites=true&w=majority&appName=Data-Collection-Cluster"""

client = MongoClient(connection_string)

dbs = client.list_database_names()
test_db = client.test
collections = test_db.list_collection_names()
print(dbs)
print(collections)

def insert_test_doc():
  collection = test_db.test
  test_document = {
    "name": "John"
    "type": "Test"
  }
  inserted_id = collection.insert_one(test_document).inserted_id
  print(inserted_id)

production = client.production
person_collection = production.person_collection

def create_documents():
  first_names = ["Ang", "Aaron"]
  last_names = ["Rum", "Ping"]
  ages = [28, 45]

  doc = []

  for first_name, last_name, age in zip(first_names, last_names, age):
    doc = {"first_name": first_name, "last_name": last_name, "age": age}
    docs.append(doc)
    #person_collection.insert_one(doc)

  person_collection.insert_many(docs)

create_documents()
  
