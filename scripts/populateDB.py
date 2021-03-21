# populates ourStuff.db with fake data
import sqlite3

def populateUserTable(cur):
	users = [	('stephanedorotich@gmail.com', 'apples','Stephane', 'Dorotich', '1994-03-26', 0, 0, 'Not an address', 'Cochrane', 'Alberta', 'H0H 0H0'),
				('navjotsk99@gmail.com', 'oranges', 'Navjot', 'Singh', '2021-03-18', 0, 0, 'Not an address', 'Calgary', 'Alberta', 'H0H 0H0'),
				('madhuselvaraj24@gmail.com', 'grapes', 'Madhu', 'Selvaraj', '2021-03-18', 0, 0, 'Not an address', 'Calgary', 'Alberta', 'H0H 0H0')
				]
	cur.executemany('INSERT INTO USER VALUES (?,?,?,?,?,?,?,?,?,?,?)', users)
	return "USER table with {} inserts".format(len(users))

def populatePhoneTable(cur):
	phones = [	('stephanedorotich@gmail.com','403','444-9910'),
				('stephanedorotich@gmail.com','587','444-9910'),
				('navjotsk99@gmail.com','999','999-9999')
				]
	cur.executemany('INSERT INTO PHONE VALUES (?,?,?)', phones)
	return "PHONE table with {} inserts".format(len(phones))

def populateAdminTable(cur):
	sql = '''INSERT INTO ADMIN VALUES (12345, 'securePassword')'''
	cur.execute(sql)
	return "ADMIN table with 1 insert"

def populateReportTable(cur):
	reports = [
		('navjotsk99@gmail.com','stephanedorotich@gmail.com',False,'His hair is too long','2021-03-04','2021-03-21'),
		('stephanedorotich@gmail.com','navjotsk99@gmail.com',False,"She doesn't like my hair",'2021-03-21','2021-03-21')
	]
	cur.executemany('INSERT INTO REPORT VALUES (?,?,?,?,?,?)', reports)
	return "REPORT table with {} inserts".format(len(reports))

def populateCategoryTable(cur):
	categories = [
		("Books",False),
		("Equipment",False),
		("Romance Novels","Books"),
		("Historical Fiction","Books"),
		("Non-fiction","Books"),
		("Music",False),
		("Music Equipment","Music"),
		("Instruments","Music"),
		("Power Tools","Equipment")
	]
	cur.executemany('INSERT INTO CATEGORY VALUES (?,?)', categories)
	return "CATEGORY table with {} inserts".format(len(categories))

def populateItemTable(cur):
	items = [
		("Shogun, James Clavell","Historical Fiction","stephanedorotich@gmail.com","My favorite book",1),
		("Acoustic Solutions ASG-150","Music Equipment","stephanedorotich@gmail.com","A great portable PA with 4 channels",30),
		("Fundamentals of Database Systems, Elmasri and Navathe","Non-fiction","stephanedorotich@gmail.com","CPSC 471 textbook",2)
	]
	cur.executemany('INSERT INTO ITEM VALUES (?,?,?,?,?)', items)
	return "ITEM table with {} inserts".format(len(items))

def populateItem_BlackoutTable(cur):
	item_blackouts = [
		("Shogun, James Clavell","stephanedorotich@gmail.com","2021-03-01","2021-03-31")
	]
	cur.executemany('INSERT INTO ITEM_BLACKOUT VALUES (?,?,?,?)', item_blackouts)
	return "ITEM_BLACKOUT table with {} inserts".format(len(item_blackouts))

def populateTransactionTable(cur):
	transactions = [
		(1,"madhuselvaraj24@gmail.com","stephanedorotich@gmail.com","Fundamentals of Database Systems, Elmasri and Navathe","2021-03-01",14,"10:30","10:30","complete",False,False),
		(1,"navjotsk99@gmail.com","stephanedorotich@gmail.com","Fundamentals of Database Systems, Elmasri and Navathe","2021-03-25", 14,"13:45","20:00","Pending",False,False)
	]
	cur.executemany('INSERT INTO RENTAL VALUES (?,?,?,?,?,?,?,?,?,?,?)', transactions)
	return "RENTAL table with {} inserts".format(len(transactions))

def populateInterested_InTable(cur):
	interests = [
		("stephanedorotich@gmail.com","Historical fiction"),
		("stephanedorotich@gmail.com","Music"),
		("stephanedorotich@gmail.com","Non-fiction")
	]
	cur.executemany('INSERT INTO INTERESTED_IN VALUES (?,?)', interests)
	return "INTERESTED_IN table with {} inserts".format(len(interests))

def msg(val):
	print("\tPopulated ",val)

def populate():
	print("Populating ourStuff.db")
	con = sqlite3.connect("ourStuff.db")
	cur = con.cursor()
	msg(populateUserTable(cur))
	msg(populatePhoneTable(cur))
	msg(populateAdminTable(cur))
	msg(populateReportTable(cur))
	msg(populateCategoryTable(cur))
	msg(populateItemTable(cur))
	msg(populateItem_BlackoutTable(cur))
	msg(populateTransactionTable(cur))
	msg(populateInterested_InTable(cur))
	con.commit()
	con.close()
