from database.db_connector import db

def save_motion_event(data):
    db.motion_logs.insert_one(data)

def save_device_status(data):
    db.devices.update_one(
        {"mac_address": data["mac_address"]},
        {"$set": data},
        upsert=True
    )
