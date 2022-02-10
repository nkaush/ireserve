# iReserve

Our project is a room reserver web application that allows users to book study rooms around campus. This app allows users to view the availability of study rooms around them and place reservations on study rooms if they wish to use them in the future. The application will also allow users to search for a room in any area of campus they wish and receive. Our application will also allow users to block off a room if they are in the vicinity and the room is available. 

## Detailed Description

State as clearly as possible what you want to do. What problem do you want to solve, etc.?

@Amaan (maybe)

## Usefulness

Too many times, freshmen (and this year sophmores) have had to book rooms for team meetings that are far from their residences. This is fine for larger and more official meetings, but for project meetings as a club, or small get-togethers, booking a room in Grainger using LibCal is just too much of a walk and hassle. Especially in the winter time, it becomes unsafe for freshman to venture out to these places far from their dorms to hold meetings. 

This is why we have build iReserve, the all in one application that allows freshman (or really anyone for that matter) the ability to book study spaces, lounges, and single person rooms right in the comfort of their own dorms. With the ability to filter out types of spaces, where they are, and what their popularity is, freshman do not have to go out when they can hold their meetings in spaces within the dorms. 

We have loaded in all the dorm maps, with all floors, and have a way to see if a room has been booked so their are no overlaps. Every dorm is loaded in, so anywhere someone wants to make a meeting in-person, they can with our service. 

As previosly mentioned, there are applications on campus like LibCal, and the older ARC reservation system during SP21, but nothing dedicated to undergraduates and specifically freshman who are the future of alot of the clubs they want to hold meeings for. The prior reservation apps are complicated and have outdated UIs, whereas ours is modern and easy to follow. The previous systems had alot of overlap and issues with reserving rooms that were already taken, and our application uses popularity and crowdsourcing to make sure that someone who makes a reservation system leaves before another one is made.  


## Realness

Our data is the physical locations of study rooms, lounges, and areas across campus, focused on the dorm buildings (ex. ISR, PAR). We will obtain our data by going through the floor plans of buildings we would like to include into our system and gather the areas that can be reserved. The floor plans for the dorm buildings are public information that we will be able to easily download and access from various websites.

## Functionality 

A lot of our functionality comes under our room reservation feature. Users will be able to schedule room reservations in advance.

We plan on having a handful of tables to model our data. 
- We will use a `Rooms` table to model study rooms by their `building`, `floor`, `room number`, `room type` (lounge, study room, etc.), and `capacity`.
- We will use a `Buildings` table to model locations of study spots around campus using `building name`, `location on campus`, and `popularity`. 
- We will use a `Users` table to model users who wish to  reserve rooms using `user id`, `name`, `email`, `hashed password`. 

We plan on presenting a list of all rooms available on the front page of the website with a timeline of the next day or so. The timeline will consist of 30 minute chunks, indicating whether or not a room was reserved at time interval. 

There are a lot of rooms to choose from, so we will group rooms by the criteria the user specifies. Users may also sort rooms by popularity, room capacity, and elevation (higher floors have better views of campus). Users may also filter rooms by this criteria as well as location on campus and room type. 

We plan to create triggers to update and compute popularity scores of each room. Anytime a reservation is added to our table of reservations, we will re-calculate the popularity of that specific room reserved. 

@Neil
1. talk about study group modification
2. talk about find me a room thing
3. talk about book current room thing

This is where you talk about what the website delivers. Talk about how a user would interact with the application (i.e. things that one could create, delete, update, or search for). Read the requirements for stages 4 and 5 to see what other functionalities you want to provide to the users. You should include:
Describe what data is stored in the database. (Where is the data from, what attributes and information would be stored?)
What are the basic functions of your web application? (What can users of this website do? Which simple and complex features are there?)
What would be a good creative component (function) that can improve the functionality of your application? (What is something cool that you want to include? How are you planning to achieve it?)

## Mockup
[Mock-up Of Database Project .pdf](https://github-dev.cs.illinois.edu/sp22-cs411/sp22-cs411-team049-PreQL/files/25/Mock-up.Of.Database.Project.pdf)

## Work Distribution
The following is a table of the high-level tasks involved and its respective team members who are in charge of that feature

| **Task**                                                                    | **Person**                                                                                                  |
|-----------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------|
| UI Development                                                              | Akul  <br>Shalin<br><br>_(everyone can basically <br>work on the UI for their <br>respective pages though)_ |
| Database Creation<br>(includes creating the map based on UIUC study spaces) | Neil<br>Amaan<br>Akul<br>Shalin                                                                                               |
| Home Page Development<br>(including Timeline & list of available rooms)     | Akul<br>Neil                                                                                                |
| Login & Sign-up Page                                                        | Shalin<br>Amaan                                                                                             |
| Make Reservation page                                                       | Akul<br>Shalin                                                                                             |
| "Find me a Room" page                                                       | Akul<br>Amaan                                                                                               |
| Book Current Room                                                           | Neil<br>Shalin                                                                                              |
