from pymongo import MongoClient
from core.state_manager import state

config = state.get_config()["mongodb"]

client = MongoClient(config["uri"])
db = client[config["db"]]

def get_db():
    return db
