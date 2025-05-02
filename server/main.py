from flask import Flask
from api.routes import routes
from core.mqtt_handler import client  # ensure MQTT runs

app = Flask(__name__)
app.register_blueprint(routes)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
