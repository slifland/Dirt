import pymongo
import streamlit as st

@st.cache_resource
def init_connection():
    return pymongo.MongoClient(
        f"mongodb+srv://slifland:{st.secrets.db_password}@cluster0.r3jmgkf.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

# Pull data from the collection.
def get_data(_client : pymongo.MongoClient, collection_name : str):
    if collection_name not in _client.hoohacks25bas.list_collection_names():
        st.error("Collection does not exist")
        return
    db = _client.hoohacks25bas
    items = db[collection_name].find()
    items = list(items)  # make hashable for st.cache_data
    return items

#inserts a document into the collection
def insert_data(document, collection_name : str):
    client = pymongo.MongoClient(
        f"mongodb+srv://slifland:{st.secrets.db_password}@cluster0.r3jmgkf.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    if(not dict(document)):
        st.error("Invalid Document format")
        return
    if collection_name not in client.hoohacks25bas.list_collection_names():
        st.error("Collection does not exist")
        print('Collection does not exist')
        return
    db = client.hoohacks25bas
    collection = db[collection_name]
    collection.insert_one(document)
    st.success("Data inserted successfully!")
    
#adds one to a user's score
def add_score(client : pymongo.MongoClient, user_id : str, collection_name : str):
    if collection_name not in client.hoohacks25bas.list_collection_names():
        st.error("Collection does not exist")
        return
    db = client.hoohacks25bas
    collection = db[collection_name]
    collection.update_one({"userID": user_id}, {"$inc": {"score": 1}})

#gets the id of the next up user
def get_new_id() -> int:
    client = pymongo.MongoClient(
        f"mongodb+srv://slifland:{st.secrets.db_password}@cluster0.r3jmgkf.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    db = client.hoohacks25bas
    collection = db['userInfo']
    items = collection.find().sort("userID", direction=pymongo.DESCENDING).limit(1)
    for item in items:
        return item['userID'] + 1
    return 0

#adds a user to the database if they do not exist
def add_user_if_necessary(user : dict):
    client = pymongo.MongoClient(
        f"mongodb+srv://slifland:{st.secrets.db_password}@cluster0.r3jmgkf.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    db = client.hoohacks25bas
    collection = db['userInfo']
    item = collection.find_one({"id": user['id']})
    if item is None:
        user['score'] = 0
        collection.insert_one(user)
        st.success("User added successfully!")
    else:
        st.success("User already exists!")
    

import json

def is_json(myjson):
  """
  Checks if a string is valid JSON.

  Args:
    myjson: The string to check.

  Returns:
    True if the string is valid JSON, False otherwise.
  """
  try:
    json.loads(myjson)
    return True
  except ValueError:
    return False