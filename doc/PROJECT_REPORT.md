# Final Project Proposal

## 1. Changes since Stage 1:
We kept the same direction and general purpose of the project with little change in our implementation. We kept the same tables, goals, and update/insert statements as we had planned out in the proposal. 

We did however have some changes with regards to the use of our stored procedure, advanced queries, and triggers from what we had originally thought. Popularity was calculated using our advanced queries rather than the trigger that we originally listed out in our proposal. The trigger was used to <b>update</b> the popularity rather than determine it. The stored procedure was used to calculate the stars rating of each room. 

## 2. What we achieved and/or failed to achieve based on usefulness:

### a) Achieved: 
We achieved the ability to reserve rooms for freshman (or anyone) who wanted a place to hold group meetings for clubs/teams in the comfort of their own dorm. By taking into account all available rooms in all freshman dorms (including PAR, LAR, ISR, and the Ikenberry dorms) we were able to achieve the goal of having a safe and secure way for freshman to reserve spaces closer to where they live. 

We achieved the ability for people to book study spaces, lounges, and single person rooms right in the comfort of their own dorms.

Every dorm was loaded in, and every floor and available room was accounted for. 

We achieved getting popularity based on frequency of reservation, and people are able to see their favorite rooms rating. 

### b) Did not achieve:
We were able to filter out names of buildings based on our SEARCH functionality, and by the times those buildings were available, but we couldn`t filter out the types of spaces or by location. 

## 3. Did we change the schema or source of data for our project:
We added a `BuildingID` to our `building` table in our schema that wasn't there in the original one. This now serves as our primary key, whereas the `address` was the primary key in the old schema. 

We added a the foreign key `BuildingID` to our `room` table that references the building that each room is in.

We created a `group` table with `GroupID` as our primary key, and a `GroupName` field

We also added two foreign keys to our `groupassignment` table. This was `UserID` to refer to users, and `GroupID` to refer to groups. 

We did change the source of data as we progressed through the project. Seeing the amount of data that we needed to fill, we had to create some data from rooms across each of the halls because enough study rooms and spaces weren`t available. We changed the source from online publicly available data on floor plans for each room, to our own generated data. 

## 4. Discussing changes to our UML Diagram and why we think they were needed:

As discussed in number 3 above, we added another table and a variety of foreign keys to our implementation.

We added a `BuildingID` to our `building` table in our schema that wasn't there in the original one. This now serves as our primary key, wheras the `address` was the primary key in the old schema (from part 3). This replaces the address in the UML diagram and is now the created and underlined attribute for each building. 

We added a the foreign key `BuildingID` to our `room` table that references the building that each room is in (from part 3). So now in the UML diagram, we will add another filled in orange attribute denoting a foreign key for `BuildingID`. 

We created a `group` table with `GroupID` as our primary key, and a `GroupName` field (from part 3). This means that we would make a new `group` table right under the `groupassignment` table in the UML diagram and add a 1..1 relation in both directions for those tables. We will have the underlined `GroupID` primary key for the `group` table. 

We also added two foreign keys to our `groupassignment` table. This was `UserID` to refer to users, and `GroupID` to refer to groups (from part 3). This means that in the UML diagram, we would have two filled in orange boxes with `GroupID` and `UserID` under it. 

We made these changes because we felt that we needed more foreign keys to identify and connect tables and their attributes with others. This is so our queries, triggers, and stored procedures could access rooms, buildings, and which group made which reservation using those foreign keys to rate rooms and calculate popularity. The group table was a good addition because it allowed each group the user was a part of to have their own name and unique ID. The new changes make it a better design because of increased interconnectedness and access to attributes from more table to do more displaying and analyzing of data. 

## 5. What functionalities did we add/remove:

We added the functionality to join a group that wasn't there in our original implementation. This means that the user can join any one of the available groups that have been created, and can join multiple groups. This allows them to make reservation using those groups for specific rooms. 

We added the heat map of rooms and their relative number of reservations using the blue dots to represent reservation count. This allows the user to see the whole map of dorms and see how many reservations are being made in each building.  

We removed the functionality to automatically find the user a room based on their current location in present time. Rather, we just had them reserve available rooms based on time. 

## 6. How our advanced database programs complement our application (Amaan): 

## 7. Each team member's technical challenge (Neil): 

## 8. Other changes in the final application from the original proposal (Amaan):

## 9. What future work we can do to improve the application (besides interface) (Neil):

## 10. Final Division of labor and how well we managed teamwork (Amaan): 




    

     

