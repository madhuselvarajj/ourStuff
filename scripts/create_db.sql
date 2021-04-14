-- SQL Script:
--      Declare "Our Stuff" Relational Database

/*
USER:
    NAME            FORMAT          TYPE        VALIDATION?
    -------------------------------------------------------
    Email:          "*@*.*"         TEXT        yes
    Password:       "________%"     TEXT        yes
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
    Email			TEXT		PRIMARY KEY,
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
    Email			TEXT,
    Phone_number	TEXT,
    PRIMARY KEY (Email, Phone_number),
    CONSTRAINT
        USR_FK FOREIGN KEY (Email) REFERENCES USER(Email)
            ON DELETE CASCADE       ON UPDATE CASCADE
);

CREATE TABLE ADMIN
(
    Admin_ID		TEXT		PRIMARY KEY,
    Password		TEXT		NOT NULL
);

CREATE TABLE REPORT
(
    User_email			TEXT,
    Reported_user_email	TEXT,
    Admin_ID			TEXT,
    Offense_description	TEXT,
    Date_of_offense		TEXT,
    Date_of_report		TEXT		NOT NULL,
    PRIMARY KEY (User_email,Reported_user_email,Date_of_offense),
    CONSTRAINT
        USR_FK FOREIGN KEY (User_email) REFERENCES USER(Email)
            ON DELETE SET NULL      ON UPDATE CASCADE,
    CONSTRAINT
        R_USR_FK FOREIGN KEY (Reported_user_email) REFERENCES USER(Email)
            ON DELETE SET NULL      ON UPDATE CASCADE,
    CONSTRAINT
        ADMN_FK FOREIGN KEY (Admin_ID) REFERENCES ADMIN(Admin_ID)
            ON DELETE SET NULL      ON UPDATE CASCADE
);

CREATE TABLE CATEGORY
(
    Name			TEXT        PRIMARY KEY,
    Parent			TEXT,
    CONSTRAINT
        CTGRY_FK FOREIGN KEY (Parent) REFERENCES CATEGORY(Name)
            ON DELETE CASCADE       ON UPDATE CASCADE
);

CREATE TABLE ITEM
(
    Title			TEXT,
    Category_name	TEXT,
    Owner_email		TEXT,
    Description		TEXT,
    Daily_rate		REAL,
    PRIMARY KEY (Title, Owner_email),
    CONSTRAINT
        USR_FK FOREIGN KEY (Owner_email) REFERENCES USER(Email)
            ON DELETE CASCADE       ON UPDATE CASCADE,
    CONSTRAINT
        CTGRY_FK FOREIGN KEY (Category_name) REFERENCES CATEGORY(Category_name)
            ON DELETE SET NULL      ON UPDATE CASCADE
);

CREATE TABLE ITEM_BLACKOUT
(
    Title			TEXT,
    Owner_email		TEXT,
    Start_date		TEXT,
    End_date		TEXT,
    PRIMARY KEY (Title, Owner_email, Start_date),
    CONSTRAINT
        ITM_FK FOREIGN KEY (Title, Owner_email) REFERENCES ITEM(Title, Owner_email)
            ON DELETE CASCADE       ON UPDATE CASCADE,
    CONSTRAINT
        USR_FK FOREIGN KEY (Owner_email) REFERENCES USER(Email)
            ON DELETE CASCADE       ON UPDATE CASCADE
);

CREATE TABLE RENTAL
(
    tID				INTEGER		PRIMARY KEY,
    Renter_email	TEXT		NOT NULL,
    Owner_email		TEXT		NOT NULL,
    Item_title		TEXT		NOT NULL,
    Start_date		TEXT		NOT NULL,
    Duration		INTEGER		NOT NULL,
    Pick_up_time	TEXT		NOT NULL,
    Drop_off_time	TEXT		NOT NULL,
    Type			TEXT		NOT NULL,
    Rating			INTEGER     DEFAULT NULL,
    Review			TEXT        DEFAULT NULL,
    CONSTRAINT
        RENTER_FK FOREIGN KEY (Renter_email) REFERENCES USER(Email)
            ON DELETE SET NULL       ON UPDATE CASCADE,
    CONSTRAINT
        OWNER_FK FOREIGN KEY (Owner_email) REFERENCES USER(Email)
            ON DELETE SET NULL      ON UPDATE CASCADE,
    CONSTRAINT
        ITM_FK FOREIGN KEY (Item_title, Owner_email) REFERENCES ITEM(Title, Owner_email)
            ON DELETE SET NULL      ON UPDATE CASCADE
);

CREATE TABLE INTERESTED_IN
(
    User_email		TEXT,
    Category_name	TEXT,
    PRIMARY KEY (User_email, Category_name)
    CONSTRAINT
        USR_FK FOREIGN KEY (User_email) REFERENCES USER(Email)
            ON DELETE CASCADE       ON UPDATE CASCADE,
    CONSTRAINT
        CTGRY_FK FOREIGN KEY (Category_name) REFERENCES CATEGORY(Name)
            ON DELETE CASCADE       ON UPDATE CASCADE
);
