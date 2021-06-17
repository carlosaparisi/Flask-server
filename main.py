from flask import Flask
from flask import render_template, request, redirect, jsonify, make_response, url_for, send_file, send_from_directory, session, flash
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import shutil

app = Flask(__name__)
app.secret_key = 'hello'
app.config['SECRET_KEY'] = '68e39f3c575c7fb732c5f8dd7b7ad24c'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///devices_database4.sqlite3'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config["IMAGE_UPLOADS"] = "./static/img"
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG", "GIF"]

app.config["CLIENT_IMAGES"] = './static/zip'

db = SQLAlchemy(app)

users = {
    "admin": {
        "username": "admin",
        "password": "admin",
    }
}


class devices(db.Model):
    _id = db.Column('id',db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    camera = db.Column(db.String(100))
    ip = db.Column(db.String(100))
    connection = db.Column(db.String(100))
    rem_space = db.Column(db.String(100))
    battery_left = db.Column(db.String(100))
    clients_connected = db.Column(db.String(100))
    pictures_left = db.Column(db.String(100))
    camera_SSID = db.Column(db.String(100))
    serial_number = db.Column(db.String(100))


    def __init__(self,name,camera,ip,connection,rem_space,battery_left,clients_connected,pictures_left,camera_SSID,serial_number):
        self.name = name
        self.camera = camera
        self.ip = ip
        self.connection = connection
        self.rem_space = rem_space
        self.battery_left = battery_left
        self.clients_connected = clients_connected
        self.pictures_left = pictures_left
        self.camera_SSID = camera_SSID
        self.serial_number = serial_number


    def __repr__(self):
        return '<devices %r>' % self.name

    def get_by_name(name):
        return devices.query.filter_by(name=name).first()

@app.route("/signin", methods=["GET", "POST"])
def sign_in():
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        print(username,password)
        print(users)

        if not username in users:
            print("Username not found")
            flash("Username not found!", "danger")
            return redirect(request.url)
        else:
            user = users[username]

        if not password == user["password"]:
            print("Incorrect password")
            flash("Incorrect password", "warning")
            return redirect(request.url)
        else:
            session["USERNAME"] = user["username"]
            print("session username set")
            flash("Welcome!", "success")
            return redirect(url_for('about'))

    return render_template("public/signin.html")

@app.route("/signout")
def sign_out():

    session.pop("USERNAME", None)

    return redirect(url_for("sign_in"))


def allowed_image(filename):

    # We only want files with a . in the filename
    if not "." in filename:
        return False

    # Split the extension from the filename
    ext = filename.rsplit(".", 1)[1]

    # Check if the extension is in ALLOWED_IMAGE_EXTENSIONS
    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False

@app.route("/uploadimage", methods=["GET", "POST"])
def upload_image():

    if request.method == "POST":

        if request.files:

            image = request.files["image"]

            if image.filename == "":
                print("No filename")
                return redirect(request.url)

            if allowed_image(image.filename):
                filename = secure_filename(image.filename)
                image.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
                print("Image saved")
                return redirect(request.url)

            else:
                print("That file extension is not allowed")
                return redirect(request.url)

    return render_template("public/uploadimage.html")

dev = {
    "admin": {
        "device": "Raspberry pi 4",
        "camera": "Gopro hero 4",
        "connection": "Last connection",
        "IP": "192.168.1.1",
    }
}


@app.route('/') #Deposito de imagenes
def about():
    if session.get("USERNAME", None) is not None:
        username = session.get("USERNAME")
        namefiles = os.listdir('./static/img')
        return render_template("admin/admin.html", username=username, namefiles=namefiles, values=devices.query.all())
    else:
        print("No username found in session")
        return redirect(url_for("sign_in"))


@app.route("/", methods=["POST"])
def submit_message():
    filename = 'Images'
    shutil.make_archive(filename, 'zip', './static/img')
    try:
        shutil.move(f'./static/img/{filename}.zip','./static/zip')
    except:
        os.replace(f'{filename}.zip', f'./static/zip/{filename}.zip')

    return send_from_directory(app.config["CLIENT_IMAGES"], filename=f'{filename}.zip', as_attachment=True)


@app.route("/json", methods=["POST"])
def json_example():
    # Validate the request body contains JSON
    if request.is_json:

        # Parse the JSON into a Python dictionary
        req = request.get_json()

        response_body = {
            "message": "JSON received!",
            "sender": req.get("name")
        }
        try:
            name = req['name']
            camera = req['message']
            remspace = req['rem_space']
            batteryleft = req['battery_left']
            clientsconnected = req['clients_connected']
            picturesleft = req['pictures_left']
            cameraSSID = req['camera_SSID']
            serialnumber = req['serial_number']


            ip = str(request.remote_addr)

            now = datetime.now()
            date_time = now.strftime("%d/%m/%Y, %H:%M")

            usr = devices(name, camera, ip, date_time,remspace,batteryleft,clientsconnected,picturesleft,cameraSSID,serialnumber)
            user = devices.get_by_name(name)

            print(name)
            print(camera)
            print(ip)

            if user is not None:  # si existe el usuario
                user.ip = ip
                user.camera = camera
                user.connection = date_time
                user.rem_space = remspace
                user.battery_left = batteryleft
                user.clients_connected = clientsconnected
                user.pictures_left = picturesleft
                user.camera_SSID = cameraSSID
                user.serial_number = serialnumber
                db.session.commit()
            else:
                db.session.add(usr)
                db.session.commit()
        except:
            print('error')

        res = make_response(jsonify(response_body), 200)
        # Return a string along with an HTTP status code
        return res
    else:
        return make_response(jsonify({"message": "Request body must be JSON"}), 400)


#host='0.0.0.0'
if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)



