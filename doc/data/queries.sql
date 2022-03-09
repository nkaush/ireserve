SELECT r.RoomNumber, b.BuildingName, r.RoomCapacity, r.Popularity
FROM Room r NATURAL JOIN Building b
WHERE r.RoomID NOT IN (SELECT res.RoomID
  FROM Reservation res
  WHERE CURRENT_TIMESTAMP BETWEEN res.StartTime AND res.EndTime
)
ORDER BY b.BuildingName, r.Popularity;