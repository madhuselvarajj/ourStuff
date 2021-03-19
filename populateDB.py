# populates ourStuff.db with fake data
import sqlite3

def populateUserTable(cur):
	users = [	('stephanedorotich@gmail.com', 'apples','Stephane', 'Dorotich', '1994-03-26', 0, 0, 'Not an address', 'Cochrane', 'Alberta', 'H0H 0H0'),
				('navjotsk99@gmail.com', 'oranges', 'Navjot', 'Singh', '2021-03-18', 0, 0, 'Not an address', 'Calgary', 'Alberta', 'H0H 0H0'),
				('madhuselvaraj24@gmail.com', 'grapes', 'Madhu', 'Selvaraj', '2021-03-18', 0, 0, 'Not an address', 'Calgary', 'Alberta', 'H0H 0H0')
				]
	cur.executemany('INSERT INTO USER VALUES (?,?,?,?,?,?,?,?,?,?,?)', users)
	# testing out "NOT NULL" constraint. It works!
	#cur.execute("INSERT INTO USER VALUES ('email@email.com','apples','Stephane',NULL,'birthday',1,1,'yes','Calgary','Alberta','TEHEHE')")
	return "4 USER"

def msg(val):
	print("Populated:",val)

def populate():
	print("Populating ourStuff.db")
	con = sqlite3.connect("ourStuff.db")
	cur = con.cursor()
	msg(populateUserTable(cur))
	con.commit()
	con.close()
