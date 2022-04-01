# imports
import os
import pymysql
from flask import Flask, request, make_response, render_template
from flask_sqlalchemy import SQLAlchemy
from db import *

app = Flask(__name__)


# Google Cloud SQL (change this accordingly)
PASSWORD ="your database password"
PUBLIC_IP_ADDRESS ="public ip of database"
DBNAME ="database name"
PROJECT_ID ="gcp project id"
INSTANCE_NAME ="instance name"
 
# configuration
app.config["SECRET_KEY"] = "yoursecretkey"
app.config["SQLALCHEMY_DATABASE_URI"]= f"mysql + mysqldb://root:{PASSWORD}@{PUBLIC_IP_ADDRESS}/{DBNAME}?unix_socket =/cloudsql/{PROJECT_ID}:{INSTANCE_NAME}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]= True
 
db = SQLAlchemy(app)

class Users(db.Model):
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
    users = Users.query.all()
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

