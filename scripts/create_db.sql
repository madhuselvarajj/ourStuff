-- SQL Script:
--      Declare "Our Stuff" Relational Database

/*
USER:
    NAME            FORMAT          TYPE        VALIDATION?
    -------------------------------------------------------
    Email:          "*@*.*"         TEXT        yes
    Password:       "*"             TEXT        no
    First_name:     "*"             TEXT        no
    Last_name:      "*"             TEXT        no
    DoB:            "YYYY-MM-DD"    TEXT        yes
    Owner:          -removed
    Renter:         -removed
    Street_address: "*"             TEXT        no
    City:           "*"             TEXT        no
    Province:       "aa"            TEXT        yes
    Postal_code     "a#a #a#"       TEXT        yes
    =======================================================
*/
CREATE TABLE USER
(
    Email			TEXT		NOT NULL,
    Password		TEXT		NOT NULL,
    First_name		TEXT		NOT NULL,
    Last_name		TEXT		NOT NULL,
    DoB				TEXT,
    Street_address	TEXT,
    City			TEXT		NOT NULL,
    Province		TEXT,
    Postal_code		TEXT
);

CREATE TABLE PHONE
(
    Email			TEXT		NOT NULL,
    Area_code		TEXT		NOT NULL,
    Phone_number	TEXT		NOT NULL
);

CREATE TABLE ADMIN
(
    Admin_ID		INTEGER		NOT NULL,
    Password		TEXT		NOT NULL	
);

CREATE TABLE REPORT
(
    User_email			TEXT		NOT NULL,
    Reported_user_email	TEXT		NOT NULL,
    Admin_ID			TEXT,
    Offense_description	TEXT,
    Date_of_offense		TEXT		NOT NULL,
    Date_of_report		TEXT		NOT NULL	
);

CREATE TABLE CATEGORY
(
    Name			TEXT		NOT NULL,
    Parent			TEXT	
);

CREATE TABLE ITEM
(
    Title			TEXT,
    Category_name	TEXT,
    Owner_email		TEXT,
    Description		TEXT,
    Daily_rate		INTEGER	
);

CREATE TABLE ITEM_BLACKOUT
(
    Title			TEXT,
    Owner_email		TEXT,
    Start_date		TEXT,
    End_date		TEXT
);

CREATE TABLE RENTAL
(
    tID				INTEGER		NOT NULL,
    Renter_email	TEXT		NOT NULL,
    Owner_email		TEXT		NOT NULL,
    Item_title		TEXT		NOT NULL,
    Start_date		TEXT		NOT NULL, 
    Duration		INTEGER		NOT NULL,
    Pick_up_time	TEXT		NOT NULL,
    Drop_off_time	TEXT		NOT NULL,
    Type			TEXT		NOT NULL,
    Rating			INTEGER,
    Review			TEXT
);

CREATE TABLE INTERESTED_IN
(
    User_email		TEXT		NOT NULL,
    Category_name	TEXT		NOT NULL
);
