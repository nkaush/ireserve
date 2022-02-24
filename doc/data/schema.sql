DROP TABLE User IF EXISTS;

CREATE TABLE User(
  UserID         INT PRIMARY KEY, 
  FirstName      VARCHAR(255) NOT NULL,
  LastName       VARCHAR(255) NOT NULL, 
  Email          VARCHAR(255) NOT NULL, 
  HashedPassword VARCHAR(255) NOT NULL
);

DROP TABLE Room IF EXISTS;

CREATE TABLE Room(
  RoomID       INT PRIMARY KEY,
  BuildingID   INT,
  FloorNumber  INT,
  RoomNumber   INT,
  RoomCapacity INT,
  RoomType:    VARCHAR(50) NOT NULL,
  Popularity   REAL,
  FOREIGN KEY (BuildingID) REFERENCES Building(BuildingID) ON DELETE CASCADE
);

DROP TABLE Building IF EXISTS;

CREATE TABLE Building(
  Address      VARCHAR(255) PRIMARY KEY NOT NULL,
  BuildingName VARCHAR(255) NOT NULL,
  Region       VARCHAR(255) NOT NULL,
);

DROP TABLE Reservation IF EXISTS;

CREATE TABLE Reservation(
  ReservationID INT PRIMARY KEY,
  RoomID        INT,
  UserID        INT,
  AssignmentID  INT,
  StartTime     VARCHAR(100) NOT NULL,
  EndTime       VARCHAR(100) NOT NULL,
  FOREIGN KEY (RoomID) REFERENCES Room(RoomID) ON DELETE CASCADE,
  FOREIGN KEY (UserID) REFERENCES User(UserID) ON DELETE CASCADE,
  FOREIGN KEY (AssignmentID) REFERENCES GroupAssignment(AssignmentID) ON DELETE CASCADE,
);

DROP TABLE GroupAssignment IF EXISTS;

CREATE TABLE GroupAssignment(
  AssignmentID INT PRIMARY KEY,
  UserID       INT,
  GroupName    VARCHAR(100) NOT NULL,
  FOREIGN KEY (UserID) REFERENCES User(UserID) ON DELETE CASCADE
);
