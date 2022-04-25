from flask import Flask, request, make_response, render_template, send_from_directory, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import os

from components.utils import is_logged_in, get_user
import components.reservation as comp_res
import components.user_logic as comp_ul

app = Flask(__name__)

# Google Cloud SQL (change this accordingly)
CLOUD_SQL_DATABASE_NAME = os.environ.get("CLOUD_SQL_DATABASE_NAME")
CLOUD_SQL_USERNAME = os.environ.get("CLOUD_SQL_USERNAME")
CLOUD_SQL_PASSWORD = os.environ.get("CLOUD_SQL_PASSWORD")
CLOUD_SQL_PUBLIC_IP_ADDRESS = os.environ.get("CLOUD_SQL_PUBLIC_IP_ADDRESS")
CLOUD_SQL_CONNECTION_NAME = os.environ.get("CLOUD_SQL_CONNECTION_NAME")

CLOUD_PORT = os.environ.get("PORT")
if CLOUD_PORT is None:
    CLOUD_PORT = os.environ.get("CLOUD_PORT")

# configuration
app.config["SECRET_KEY"] = "yoursecretkey"
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql://{CLOUD_SQL_USERNAME}:{CLOUD_SQL_PASSWORD}@{CLOUD_SQL_PUBLIC_IP_ADDRESS}/{CLOUD_SQL_DATABASE_NAME}?unix_socket=/cloudsql/{CLOUD_SQL_CONNECTION_NAME}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

print(app.config["SQLALCHEMY_DATABASE_URI"])

db = SQLAlchemy(app)

# Homepage
@app.route('/')
@app.route('/index')
def home(): 
    return render_template("index.html", logged_in=is_logged_in(request))

# Serve static files
@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

# Serve favicon
@app.route('/favicon.ico')
def send_favicon():
    return send_from_directory('static', 'images/favicon.png')

# Logout redirect
@app.route('/logout', methods=['GET'])
def logout():
    return comp_ul.logout()

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    return comp_ul.login(request, db)

# Register a user
@app.route('/register', methods=['POST', 'GET'])
def register():
    return comp_ul.register(request, db)

# Search for user   
@app.route('/users', methods =['GET'])
def search_users():
    return comp_ul.search_users(request, db)

# Update a user's name
@app.route('/users/update', methods=['GET', 'POST'])
def update_user():
    return comp_ul.update_user(request, db)

# View all reservations   
@app.route('/reservations')
def get_all_reservations():
    reservations = db.engine.execute("SELECT * FROM reservation NATURAL JOIN user NATURAL JOIN room NATURAL JOIN building NATURAL JOIN `group`;")
    return render_template("reservation.html", queried_reservations=reservations, logged_in=is_logged_in(request), no_delete=True)

# View all reservations made by a particular user  
@app.route('/reservations/user', methods=['GET'])
def reservations_for_user():
    user_cookie = get_user(request)
    user_id = None

    if user_cookie is not None:
        user_id = user_cookie['UserID']

    print(user_cookie)

    # checking for reservation
    reservations = db.engine.execute(text("SELECT * FROM (SELECT * FROM reservation r WHERE r.UserID = :query) AS tmp1 NATURAL JOIN user NATURAL JOIN room NATURAL JOIN building NATURAL JOIN `group`;"), query="{}".format(user_id))
    
    return render_template("reservation.html", queried_reservations=reservations, logged_in=is_logged_in(request))

@app.route('/reservations/current_popularity')
def get_popular_may21_reservations():
    return comp_res.get_popular_may21_reservations(request, db)

# Delete Reservation
@app.route('/reservation/<int:reservation_id>', methods=['DELETE'])
def delete_reservation(reservation_id):
    return comp_res.delete_reservation(db, reservation_id)

#add reservation    
@app.route('/reservation/add', methods=['POST'])
def add_reservation():
    return comp_res.add_reservation(request, db)

# Make a reservation  
@app.route('/reserve', methods=['GET'])
def make_reservation():
    user_cookie = get_user(request)
    user_id = -1

    if user_cookie is not None:
        user_id = user_cookie['UserID']

    rooms = db.engine.execute("SELECT * FROM building b NATURAL JOIN room;")
    groups = db.engine.execute(f"SELECT GroupID, GroupName FROM `group` g NATURAL JOIN `groupassignment` ga WHERE ga.UserID = {user_id};")
    return render_template("reserve.html", logged_in=is_logged_in(request), queried_rooms=rooms, user_groups=groups)

# Make a reservation  
@app.route('/delete_reservation', methods=['GET'])
def delete_reservation_page():
    return render_template("delete_reservation.html", logged_in=is_logged_in(request))

#Search for room   
@app.route('/rooms', methods=['GET'])
def search_room():
    searched_building = request.args.get("building")

    rooms = None

    if searched_building is None: 
        rooms = db.engine.execute("SELECT * FROM building b NATURAL JOIN room;")
    else: 
        print(searched_building)
        rooms = db.engine.execute(text("SELECT * FROM building b NATURAL JOIN room WHERE b.BuildingName LIKE :query;"), query="%{}%".format(searched_building))

    return render_template("rooms.html", route="rooms", queried_rooms=rooms, logged_in=is_logged_in(request))
 
def create_app():
   return app
   
if __name__ == "__main__":
    # serving the app directly
    app.run(host='0.0.0.0')
    # from waitress import serve
    # serve(app, host="0.0.0.0", port=CLOUD_PORT)
