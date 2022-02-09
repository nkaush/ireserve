# iReserve

Our project is a room reserver web application that allows users to book study rooms around campus. This app allows users to view the availability of study rooms around them and place reservations on study rooms if they wish to use them in the future. The application will also allow users to search for a room in any area of campus they wish and receive. Our application will also allow users to block off a room if they are in the vicinity and the room is available. 

## Detailed Description

State as clearly as possible what you want to do. What problem do you want to solve, etc.?

## Usefulness

Explain as clearly as possible why your chosen application is useful. Make sure to answer the following questions: Are there any similar websites/applications out there?  If so, what are they, and how is yours different?

## Realness

Describe what your data is and where you will get it.

## Functionality 

A lot of our functionality comes under our room reservation feature. Users will be able to schedule room reservations in advance.

We plan on having a handful of tables to model our data. 
- We will use a `Rooms` table to model study rooms by their `building`, `floor`, `room number`, `room type` (lounge, study room, etc.), and `capacity`.
- We will use a `Buildings` table to model locations of study spots around campus using `building name`, `location on campus`, and `popularity`. 
- We will use a `Users` table to model users who wish to  reserve rooms using `user id`, `name`, `email`, `hashed password`. 

We plan on presenting a list of all rooms available on the front page of the website with a timeline of the next day or so. The timeline will consist of 30 minute chunks, indicating whether or not a room was reserved at time interval. 

There are a lot of rooms to choose from, so we will group rooms by the criteria the user specifies. Users may also sort rooms by popularity, room capacity, and elevation (higher floors have better views of campus). Users may also filter rooms by this criteria as well as location on campus and room type. 

We plan to create triggers to update and compute popularity scores of each room. Anytime a reservation is added to our table of reservations, we will re-calculate the popularity of that specific room reserved. 

@todo
1. talk about study group modification
2. talk about find me a room thing
3. talk about book current room thing

This is where you talk about what the website delivers. Talk about how a user would interact with the application (i.e. things that one could create, delete, update, or search for). Read the requirements for stages 4 and 5 to see what other functionalities you want to provide to the users. You should include:
Describe what data is stored in the database. (Where is the data from, what attributes and information would be stored?)
What are the basic functions of your web application? (What can users of this website do? Which simple and complex features are there?)
What would be a good creative component (function) that can improve the functionality of your application? (What is something cool that you want to include? How are you planning to achieve it?)

## Mockup

`<insert image here>`

## Work Distribution

