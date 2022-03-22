# Database Design

## Data Definition Language Commands

```sql
CREATE DATABASE `ireserve`;

USE `ireserve`;

DROP TABLE IF EXISTS `user`;

CREATE TABLE `user` (
  `UserID` INT PRIMARY KEY, 
  `FirstName` VARCHAR(255) NOT NULL,
  `LastName` VARCHAR(255) NOT NULL, 
  `Email` VARCHAR(255) NOT NULL, 
  `HashedPassword` VARCHAR(255) NOT NULL
);

DROP TABLE IF EXISTS `building`;

CREATE TABLE `building` (
  `BuildingID` INT PRIMARY KEY,
  `Address` VARCHAR(255) NOT NULL,
  `BuildingName` VARCHAR(255) NOT NULL,
  `Region` VARCHAR(255) NOT NULL
);

DROP TABLE IF EXISTS `room`;

CREATE TABLE `room` (
  `RoomID` INT PRIMARY KEY,
  `BuildingID` INT,
  `FloorNumber` INT,
  `RoomNumber` INT,
  `RoomCapacity` INT,
  `RoomType` VARCHAR(50) NOT NULL,
  `Popularity` REAL,
  FOREIGN KEY (`BuildingID`) REFERENCES `building` (`BuildingID`) ON DELETE CASCADE
);

DROP TABLE IF EXISTS `groupassignment`;

CREATE TABLE `groupassignment`(
  `AssignmentID` INT PRIMARY KEY,
  `UserID` INT,
  `GroupName` VARCHAR(100) NOT NULL,
  FOREIGN KEY (`UserID`) REFERENCES `user` (`UserID`) ON DELETE CASCADE
);

DROP TABLE IF EXISTS `reservation`;

CREATE TABLE `reservation` (
  `ReservationID` INT PRIMARY KEY,
  `RoomID` INT,
  `UserID` INT,
  `AssignmentID` INT,
  `StartTime` VARCHAR(100) NOT NULL,
  `EndTime` VARCHAR(100) NOT NULL,
  FOREIGN KEY (`RoomID`) REFERENCES `room` (`RoomID`) ON DELETE CASCADE,
  FOREIGN KEY (`UserID`) REFERENCES `user` (`UserID`) ON DELETE CASCADE,
  FOREIGN KEY (`AssignmentID`) REFERENCES `groupassignment` (`AssignmentID`) ON DELETE CASCADE
);
```

## Database Implementation

![](images/tables.png)

## Data Insertion

![](images/counts/building_count.png)
![](images/counts/group_assignment_count.png)
![](images/counts/group_count.png)
![](images/counts/reservation_count.png)
![](images/counts/room_count.png)
![](images/counts/user_count.png)

## Advanced Query 1

Find all priority users. We define priority users as those who are in a group for a 400 level CS course or have made 7 or more reservations with our application.

```sql
(SELECT DISTINCT u.FirstName, u.LastName
 FROM `user` u NATURAL JOIN `groupassignment` ga NATURAL JOIN `group` grp
 WHERE grp.GroupName LIKE 'CS4__ %'
)
UNION
(SELECT u.FirstName, u.LastName FROM `user` u
 WHERE u.UserID IN (SELECT r.UserID 
                    FROM reservation r 
                    GROUP BY r.UserID 
                    HAVING COUNT(r.UserID) >= 7)
)
```

Results:
![](images/query1.png)

## Advanced Query 2

Find all all buildings with reservations made in them in May 2021 and with an average room populatity larger than 50.

```sql 
SELECT tmp.BuildingName, AVG(tmp.Popularity) AS AVG_POPULARITY
FROM (SELECT * FROM room r NATURAL JOIN building b
WHERE r.RoomID IN (SELECT res.RoomID FROM reservation res WHERE res.StartTime LIKE "2021-05%")) AS tmp
GROUP BY tmp.BuildingName
HAVING AVG(tmp.Popularity) > 50
ORDER BY AVG_POPULARITY DESC;
```

Results:
![](images/query2.png)

## Advanced Query 1 Indices

### Index 1

### Index 2

### Index 3 

## Advanced Query 2 Indices

### Index 1

### Index 2

### Index 3 
