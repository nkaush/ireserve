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
@app.route('/view')
def view():
    # fetches all the users
    users = User.query.all()
    # result = db.engine.execute("<sql here>")
    
    return render_template("users.html", queried_users=users)

#add user    
@app.route('/add_user', methods =['POST'])
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
@app.route('/search_room', methods =['GET'])
def search_room():
    searched_building = request.args.get("building")

    print(searched_building)
 
    # checking for building
    rooms = db.engine.execute(text("SELECT * FROM building b NATURAL JOIN room WHERE b.BuildingName LIKE :query;"), query="%{}%".format(searched_building))
    text("select * from table where "
         "string like :string limit 1"), 
    string="_stringStart%"
    # result = db.engine.execute("<sql here>")

    return render_template("rooms.html", queried_rooms=rooms)
 
# Delete Reservation
@app.route('/Reservation/Delete', methods =['GET'])
def delete_reservation():
    searched_reservation = request.args.get("ReservationId")
    rooms = db.engine.execute("DELETE FROM reservation WHERE ReservationID = {};".format(searched_reservation))
    
    reservations = db.engine.execute("SELECT * FROM reservation;")

    return render_template("reservation.html", queried_reservations=reservations)   
 
if __name__ == "__main__":
    # serving the app directly
    app.run()

