from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Request
from core.mqtt_client import mqtt_client
from fastapi.responses import JSONResponse
from core.state_manager import state
from database.db_connector import db, video_metadata_collection, motion_logs_collection, devices_collection, led_status_collection
from bson.json_util import dumps
from pathlib import Path
import os
import json 
from datetime import datetime
from core.state_manager import state

config = state.get_config()["mqtt"]


router = APIRouter()

@router.post("/upload_video")
async def upload_video(
    file: UploadFile = File(...),
    mac_address: str = Form(...),
    filename: str = Form(...)
):
    try:
        # Ensure directory exists
        dir_path = Path(__file__).resolve().parent.parent / "videos" 
        os.makedirs(dir_path, exist_ok=True)
        file_path = os.path.join(dir_path, filename)

        # Save the uploaded file
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        video_metadata_collection.update_one(
            {"video_file": filename},
            {"$set": {"location": "server", "timestamp": datetime.utcnow().isoformat()}},
            upsert=True
        )

        # Prepare and send ACK via MQTT
        ack_payload = {
            "mac_address": mac_address,
            "filename": filename,
            "status": "received"
        }
        mqtt_client.publish_event("video_upload_ack", ack_payload)
        
        return {"status": "success", "message": "Video uploaded and ACK sent."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


# GET /api/logs - Get all events (from MongoDB)
@router.get("/logs")
async def get_logs():
    try:
        logs = list(motion_logs_collection.find())
        serialized_logs = []
        for log in logs:
            log["_id"] = str(log["_id"])
            serialized_logs.append(log)
        return serialized_logs
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": f"Failed to retrieve logs: {str(e)}"})

# GET /api/devices - List connected devices
@router.get("/devices")
async def get_devices():
    try:
        devices = list(devices_collection.find())
        seriealized_devices = []
        for device in devices:
            device["_id"] = str(device["_id"])
            seriealized_devices.append(device)
        return seriealized_devices
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": f"Failed to retrieve devices: {str(e)}"})

# POST /api/control - Send control command to RPi (e.g., turn on/off light)
@router.post("/control")
async def control_device(request: Request):
    try:
        data = await request.json()
        print(f"Received control request: {data}")
        mac = data.get("mac")
        action = data.get("action")
        print(f"MAC: {mac}, Action: {action}")

        if not mac or action not in ["on", "off"]:
            raise HTTPException(status_code=400, detail="Missing or invalid 'mac' or 'action'.")

        mqtt_client.publish_event("light_control", {
            "mac": mac,
            "action": action
        })

        led_status_collection.insert_one({
            "mac": mac,
            "action": action,
            "timestamp": datetime.utcnow().isoformat()
        })

        return {"status": "success", "message": f"Sent '{action}' command to device {mac}"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error sending control message: {e}")
