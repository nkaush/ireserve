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
 
    for user in users:
        response.append({
            "FirstName" : user.FirstName,
            "Email": user.Email
        })
 
    return make_response({
        'status' : 'success',
        'message': response
    }, 200)
 
 
if __name__ == "__main__":
    # serving the app directly
    app.run()

