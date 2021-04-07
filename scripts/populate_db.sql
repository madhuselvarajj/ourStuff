INSERT INTO USER VALUES
	("stephanedorotich@gmail.com", "apples", "Stephane", "Dorotich", "1994-03-26", "Not an address", "Cochrane", "Alberta", "H0H 0H0"),
	("navjotsk99@gmail.com", "oranges", "Navjot", "Singh", "2021-03-18", "Not an address", "Calgary", "Alberta", "H0H 0H0"),
	("madhuselvaraj24@gmail.com", "grapes", "Madhu", "Selvaraj", "2021-03-18", "Not an address", "Calgary", "Alberta", "H0H 0H0");

INSERT INTO PHONE VALUES
	("stephanedorotich@gmail.com", "403-444-9910"),
	("stephanedorotich@gmail.com", "587-444-9910"),
	("navjotsk99@gmail.com", "999-999-9999");

INSERT INTO ADMIN VALUES
	(12345, "securePassword");

INSERT INTO REPORT VALUES
	("navjotsk99@gmail.com", "stephanedorotich@gmail.com", NULL, "His hair is too long", "2021-03-04", "2021-03-21"),
	("stephanedorotich@gmail.com", "navjotsk99@gmail.com", NULL, "She doesn't like my hair", "2021-03-21", "2021-03-21");

INSERT INTO CATEGORY VALUES
	("Books", NULL),
	("Equipment", NULL),
	("Romance Novels", "Books"),
	("Historical Fiction", "Books"),
	("Non-fiction", "Books"),
	("Music", NULL),
	("Music Equipment", "Music"),
	("Instruments", "Music"),
	("Power Tools", "Equipment"),
	("Sports", NULL);

INSERT INTO ITEM VALUES
	("Shogun, James Clavell", "Historical Fiction", "stephanedorotich@gmail.com", "My favorite book", 1.5),
	("Acoustic Solutions ASG-150", "Music Equipment", "stephanedorotich@gmail.com", "A great portable PA with 4 channels", 30.0),
	("Fundamentals of Database Systems, Elmasri and Navathe", "Non-fiction", "stephanedorotich@gmail.com", "CPSC 471 textbook", 2.0);

INSERT INTO ITEM_BLACKOUT VALUES
	("Shogun, James Clavell", "stephanedorotich@gmail.com", "2021-03-01", "2021-03-31");

INSERT INTO RENTAL VALUES
	(0, "madhuselvaraj24@gmail.com", "stephanedorotich@gmail.com", "Fundamentals of Database Systems, Elmasri and Navathe", "2021-03-01", 14, "10:30", "10:30", "complete", 0, "0"),
	(1, "navjotsk99@gmail.com", "madhuselvaraj24@gmail.com", "book", "2021-03-01", 14, "10:30", "10:30", "pending", 0, "0"),
	(2, "navjotsk99@gmail.com", "stephanedorotich@gmail.com", "Fundamentals of Database Systems, Elmasri and Navathe", "2021-03-25", 14, "13:45", "20:00", "pending", 0, "0");

INSERT INTO INTERESTED_IN VALUES
	("stephanedorotich@gmail.com", "Historical fiction"),
	("stephanedorotich@gmail.com", "Music"),
	("stephanedorotich@gmail.com", "Non-fiction");
