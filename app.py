# create flask server
from re import A
from flask import (
    Flask,
    render_template,
    request,
)
from werkzeug.utils import secure_filename
import os
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
from flask_cors import CORS, cross_origin
import config as cfg
import pyodbc
from flask_bootstrap import Bootstrap


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
socketio = SocketIO(app)

bootstrap = Bootstrap(app)
mqtt = Mqtt(app)

ALLOWED_EXTENSIONS = set(["png", "jpg", "jpeg", "gif"])
page_config = {
    "title": cfg.title,
    "name": cfg.name,
    "tank_number": cfg.tank_number,
}

@app.route("/")
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def index():
    # get the first image name from static/images
    image_names = os.listdir("static/images/map")
    if len(image_names) > 0:
        first_image_name = image_names[0]
    else:
        first_image_name = None
    return render_template("index.html", image_name=first_image_name, page_config=page_config)


# @app.route("/save_image", methods=["POST"])
# def save_image():
#     # save image to static/images
#     # from ImmutableMultiDict([('image', <FileStorage: 'image.png' ('image/png')>)])
#     image = request.files["image"]
#     # delete all images in static/images
#     for file in os.listdir("static/images/map"):
#         os.remove(os.path.join("static/images/map", file))
#     # save image to static/images
#     image.save(os.path.join("static/images/map", secure_filename(image.filename)))
#     return {"status": "ok", "image_name": image.filename}

@app.route("/tank_history", methods=["POST"])
def tank_history():
    data = request.get_json()
    from_date = data["from_date"]
    to_date = data["to_date"]
    tankno = data["tankno"]
    # get data from sql server
    # connect to sql server
    conn = pyodbc.connect(
        "Driver={SQL Server};"
        f"Server={cfg.server_name};"
        f"Database={cfg.database};"
    )
    cursor = conn.cursor()
    # get data from sql server
    cursor.execute(
        f"SELECT * FROM {cfg.table_tank} WHERE storedate >= '{from_date}' AND storedate <= '{to_date}' AND tankno = '{tankno}' ORDER BY storedate DESC"
    )
    column = [column[0] for column in cursor.description]
    rows = cursor.fetchall()
    tank_data = []
    for row in rows:
        temp=dict(zip(column, row))
        temp["storedate"] = temp["storedate"].strftime("%Y-%m-%d %H:%M:%S")
        tank_data.append(temp)
    return {
        "status": "ok",
        "data": tank_data
    }

@app.route("/history", methods=["GET"])
def history():
    return render_template("history.html", page_config=page_config)

@app.route("/product_history", methods=["POST"])
def product_history():
    data = request.get_json()
    from_date = data["from_date"]
    to_date = data["to_date"]
    idproduct = data["idproduct"]
    # get data from sql server
    # connect to sql server
    conn = pyodbc.connect(
        "Driver={SQL Server};"
        f"Server={cfg.server_name};"
        f"Database={cfg.database};"
    )
    cursor = conn.cursor()
    # get data from sql server
    cursor.execute(
        f"SELECT * FROM {cfg.table_product} WHERE storedate >= '{from_date}' AND storedate <= '{to_date}' AND idproduct = '{idproduct}' ORDER BY storedate DESC"
    )
    column = [column[0] for column in cursor.description]
    rows = cursor.fetchall()
    product_data = []
    for row in rows:
        temp=dict(zip(column, row))
        temp["storedate"]=temp["storedate"].strftime("%Y-%m-%d %H:%M:%S")
        product_data.append(temp)

    return {
        "status": "ok",
        "data": product_data
    }

# socketio.emit("mqtt_message", data, namespace="/test")
@socketio.on("mqtt_message")
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def handle_mqtt_message(message):
    data = message["tank_data"]
    socketio.emit("mqtt_message", data)


@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe(app.config["MQTT_LAST_WILL_TOPIC"])


@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    # send message to client
    socketio.emit("mqtt_message", message.payload.decode())

if __name__ == '__main__':
   socketio.run(app, host='0.0.0.0', port=4000, use_reloader=False)
