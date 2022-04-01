# imports
import os
import pymysql
from flask import Flask, request, make_response, render_template
from flask_sqlalchemy import SQLAlchemy
from db import *

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

#Initial page
@app.route('/')
def home(): 
    return render_template(
        "main_page.html"
    )

# fetches all the users
@app.route('/view')
def view():
    # fetches all the users
    users = User.query.all()
    # result = db.engine.execute("<sql here>")

    # response list consisting user details
    response = list()
 
    for user in users[:15]:
        response.append({
            "FirstName" : user.FirstName,
            "Email": user.Email
        })
 
    return make_response({
        'status' : 'success',
        'message': response
    }, 200)
 
@app.route('/add', methods =['POST'])
def add():
    # getting name and email
    first_name = request.form.get('FirstName')
    email = request.form.get('Email')
 
    # checking if user already exists
    user = User.query.filter_by(email = email).first()
 
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
        except:
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

