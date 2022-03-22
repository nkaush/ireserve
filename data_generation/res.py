import random
import time
    
def str_time_prop(start, end, time_format, prop):
    stime = time.mktime(time.strptime(start, time_format))
    etime = time.mktime(time.strptime(end, time_format))

    ptime = stime + prop * (etime - stime)

    return time.strftime(time_format, time.localtime(ptime))

def random_date(start, end, prop):
    return str_time_prop(start, end, '%Y-%m-%d', prop)

def random_time(start, end, prop):
    return str_time_prop(start, end, '%H:00:00', prop)
    
def random_datetime(start_d, end_d, start_t, end_t, prop):
    return random_date(start_d, end_d, prop) + ' ' + random_time(start_t, end_t, prop)

def next_hour(t):
    hour = int(t[11:13]) + 1
    return t[:11] + str(hour) + t[13:]

class Reservation:
    i = 1

    def __init__(self):
        self.res_id = i
        self.start = random_datetime("2021-01-01", "2022-05-08", "08:00:00", "22:00:00", random.random())
        self.end = next_hour(self.start)
        self.room_id = random.randint(0, 1021)
        self.assignment_id = random.randint(0, 498)
        self.user_id = random.randint(1, 1000)

reservations = set()
fmt = "INSERT INTO reservation (ReservationID, RoomID, UserID, GroupID, StartTime, EndTime) VALUES ({}, {}, {}, {}, '{}', '{}');"

def make_res():
    res = Reservation()
    while res in reservations:
        res = Reservation()

    Reservation.i += 1
    return res

for i in range(3000):
    res = make_res()
    print(fmt.format(res.res_id, res.room_id, res.user_id, res.assignment_id, res.start, res.end))