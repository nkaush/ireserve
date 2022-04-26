SELECT * FROM building b NATURAL JOIN room r
WHERE NOT EXISTS (SELECT * FROM reservation res WHERE r.RoomID = res.RoomID AND res.StartTime = "2022-04-26 15:00:00")
ORDER BY Popularity DESC;