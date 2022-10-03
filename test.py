# create flask server
from re import A
from flask import (
    Flask,
    flash,
    render_template,
    request,
    redirect,
    url_for,
    session,
)
from werkzeug.utils import secure_filename
import os
from flask_mqtt import Mqtt
# from flask_socketio import SocketIO
from flask_cors import CORS, cross_origin
import config as cfg
# add package for connect to sql server
import json
import datetime

app = Flask(__name__)
cors = CORS(app, resources={r"/foo": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["MQTT_BROKER_URL"] = cfg.mqtt_url
app.config["MQTT_BROKER_PORT"] = cfg.mqtt_port
app.config["MQTT_USERNAME"] = cfg.mqtt_username
app.config["MQTT_PASSWORD"] = cfg.mqtt_password
app.config["MQTT_KEEPALIVE"] = 5
app.config["MQTT_TLS_ENABLED"] = False
app.config["MQTT_LAST_WILL_TOPIC"] = cfg.mqtt_topic
mqtt = Mqtt(app)
# socketio = SocketIO(app)

ALLOWED_EXTENSIONS = set(["png", "jpg", "jpeg", "gif"])


@app.route("/")
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def index():
    # get the first image name from static/images
    image_names = os.listdir("static/images/map")
    if len(image_names) > 0:
        first_image_name = image_names[0]
    else:
        first_image_name = None
    return render_template("index.html", image_name=first_image_name)


@app.route("/config", methods=["GET"])
def config():
    return render_template("config.html")



@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe(app.config["MQTT_LAST_WILL_TOPIC"])


@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    print("message dslak received: ", message.payload.decode())
   



if __name__ == "__main__":
    app.run(port=5000, debug=True)
   
