from flask import render_template, make_response
from .utils import is_logged_in, get_user
from sqlalchemy import text

def get_popular_may21_reservations(request, db):
    reservations = db.engine.execute(text(
        """
        SELECT tmp.BuildingName, AVG(tmp.Popularity) AS AVG_POPULARITY
        FROM (SELECT * FROM room r NATURAL JOIN building b
        WHERE r.RoomID IN (SELECT res.RoomID FROM reservation res WHERE res.StartTime LIKE :query)) AS tmp
        GROUP BY tmp.BuildingName
        HAVING AVG(tmp.Popularity) > 0
        ORDER BY AVG_POPULARITY DESC;
        """), query="2021-05%"
    )

    print(dir(reservations))
    print(reservations.rowcount)

    return render_template("reservations_may_popular.html", queried_reservations=reservations, logged_in=is_logged_in(request))

def delete_reservation(db, reservation_id):
    db.engine.execute("DELETE FROM reservation WHERE ReservationID = {};".format(reservation_id))
    
    responseObject = {
        'status' : 'success',
        'message': 'Successfully deleted reservation with ID = {}.'.format(reservation_id)
    }

    return make_response(responseObject, 200)

def add_reservation(request, db):
    user = get_user(request)
    group_id = request.json.get('GroupID')
    room_id = request.json.get('RoomID')
    start_time = request.json.get('StartTime')
    end_time = request.json.get('EndTime')
 
    # checking if reservtaion already exists
    reservation = db.engine.execute(f"SELECT * FROM reservation WHERE RoomID = {room_id} AND StartTime = '{start_time}';").first()

    if not reservation:
        try:
            max_id = db.engine.execute("SELECT MAX(ReservationID) FROM reservation;").first()[0]
            print(max_id)
            db.engine.execute(f"INSERT INTO reservation(ReservationID, RoomID, UserID, GroupID, StartTime, EndTime) VALUES ({(max_id + 1)}, {room_id}, {user['UserID']}, {group_id}, '{start_time}', '{end_time}');")

            # response
            room = db.engine.execute(f"SELECT RoomNumber, BuildingName FROM room NATURAL JOIN building WHERE RoomID = {room_id}").first()
            responseObject = {
                'status' : 'success',
                'message': 'Successfully reserved room {} in {}.'.format(room.RoomNumber, room.BuildingName)
            }
 
            return make_response(responseObject, 200)
        except Exception as e:
            print(e)
            responseObject = {
                'status' : 'fail',
                'message': 'Some error occured.'
            }
 
            return make_response(responseObject, 400)
         
    else:
        # if user already exists then send status as fail
        responseObject = {
            'status' : 'fail',
            'message': 'Reservation already exists.'
        }
 
        return make_response(responseObject, 403)
