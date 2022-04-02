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
 
# configuration
app.config["SECRET_KEY"] = "yoursecretkey"
app.config["SQLALCHEMY_DATABASE_URI"]= f"mysql+mysqldb://{CLOUD_SQL_USERNAME}:{CLOUD_SQL_PASSWORD}@{CLOUD_SQL_PUBLIC_IP_ADDRESS}/{CLOUD_SQL_DATABASE_NAME}?unix_socket=/cloudsql/{CLOUD_SQL_CONNECTION_NAME}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]= True
 
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

#Initial page
@app.route('/')
def home(): 
    return render_template(
        "main_page.html"
    )

@app.route('/favicon.ico')
def send_resume():
    return send_from_directory('static', 'images/favicon.png')

# fetches all the users
@app.route('/users')
def view():
    # fetches all the users
    users = User.query.all()
    return render_template("users.html", queried_users=users)

@app.route('/users/priority')
def get_priority_users():
    """Fetches all priority users."""

    users = db.engine.execute(
        """
        (SELECT DISTINCT u.FirstName, u.LastName 
        FROM `user` u NATURAL JOIN `groupassignment` ga NATURAL JOIN `group` grp grp
        WHERE grp.GroupName LIKE 'CS4__ %'
        )
        UNION
        (SELECT u.FirstName, u.LastName 
        FROM `user` u
        WHERE u.UserID IN (SELECT r.UserID 
                    FROM reservation r 
                    GROUP BY r.UserID 
                    HAVING COUNT(r.UserID) >= 7)
        );
        """
    )

    return render_template("users_priority.html", queried_users=users)

# All reservations   
@app.route('/reservations')
def get_all_buildings():
    
    reservations = db.engine.execute("SELECT * FROM reservation;")
    return render_template("reservation.html", queried_reservations=reservations)

# Reservations for a user  
@app.route('/reservations/user', methods =['GET'])
def reservations_for_user():
    user_id= request.args.get("UserID")

    print(user_id)
 
    # checking for reservation
    reservations = db.engine.execute(text("SELECT * FROM reservations r WHERE r.UserID LIKE :query;"), query="%{}%".format(user_id))
    
    return render_template("user_reservations.html", queried_reservations=reservations)

@app.route('reservations/popular_may21')
def get_popular_may21_reservations():
    reservations = db.engine.execute(
        """
        SELECT tmp.BuildingName, AVG(tmp.Popularity) AS AVG_POPULARITY
        FROM (SELECT * FROM room r NATURAL JOIN building b
        WHERE r.RoomID IN (SELECT res.RoomID FROM reservation res WHERE res.StartTime LIKE "2021-05%")) AS tmp
        GROUP BY tmp.BuildingName
        HAVING AVG(tmp.Popularity) > 50
        ORDER BY AVG_POPULARITY DESC;
        """
    )
    return render_template("reservations_may_popular.html", queried_reservations=reservations)

#add user    
@app.route('/Users/add', methods =['POST'])
def add_user():
    # getting name and email
    first_name = request.json.get('FirstName')
    email = request.json.get('Email')

    print(first_name)
    print(email)
 
    # checking if user already exists
    user = User.query.filter_by(Email = email).first()
 
    if not user:
        try:
            # creating Users object
            user = User(
                UserId = 1001,
                FirstName = first_name,
                LastName = "",
                Email = email, 
                HashedPassword = ""
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
 
# Delete Reservation
@app.route('/reservation/delete', methods =['GET'])
def delete_reservation():
    searched_reservation = request.args.get("ReservationId")
    rooms = db.engine.execute("DELETE FROM reservation WHERE ReservationID = {};".format(searched_reservation))
    
    reservations = db.engine.execute("SELECT * FROM reservation;")

    return render_template("reservation_delete.html", queried_reservations=reservations)


#add reservation    
@app.route('/reservation/add', methods =['POST'])
def add_reservtaion():
    # getting components of reservation

    group_id = request.json.get('GroupID')
    room_id = request.json.get('RoomID')
    start_time = request.json.get('StartTime')
    end_time = request.json.get('end_time')

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
 
if __name__ == "__main__":
    # serving the app directly
    app.run()

