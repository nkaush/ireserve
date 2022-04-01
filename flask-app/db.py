#db.py
import os
import pymysql
from flask import jsonify
from dotenv import load_dotenv

load_dotenv()

db_user = os.environ.get('CLOUD_SQL_USERNAME')
db_password = os.environ.get('CLOUD_SQL_PASSWORD')
db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')

def open_connection():
    unix_socket = '/cloudsql/{}'.format(db_connection_name)
    try:
        if os.environ.get('GAE_ENV') == 'standard':
            conn = pymysql.connect(user=db_user, 
                                   password=db_password,
                                   unix_socket=unix_socket, 
                                   db=db_name,
                                   cursorclass=pymysql.cursors.DictCursor
                                  )
            return conn
    except Exception as e:
        print(e)

    



