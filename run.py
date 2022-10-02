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
from flask_socketio import SocketIO
from flask_cors import CORS, cross_origin
import config as cfg
# add package for connect to sql server
import pyodbc
import json
import datetime
import time

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
socketio = SocketIO(app)

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


@app.route("/save_image", methods=["POST"])
def save_image():
    # save image to static/images
    # from ImmutableMultiDict([('image', <FileStorage: 'image.png' ('image/png')>)])
    image = request.files["image"]
    # delete all images in static/images
    for file in os.listdir("static/images/map"):
        os.remove(os.path.join("static/images/map", file))
    # save image to static/images
    image.save(os.path.join("static/images/map", secure_filename(image.filename)))
    return {"status": "ok", "image_name": image.filename}

@app.route("/history", methods=["GET"])
def history():
    # get data from sql server
    # connect to sql server
    conn = pyodbc.connect(
        "Driver={SQL Server};"
        "Server={};"
        "Database={};".format(cfg.server_name, cfg.database),
    )
    cursor = conn.cursor()
    # get data from sql server
    sql = "SELECT * FROM {} ORDER BY ID DESC LIMIT 10".format(cfg.table_tank)
    cursor.execute(sql)
    rows = cursor.fetchall()
    print(rows)
    # get data from sql server
    sql = "SELECT * FROM {} ORDER BY ID DESC LIMIT 10".format(cfg.table_product)
    cursor.execute(sql)
    rows1 = cursor.fetchall()
    print(rows1)
    return "ok"


# socketio.emit("mqtt_message", data, namespace="/test")
@socketio.on("mqtt_message", namespace="/test")
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def handle_mqtt_message(message):
    print("ldsfajlkd")
    print("message received socket: ", message)
    socketio.emit("mqtt_message", message, namespace="/test")


@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe(app.config["MQTT_LAST_WILL_TOPIC"])


@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    print("message dslak received: ", message.payload.decode())
    # send message to client
    socketio.emit("mqtt_message", message.payload.decode(), namespace="/test")



if __name__ == "__main__":
    # app.run(port=5000, debug=True)
    socketio.run(
        app, host="127.0.0.1", port=5000, use_reloader=False, debug=True
    )
