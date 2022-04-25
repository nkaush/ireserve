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
    def __init__(self):
        self.start = random_datetime("2021-01-01", "2022-05-08", "08:00:00", "22:00:00", random.random())
        self.end = next_hour(self.start)
        self.room_id = random.randint(0, 1021)

    def __eq__(self, other):
        return self.__hash__() == hash(other)

    def __hash__(self):
        return hash((self.start, self.end, self.room_id))

        
reservations = set()

def make_res():
    res = Reservation()
    while res in reservations:
        res = Reservation()
        reservations.add(res)

    return res

creation = """DROP TABLE IF EXISTS `reservation`;

CREATE TABLE `reservation` (
  `ReservationID` INT PRIMARY KEY,
  `RoomID` INT,
  `UserID` INT,
  `GroupID` INT,
  `StartTime` VARCHAR(100) NOT NULL,
  `EndTime` VARCHAR(100) NOT NULL,
  FOREIGN KEY (`RoomID`) REFERENCES `room` (`RoomID`) ON DELETE CASCADE,
  FOREIGN KEY (`UserID`) REFERENCES `user` (`UserID`) ON DELETE CASCADE,
  FOREIGN KEY (`GroupID`) REFERENCES `group` (`GroupID`) ON DELETE CASCADE
);
"""

def run():
    print(creation)
    print("INSERT INTO reservation (ReservationID, RoomID, UserID, GroupID, StartTime, EndTime) VALUES")
    fmt = "\t({}, {}, {}, {}, '{}', '{}'),"
    fmt2 = "\t({}, {}, {}, {}, '{}', '{}');"

    iters = 30000
    for i in range(iters):
        res = make_res()
        assignment_id = random.randint(0, 498)
        user_id = random.randint(1, 1019)

        if i < (iters - 1):
            print(fmt.format(i, res.room_id, user_id, assignment_id, res.start, res.end))
        else:
            print(fmt2.format(i, res.room_id, user_id, assignment_id, res.start, res.end))

run()