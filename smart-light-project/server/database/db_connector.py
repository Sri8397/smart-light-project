from pymongo import MongoClient
from core.state_manager import state

# Get the database URI and name from the configuration
db_config = state.get_config()["db"]
uri = db_config["uri"]
database_name = db_config["database_name"]

# Connect to MongoDB
client = MongoClient(uri)
db = client[database_name]

# Access collections using the config data
motion_logs_collection = db[db_config["motion_logs_collection"]]
devices_collection = db[db_config["devices_collection"]]
video_metadata_collection = db[db_config["video_metadata_collection"]]

# video_metadata_collection.update_many(
#     {"location": {"$exists": False}},
#     {"$set": {"location": "rpi"}}
# )

# video_metadata_collection.create_index("location")
