import pymongo
import bcrypt
import streamlit as st

# Connect to MongoDB using Streamlit Secrets
@st.cache_resource
def init_connection():
    return pymongo.MongoClient(st.secrets["MONGO_URI"])

client = init_connection()
db = client["ManuscriptApp"]
users_collection = db["users"]

def create_user(username, password):
    if users_collection.find_one({"username": username}):
        return False # User exists
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    users_collection.insert_one({"username": username, "password": hashed})
    return True

# THIS IS THE FUNCTION IT IS LOOKING FOR:
def authenticate_user(username, password):
    user = users_collection.find_one({"username": username})
    if user:
        if bcrypt.checkpw(password.encode('utf-8'), user["password"]):
            return True
    return False