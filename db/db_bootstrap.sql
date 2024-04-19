-- This file is to bootstrap a database for the CS3200 project. 

-- Create a new database.  You can change the name later.  You'll
-- need this name in the FLASK API file(s),  the AppSmith 
-- data source creation.
DROP DATABASE IF EXISTS KitchenKorner;

CREATE DATABASE IF NOT EXISTS KitchenKorner;
-- Via the Docker Compose file, a special user called webapp will 
-- be created in MySQL. We are going to grant that user 
-- all privilages to the new database we just created. 
-- TODO: If you changed the name of the database above, you need 
-- to change it here too.
grant all privileges on KitchenKorner.* to 'webapp'@'%';
flush privileges;

-- Move into the database we just created.
-- TODO: If you changed the name of the database above, you need to
-- change it here too. 


USE KitchenKorner;

CREATE TABLE IF NOT EXISTS Users (
    User_ID int PRIMARY KEY,
    Username varchar(20) UNIQUE NOT NULL,
    Email varchar(50) UNIQUE NOT NULL,
    Full_Name text NOT NULL,
    Created_At datetime NOT NULL DEFAULT current_timestamp
);

CREATE TABLE IF NOT EXISTS Filters (
    Filter_ID int PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS Posts (
    Post_ID int PRIMARY KEY,
    User_ID int NOT NULL,
    Created_At datetime NOT NULL DEFAULT current_timestamp,
    Filter_ID int NOT NULL,
    CONSTRAINT fk_01 FOREIGN KEY (User_ID)
        REFERENCES Users(User_ID)
        ON UPDATE cascade ON DELETE cascade,
    CONSTRAINT fk_27 FOREIGN KEY (Filter_ID)
        REFERENCES Filters(Filter_ID)
        ON UPDATE cascade ON DELETE cascade
);

CREATE TABLE IF NOT EXISTS Ingredients (
    Amount int,
    Ingredient_ID int PRIMARY KEY ,
    Price float,
    Store varchar(30),
    Ingredient_Name varchar(20)
);

CREATE TABLE IF NOT EXISTS Recipes (
    Instructions text,
    Image blob,
    Meal_Type varchar(30) NOT NULL,
    Recipe_ID int PRIMARY KEY,
    Recipe_Name varchar(30),
    Post_ID int NOT NULL,
    Cuisine varchar(20) NOT NULL,
    Expected_Time time,
    Expected_Difficulty ENUM ('1', '2', '3', '4', '5', '6', '7', '8', '9', '10'),
    CONSTRAINT fk_02 FOREIGN KEY (Post_ID)
        REFERENCES Posts(Post_ID)
        ON UPDATE cascade ON DELETE cascade
);

CREATE TABLE IF NOT EXISTS IngredientDetails (
    Recipe_ID int NOT NULL,
    Ingredient_ID int NOT NULL,
    PRIMARY KEY (Recipe_ID, Ingredient_ID),
    CONSTRAINT fk_03 FOREIGN KEY (Recipe_ID)
        REFERENCES Recipes(Recipe_ID)
        ON UPDATE cascade ON DELETE cascade,
    CONSTRAINT fk_04 FOREIGN KEY (Ingredient_ID)
        REFERENCES Ingredients(Ingredient_ID)
        ON UPDATE cascade ON DELETE cascade
);

CREATE TABLE IF NOT EXISTS Comments (
    Text text,
    User_ID int NOT NULL,
    Timestamp datetime NOT NULL DEFAULT current_timestamp,
    Comment_ID int PRIMARY KEY,
    Post_ID int NOT NULL,
    CONSTRAINT fk_05 FOREIGN KEY (User_ID)
        REFERENCES Users(User_ID)
        ON UPDATE cascade ON DELETE cascade,
    CONSTRAINT fk_06 FOREIGN KEY (Post_ID)
        REFERENCES Posts(Post_ID)
        ON UPDATE cascade ON DELETE cascade
);

CREATE TABLE IF NOT EXISTS Ratings (
    Rating_ID int PRIMARY KEY,
    Actual_Difficulty ENUM ('1', '2', '3', '4', '5', '6', '7', '8', '9', '10'),
    Actual_Time float,
    Taste ENUM ('1', '2', '3', '4', '5', '6', '7', '8', '9', '10'),
    Post_ID int NOT NULL,
    User_ID int NOT NULL,
    CONSTRAINT fk_07 FOREIGN KEY (Post_ID)
        REFERENCES Posts(Post_ID)
        ON UPDATE cascade ON DELETE cascade,
    CONSTRAINT fk_08 FOREIGN KEY (User_ID)
        REFERENCES Users(User_ID)
        ON UPDATE cascade ON DELETE cascade
);

CREATE TABLE IF NOT EXISTS Follows (
    Followee_ID int NOT NULL,
    Follower_ID int NOT NULL,
    PRIMARY KEY (Followee_ID, Follower_ID),
    CONSTRAINT fk_09 FOREIGN KEY (Followee_ID)
        REFERENCES Users(User_ID)
        ON UPDATE cascade ON DELETE cascade,
    CONSTRAINT fk_10 FOREIGN KEY (Follower_ID)
        REFERENCES Users(User_ID)
        ON UPDATE cascade ON DELETE cascade
);

CREATE TABLE IF NOT EXISTS Feeds (
    Following_ID int NOT NULL,
    Post_ID int NOT NULL,
    User_ID int PRIMARY KEY,
    CONSTRAINT fk_32 FOREIGN KEY (Following_ID)
        REFERENCES Users(User_ID)
        ON UPDATE cascade ON DELETE cascade,
    CONSTRAINT fk_33 FOREIGN KEY (Post_ID)
        REFERENCES Posts(Post_ID)
        ON UPDATE cascade ON DELETE cascade,
    CONSTRAINT fk_34 FOREIGN KEY (User_ID)
        REFERENCES Users(User_ID)
        ON UPDATE cascade ON DELETE cascade
);

CREATE TABLE IF NOT EXISTS Cookbook (
    Cookbook_ID int PRIMARY KEY,
    Recipe_ID int NOT NULL,
    User_ID int NOT NULL,
    Modified_Datetime datetime,
    CONSTRAINT fk_11 FOREIGN KEY (Recipe_ID)
        REFERENCES Recipes(Recipe_ID)
        ON UPDATE cascade ON DELETE cascade,
    CONSTRAINT fk_12 FOREIGN KEY (User_ID)
        REFERENCES Users(User_ID)
        ON UPDATE cascade ON DELETE cascade
);

CREATE TABLE IF NOT EXISTS External_Messages (
    Message_ID int PRIMARY KEY,
    Post_ID int NOT NULL,
    User_ID int NOT NULL,
    Text text,
    CONSTRAINT fk_13 FOREIGN KEY (Post_ID)
        REFERENCES Posts(Post_ID)
        ON UPDATE cascade ON DELETE cascade,
    CONSTRAINT fk_14 FOREIGN KEY (User_ID)
        REFERENCES Users(User_ID)
        ON UPDATE cascade ON DELETE cascade
);

-- TODO: change tag id to user id
CREATE TABLE IF NOT EXISTS Tags (
    Post_ID int NOT NULL,
    User_ID int,
    PRIMARY KEY (Post_ID, User_ID),
    CONSTRAINT fk_15 FOREIGN KEY (Post_ID)
        REFERENCES Posts(Post_ID)
        ON UPDATE cascade ON DELETE cascade,
    CONSTRAINT fk_35 FOREIGN KEY (User_ID)
        REFERENCES Users(User_ID)
        ON UPDATE cascade ON DELETE cascade
);

CREATE TABLE IF NOT EXISTS Recipe_Cookbook (
    Recipe_ID int NOT NULL,
    Cookbook_ID int NOT NULL,
    PRIMARY KEY (Recipe_ID, Cookbook_ID),
    CONSTRAINT fk_18 FOREIGN KEY (Recipe_ID)
        REFERENCES Recipes(Recipe_ID)
        ON UPDATE cascade ON DELETE cascade,
    CONSTRAINT fk_19 FOREIGN KEY (Cookbook_ID)
        REFERENCES Cookbook(Cookbook_ID)
        ON UPDATE cascade ON DELETE cascade
);

CREATE TABLE IF NOT EXISTS Keywords_In (
    Filter_ID int PRIMARY KEY,
    Keyword_One tinytext,
    Keyword_Two tinytext,
    Keyword_Three tinytext,
    Keyword_Four tinytext,
    Keyword_Five tinytext,
    Keyword_Six tinytext,
    Keyword_Seven tinytext,
    Keyword_Eight tinytext,
    Keyword_Nine tinytext,
    Keyword_Ten tinytext,
    CONSTRAINT fk_28 FOREIGN KEY (Filter_ID)
        REFERENCES Filters(Filter_ID)
        ON UPDATE cascade ON DELETE cascade
);

CREATE TABLE IF NOT EXISTS Keywords_Out (
    Filter_ID int PRIMARY KEY,
    Keyword_One tinytext,
    Keyword_Two tinytext,
    Keyword_Three tinytext,
    Keyword_Four tinytext,
    Keyword_Five tinytext,
    Keyword_Six tinytext,
    Keyword_Seven tinytext,
    Keyword_Eight tinytext,
    Keyword_Nine tinytext,
    Keyword_Ten tinytext,
    CONSTRAINT fk_29 FOREIGN KEY (Filter_ID)
        REFERENCES Filters(Filter_ID)
        ON UPDATE cascade ON DELETE cascade
);

-- TODO: Update to be receiver and sender
CREATE TABLE IF NOT EXISTS Direct_Messages (
    User_ID int NOT NULL,
    Text text,
    Time_sent datetime NOT NULL DEFAULT current_timestamp,
    Post_ID int NOT NULL,
    PRIMARY KEY (User_ID, Time_sent),
    CONSTRAINT fk_24 FOREIGN KEY (User_ID)
        REFERENCES Users(User_ID)
        ON UPDATE cascade ON DELETE cascade,
    CONSTRAINT fk_25 FOREIGN KEY (Post_ID)
        REFERENCES Posts(Post_ID)
        ON UPDATE cascade ON DELETE cascade
);
