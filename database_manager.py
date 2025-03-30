import pymongo
import streamlit as st
import extra_streamlit_components as stx
import datetime
import time


def get_manager():
    return stx.CookieManager()

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
        return
    db = client.hoohacks25bas
    collection = db[collection_name]
    collection.insert_one(document)
    st.success("Data inserted successfully!")
    
#adds one to a user's score
def add_score(client : pymongo.MongoClient, user_id : str, collection_name : str):
    if not client:
        client = init_connection()
    if collection_name not in client.hoohacks25bas.list_collection_names():
        st.error("Collection does not exist")
        return False
    
    db = client.hoohacks25bas
    collection = db[collection_name]
    result = collection.find_one({"id": user_id})
    st.write(result)
    if not "last_scored" in result:
        collection.update_one({"id": user_id}, {"$inc": {"score": 1}, "$set": {"last_scored": datetime.datetime.now()}})
        return True
    elif (datetime.datetime.now() - result['last_scored']).total_seconds() > 300:
        collection.update_one({"id": user_id}, {"$inc": {"score": 1}, "$set": {"last_scored": datetime.datetime.now()}})
        return True
    else:
        return False
    
#     #adds one to a user's score
# def attempt_add_score(collection_name : str, manager) -> bool:
#     client = init_connection()
#     if collection_name not in client.hoohacks25bas.list_collection_names():
#         st.error("Collection does not exist")
#         return False
#     db = client.hoohacks25bas
#     collection = db[collection_name]
#     result = collection.find()
#     result = list(result)
#     if "manager" in st.session_state:
#         cookie = st.session_state.get("manager").get("user_email")
#         time.sleep(2)
#     else:
#         st.error("Cookie manager not found in session state")
#         return False
#     if cookie is None:
#         st.error("User email not found in cookies")
#         return False
#     person = collection.find_one({"id": str(cookie)})
#     if 'last_scored' not in person or (datetime.datetime.now() - person['last_scored']).total_seconds() < 500:
#         collection.update_one({"id": str(cookie)}, {"$inc": {"score": 1}, "$set": {"last_scored": datetime.datetime.now()}})
#         client.close()
#         return True
#     else:
#         client.close()
#         return False

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