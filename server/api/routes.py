from flask import Blueprint, jsonify, request
from services.video_service import save_video
from core.device_registry import get_devices
from database.mongo_client import get_db
from core.mqtt_handler import send_control

routes = Blueprint("routes", __name__)
db = get_db()

@routes.route("/api/upload-video", methods=["POST"])
def upload_video():
    return save_video()

@routes.route("/api/devices", methods=["GET"])
def list_devices():
    return jsonify(get_devices())

@routes.route("/api/logs", methods=["GET"])
def get_logs():
    return jsonify(list(db.logs.find({}, {"_id": 0})))

@routes.route("/api/control", methods=["POST"])
def control_light():
    data = request.json
    send_control(data["mac_address"], data["command"])
    return {"status": "sent"}
