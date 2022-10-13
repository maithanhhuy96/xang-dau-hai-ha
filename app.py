# create flask server
from re import A
from flask import (
    Flask,
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
import pyodbc
from flask_bootstrap import Bootstrap
import configparser
from datetime import timedelta

config = configparser.ConfigParser()
config.read("config.txt")

app = Flask(__name__)
cors = CORS(app, resources={r"/foo": {"origins": "*"}})
app.config["CORS_HEADERS"] = "Content-Type"
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["MQTT_BROKER_URL"] = config["mqtt_config"]["mqtt_url"]
app.config["MQTT_BROKER_PORT"] = int(config["mqtt_config"]["mqtt_port"])
app.config["MQTT_USERNAME"] = config["mqtt_config"]["mqtt_username"]
app.config["MQTT_PASSWORD"] = config["mqtt_config"]["mqtt_password"]
app.config["MQTT_KEEPALIVE"] = 5
app.config["MQTT_TLS_ENABLED"] = False
app.config["MQTT_LAST_WILL_TOPIC"] = config["mqtt_config"]["mqtt_topic"]
# set permanent session
app.permanent_session_lifetime = timedelta(minutes=5)
socketio = SocketIO(app)

bootstrap = Bootstrap(app)
mqtt = Mqtt(app)

# setting for session
app.secret_key = "secret_key"


ALLOWED_EXTENSIONS = set(["png", "jpg", "jpeg", "gif"])

# create to check require login
def is_login():
    if "username" in session:
        return True
    else:
        return False


# Route for handling the login page logic
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = request.get_json()
        # read username and password from config.txt
        config.read("config.txt")
        guess = {
            "username": config["login_config"]["guest_usr"],
            "password": config["login_config"]["guest_pwd"],
        }
        admin = {
            "username": config["login_config"]["admin_usr"],
            "password": config["login_config"]["admin_pwd"],
        }
        if (
            data["username"] == guess["username"]
            and data["password"] == guess["password"]
        ):
            session["username"] = data["username"]
            session["role"] = "guest"
            session.permanent = True
            return {"message": "Login success", "status": 200}
        elif (
            data["username"] == admin["username"]
            and data["password"] == admin["password"]
        ):
            session["username"] = data["username"]
            session["role"] = "admin"
            session.permanent = True
            return {"message": "Login success", "status": 200}
        else:
            return {"message": "Invalid username or password", "status": 401}

    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))


@app.route("/")
@cross_origin(origin="*", headers=["Content-Type", "Authorization"])
def index():
    # if not login go to login page
    if not is_login():
        return redirect(url_for("login"))
    config.read("config.txt")
    page_config = {
        "title": config["page_settings"]["title"],
        "name": config["page_settings"]["name"],
        "tank_number": int(config["history_settings"]["tank_number"]),
    }
    # get the first image name from static/images
    image_names = os.listdir("static/images/map")
    if len(image_names) > 0:
        first_image_name = image_names[0]
    else:
        first_image_name = None
    return render_template(
        "index.html",
        image_name=first_image_name,
        page_config=page_config,
        role=session["role"],
    )


@app.route("/get_max", methods=["POST"])
def get_max():
    data = request.get_json()
    tankid = data["tankno"]
    # get maxh, maxv based on tankid from quangtriconfig db, tankdata table
    # connect to db
    conn = pyodbc.connect(
        "DRIVER={SQL Server};SERVER="
        + config["sql_config"]["server_name"]
        + ";DATABASE=quangtriconfig;UID="
        + config["sql_config"]["user"]
        + ";PWD="
        + config["sql_config"]["password"]
    )
    cursor = conn.cursor()
    # get maxh, maxv
    cursor.execute("SELECT maxh, maxv FROM tankdata WHERE tankid = " + tankid)
    row = cursor.fetchone()
    maxh = row[0]
    maxv = row[1]
    return {"status": "ok", "data": {"maxh": maxh, "maxv": maxv}}


@app.route("/tank_history", methods=["POST"])
def tank_history():
    config.read("config.txt")
    server_name = config["sql_config"]["server_name"]
    user = config["sql_config"]["user"]
    password = config["sql_config"]["password"]
    database = config["sql_config"]["database"]
    table_tank = config["sql_config"]["table_tank"]
    data = request.get_json()
    from_date = data["from_date"]
    to_date = data["to_date"]
    tankno = data["tankno"]
    # get data from sql server
    # connect to sql server
    conn = pyodbc.connect(
        "Driver={SQL Server};" f"Server={server_name};" f"Database={database};"
    )
    cursor = conn.cursor()
    # get data from sql server
    cursor.execute(
        f"SELECT * FROM {table_tank} WHERE storedate >= '{from_date}' AND storedate <= '{to_date}' AND tankno = '{tankno}' ORDER BY storedate DESC"
    )
    column = [column[0] for column in cursor.description]
    rows = cursor.fetchall()
    tank_data = []
    for row in rows:
        temp = dict(zip(column, row))
        temp["storedate"] = temp["storedate"].strftime("%Y-%m-%d %H:%M:%S")
        tank_data.append(temp)
    return {"status": "ok", "data": tank_data}


@app.route("/history", methods=["GET"])
def history():
    if not is_login():
        return redirect(url_for("login"))
    config.read("config.txt")
    page_config = {
        "title": config["page_settings"]["title"],
        "name": config["page_settings"]["name"],
        "tank_number": int(config["history_settings"]["tank_number"]),
    }
    return render_template(
        "history.html", page_config=page_config, role=session["role"]
    )


@app.route("/product_history", methods=["POST"])
def product_history():
    config.read("config.txt")
    server_name = config["sql_config"]["server_name"]
    user = config["sql_config"]["user"]
    password = config["sql_config"]["password"]
    database = config["sql_config"]["database"]
    table_product = config["sql_config"]["table_product"]
    data = request.get_json()
    from_date = data["from_date"]
    to_date = data["to_date"]
    idproduct = data["idproduct"]
    # get data from sql server
    # connect to sql server
    conn = pyodbc.connect(
        "Driver={SQL Server};" f"Server={server_name};" f"Database={database};"
    )
    cursor = conn.cursor()
    # get data from sql server
    cursor.execute(
        f"SELECT * FROM {table_product} WHERE storedate >= '{from_date}' AND storedate <= '{to_date}' AND idproduct = '{idproduct}' ORDER BY storedate DESC"
    )
    column = [column[0] for column in cursor.description]
    rows = cursor.fetchall()
    product_data = []
    for row in rows:
        temp = dict(zip(column, row))
        temp["storedate"] = temp["storedate"].strftime("%Y-%m-%d %H:%M:%S")
        product_data.append(temp)

    return {"status": "ok", "data": product_data}


# get and post
@app.route("/configurations", methods=["GET", "POST"])
def configurations():
    if not is_login():
        return redirect(url_for("login"))
    if session["role"] != "admin":
        # return not permission page
        return "Not permission", 403
    config.read("config.txt")
    page_config = {
        "title": config["page_settings"]["title"],
        "name": config["page_settings"]["name"],
        "tank_number": int(config["history_settings"]["tank_number"]),
    }
    if request.method == "POST":
        data = request.get_json()
        # update config file
        # update product, maxh, maxv, density based on tankno
        # connect to db
        conn = pyodbc.connect(
            "DRIVER={SQL Server};SERVER="
            + config["sql_config"]["server_name"]
            + ";DATABASE=quangtriconfig;UID="
            + config["sql_config"]["user"]
            + ";PWD="
            + config["sql_config"]["password"]
        )
        cursor = conn.cursor()
        # update product, maxh, maxv, density
        cursor.execute(
            f"UPDATE tankdata SET product = '{data['product']}', maxh = {data['maxh']}, maxv = {data['maxv']}, density = {data['density']} WHERE tankid = {data['tankno']}"
        )
        conn.commit()
        return {"status": "success"}
    else:
        # get data from db
        # connect to db
        conn = pyodbc.connect(
            "DRIVER={SQL Server};SERVER="
            + config["sql_config"]["server_name"]
            + ";DATABASE=quangtriconfig;UID="
            + config["sql_config"]["user"]
            + ";PWD="
            + config["sql_config"]["password"]
        )
        cursor = conn.cursor()
        # get data
        cursor.execute("SELECT * FROM tankdata ORDER BY tankid")
        column = [column[0] for column in cursor.description]
        rows = cursor.fetchall()
        tank_data = []
        for row in rows:
            temp = dict(zip(column, row))
            tank_data.append(temp)

        return render_template(
            "configurations.html", page_config=page_config, tank_data=tank_data
        )


# socketio.emit("mqtt_message", data, namespace="/test")
@socketio.on("mqtt_message")
@cross_origin(origin="*", headers=["Content-Type", "Authorization"])
def handle_mqtt_message(message):
    data = message["tank_data"]
    socketio.emit("mqtt_message", data)


@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    mqtt.subscribe(app.config["MQTT_LAST_WILL_TOPIC"])


# disconnect callback
@mqtt.on_disconnect()
def handle_disconnect():
    print("Disconnected with result code ")


@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    # send message to client
    socketio.emit("mqtt_message", message.payload.decode())


if __name__ == "__main__":
    socketio.run(
        app, host="0.0.0.0", port=4000, use_reloader=False, debug=True
    )
