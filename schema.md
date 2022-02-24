# UML Diagram

# Relational Schema

```
User(
  UserID:INT [PK], 
  FirstName:VARCHAR(255),
  LastName:VARCHAR(255), 
  Email:VARCHAR(255), 
  HashedPassword:VARCHAR(255)
)

Room(
  RoomID:INT [PK],
  BuildingID:INT [FK to Building.BuildingId],
  FloorNumber:INT,
  RoomNumber:INT,
  RoomCapacity:INT,
  RoomType:VARCHAR(50),
  Popularity:REAL
)

Building(
  Address:VARCHAR(255) [PK],
  BuildingName:VARCHAR(255),
  Region:VARCHAR(255),
)

Reservation(
  ReservationID:INT [PK]
  RoomID:INT [FK to Room.RoomId]
  UserID:INT [FK to User.UserID]
  AssignmentID:INT [FK to GroupAssignment.AssignmentID],
  StartTime:VARCHAR(100)
  EndTime:VARCHAR(100)
)

GroupAssignment(
  AssignmentID:INT [PK],
  UserID:INT [FK to User.UserID]
  GroupName:VARCHAR(100)
)
```