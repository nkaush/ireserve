#db.py
import os
import pymysql
from flask import jsonify

db_user = os.environ.get('CLOUD_SQL_USERNAME')
db_password = os.environ.get('CLOUD_SQL_PASSWORD')
db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')


def open_connection():
    unix_socket = '/cloudsql/{}'.format(db_connection_name)
    try:
        if os.environ.get('GAE_ENV') == 'standard':
            conn = pymysql.connect(user=db_user, password=db_password,
                                unix_socket=unix_socket, db=db_name,
                                cursorclass=pymysql.cursors.DictCursor
                                )
    except pymysql.MySQLError as e:
        print(e)

    return conn


# Get all buildings
def get_buildings():
    conn = open_connection()
    with conn.cursor() as cursor:
        result = cursor.execute('Select * from b Buildings LIMIT 15;')
    conn.close()
    return result

# Get all groups
def get_groups():
    conn = open_connection()
    with conn.cursor() as cursor:
        result = cursor.execute('Select * from g Groups LIMIT 15;')
    conn.close()
    return result

# Get all reservations
def get_reservations():
    conn = open_connection()
    with conn.cursor() as cursor:
        result = cursor.execute('Select * from r Reservations LIMIT 15;')
    conn.close()
    return result

# Get all rooms 
def get_rooms():
    conn = open_connection()
    with conn.cursor() as cursor:
        result = cursor.execute('Select * from r Rooms LIMIT 15;')
    conn.close()
    return result

# Get all users
def get_users():
    conn = open_connection()
    with conn.cursor() as cursor:
        result = cursor.execute('Select * from u Users LIMIT 15;')
    conn.close()
    return result


