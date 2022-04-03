# imports
import os
from flask import Flask, request, make_response, render_template, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)

# Google Cloud SQL (change this accordingly)

CLOUD_SQL_DATABASE_NAME = os.environ.get("CLOUD_SQL_DATABASE_NAME")
CLOUD_SQL_USERNAME = os.environ.get("CLOUD_SQL_USERNAME")
CLOUD_SQL_PASSWORD=os.environ.get("CLOUD_SQL_PASSWORD")
CLOUD_SQL_PUBLIC_IP_ADDRESS = os.environ.get("CLOUD_SQL_PUBLIC_IP_ADDRESS")
CLOUD_SQL_CONNECTION_NAME = os.environ.get("CLOUD_SQL_CONNECTION_NAME")

CLOUD_PORT = os.environ.get("PORT")
if CLOUD_PORT is None:
    CLOUD_PORT = os.environ.get("CLOUD_PORT")
 
# configuration
app.config["SECRET_KEY"] = "yoursecretkey"
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+mysqldb://{CLOUD_SQL_USERNAME}:{CLOUD_SQL_PASSWORD}@{CLOUD_SQL_PUBLIC_IP_ADDRESS}/{CLOUD_SQL_DATABASE_NAME}?unix_socket=/cloudsql/{CLOUD_SQL_CONNECTION_NAME}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
 
db = SQLAlchemy(app)

class User(db.Model):
    UserId = db.Column(db.Integer, primary_key = True, nullable = False)
    FirstName = db.Column(db.String(255), nullable = False)
    LastName = db.Column(db.String(255), nullable = False)
    Email = db.Column(db.String(255), nullable = False)
    HashedPassword = db.Column(db.String(255), nullable = False)

class Building(db.Model):
    BuildingID = db.Column(db.Integer, primary_key = True, nullable = False)
    Address = db.Column(db.String(255), nullable = False)
    BuildingName = db.Column(db.String(255), nullable = False)
    Region = db.Column(db.String(255), nullable = False)

class Reservation(db.Model):
    ReservationID =  db.Column(db.Integer, primary_key = True, nullable = False)
    RoomID =  db.Column(db.Integer, nullable = False)
    UserID = db.Column(db.Integer, nullable = False)
    GroupID = db.Column(db.Integer, nullable = False)
    StartTime = db.Column(db.String(100), nullable = False)
    EndTime = db.Column(db.String(100), nullable = False)

@app.route('/')
def home(): 
    return render_template("index.html")

@app.route('/login')
def login(): 
    return render_template("login.html")

@app.route('/register')
def register(): 
    return render_template("register.html")

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

@app.route('/favicon.ico')
def send_favicon():
    return send_from_directory('static', 'images/favicon.png')

#add user    
@app.route('/users', methods=['POST'])
def add_user():
    # getting name and email
    first_name = request.json.get('FirstName')
    last_name = request.json.get('LastName')
    email = request.json.get('Email')
    password = request.json.get('HashedPassword')

    print(first_name)
    print(email)
 
    # checking if user already exists
    next_id = db.engine.execute("SELECT MAX(UserID) FROM user;").first()[0] + 1
    user = User.query.filter_by(Email = email).first()
 
    if not user:
        try:
            # creating Users object
            user = User(
                UserId = next_id,
                FirstName = first_name,
                LastName = last_name,
                Email = email, 
                HashedPassword = password
            )
            # adding the fields to users table
            db.session.add(user)
            db.session.commit()
            # response
            responseObject = {
                'status' : 'success',
                'message': 'Successfully registered.'
            }
 
            return make_response(responseObject, 200)
        except Exception as e:
            print(e)
            responseObject = {
                'status' : 'fail',
                'message': 'Some error occured !!'
            }
 
            return make_response(responseObject, 400)
         
    else:
        # if user already exists then send status as fail
        responseObject = {
            'status' : 'fail',
            'message': 'User already exists !!'
        }
 
        return make_response(responseObject, 403)

@app.route('/users/priority')
def get_priority_users():
    """Fetches all priority users."""

    users = db.engine.execute(text(
        """
        (SELECT DISTINCT u.FirstName, u.LastName, u.Email
        FROM `user` u NATURAL JOIN `groupassignment` ga NATURAL JOIN `group` grp
        WHERE grp.GroupName LIKE :query
        )
        UNION
        (SELECT u.FirstName, u.LastName, u.Email
        FROM `user` u
        WHERE u.UserID IN (SELECT r.UserID 
                    FROM reservation r 
                    GROUP BY r.UserID 
                    HAVING COUNT(r.UserID) >= 7)
        );
        """), query='CS4__ %'
    )

    return render_template("users.html", queried_users=users)

# All reservations   
@app.route('/reservations')
def get_all_buildings():
    
    reservations = db.engine.execute("SELECT * FROM reservation NATURAL JOIN user NATURAL JOIN room NATURAL JOIN building NATURAL JOIN `group`;")
    return render_template("reservation.html", queried_reservations=reservations)

# Reservations for a user  
@app.route('/reservations/user', methods=['GET'])
def reservations_for_user():
    user_id= request.args.get("userid")

    print(user_id)

    # checking for reservation
    reservations = db.engine.execute(text("SELECT * FROM (SELECT * FROM reservation r WHERE r.UserID = :query) AS tmp1 NATURAL JOIN user NATURAL JOIN room NATURAL JOIN building NATURAL JOIN `group`;"), query="{}".format(user_id))
    
    return render_template("reservation.html", queried_reservations=reservations)

@app.route('/reservations/popular_may21')
def get_popular_may21_reservations():
    reservations = db.engine.execute(text(
        """
        SELECT tmp.BuildingName, AVG(tmp.Popularity) AS AVG_POPULARITY
        FROM (SELECT * FROM room r NATURAL JOIN building b
        WHERE r.RoomID IN (SELECT res.RoomID FROM reservation res WHERE res.StartTime LIKE :query)) AS tmp
        GROUP BY tmp.BuildingName
        HAVING AVG(tmp.Popularity) > 50
        ORDER BY AVG_POPULARITY DESC;
        """), query="2021-05%"
    )

    print(dir(reservations))
    print(reservations.rowcount)

    return render_template("reservations_may_popular.html", queried_reservations=reservations)

#Search for room   
@app.route('/rooms', methods =['GET'])
def search_room():
    searched_building = request.args.get("building")

    rooms = None

    if searched_building is None: 
        rooms = db.engine.execute("SELECT * FROM building b NATURAL JOIN room;")
    else: 
        print(searched_building)
        rooms = db.engine.execute(text("SELECT * FROM building b NATURAL JOIN room WHERE b.BuildingName LIKE :query;"), query="%{}%".format(searched_building))

    return render_template("rooms.html", route="rooms", queried_rooms=rooms)

#Search for user   
@app.route('/users', methods =['GET'])
def search_users():
    searched_user = request.args.get("user")
    is_priority = request.args.get("priority")

    users = None

    if is_priority == "true":
        if searched_user is None:
            users = db.engine.execute(text(
                """
                (SELECT DISTINCT u.FirstName, u.LastName, u.Email FROM `user` u NATURAL JOIN `groupassignment` ga NATURAL JOIN `group` grp
                    WHERE grp.GroupName LIKE :query)
                UNION (SELECT u.FirstName, u.LastName, u.Email FROM `user` u
                    WHERE u.UserID IN (SELECT r.UserID FROM reservation r GROUP BY r.UserID HAVING COUNT(r.UserID) >= 7));
                """), query='CS4__ %'
            )
        else:
            users = db.engine.execute(text(
                """
                (SELECT DISTINCT u.FirstName, u.LastName, u.Email FROM `user` u NATURAL JOIN `groupassignment` ga NATURAL JOIN `group` grp
                    WHERE grp.GroupName LIKE :query AND (u.FirstName LIKE :filter OR u.LastName LIKE :filter))
                UNION (SELECT u.FirstName, u.LastName, u.Email FROM `user` u
                    WHERE u.UserID IN (SELECT r.UserID FROM reservation r GROUP BY r.UserID HAVING COUNT(r.UserID) >= 7) 
                    AND (u.FirstName LIKE :filter OR u.LastName LIKE :filter) 
                );
                """), query='CS4__ %', filter="%{}%".format(searched_user)
            )
    elif searched_user is None: 
        users = db.engine.execute("SELECT * FROM user u;")
    else: 
        users = db.engine.execute(text("SELECT * FROM user u WHERE u.FirstName LIKE :query;"), query="%{}%".format(searched_user))

    return render_template("users.html", route="users", queried_users=users, is_priority=is_priority)    
 
# Delete Reservation
@app.route('/reservation/delete', methods=['DELETE'])
def delete_reservation():
    searched_reservation = request.json.get("ReservationID")
    rooms = db.engine.execute("DELETE FROM reservation WHERE ReservationID = {};".format(searched_reservation))
    
    reservations = db.engine.execute("SELECT * FROM reservation;")
    responseObject = {
        'status' : 'success',
        'message': 'Successfully deleted reservation with id={}.'.format(searched_reservation)
    }

    return make_response(responseObject, 200)

#add reservation    
@app.route('/reservation/add', methods=['POST'])
def add_reservtaion():
    # getting components of reservation

    group_id = request.json.get('GroupID')
    room_id = request.json.get('RoomID')
    start_time = request.json.get('StartTime')
    end_time = request.json.get('EndTime')

    print(group_id)
    print(room_id)
    print(start_time)
    print(end_time)
 
    # checking if reservtaion already exists
    reservation = Reservation.query.filter_by(GroupID = group_id, RoomID = room_id).first()
 
    if not reservation:
        try:
            max_id = db.engine.execute("Select MAX(ReservationID) from reservation").first()[0]
            print(max_id)
            reservation = Reservation(
                ReservationID = (max_id + 1),
                RoomID = room_id,
                UserID = 10,
                GroupID = group_id,
                StartTime = start_time,
                EndTime = end_time
            )
            # adding the fields to users table
            db.session.add(reservation)
            db.session.commit()
            # response
            responseObject = {
                'status' : 'success',
                'message': 'Successfully registered.'
            }
 
            return make_response(responseObject, 200)
        except Exception as e:
            print(e)
            responseObject = {
                'status' : 'fail',
                'message': 'Some error occured !!'
            }
 
            return make_response(responseObject, 400)
         
    else:
        # if user already exists then send status as fail
        responseObject = {
            'status' : 'fail',
            'message': 'User already exists !!'
        }
 
        return make_response(responseObject, 403)   
 
def create_app():
   return app
   
if __name__ == "__main__":
    # serving the app directly
    app.run(host='0.0.0.0')
    # from waitress import serve
    # serve(app, host="0.0.0.0", port=CLOUD_PORT)
