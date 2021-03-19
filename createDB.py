# creates a db that conforms to the Relational Model for Our Stuff
import sqlite3
def makeUserTable(cur):
	sql = '''CREATE TABLE USER (
		Email		TEXT		NOT NULL,
		Password	TEXT		NOT NULL,
		First_name	TEXT		NOT NULL,
		Last_name	TEXT		NOT NULL,
		DoB			TEXT,
		Owner		INTEGER,
		Renter		INTEGER,
		Street_address	TEXT,
		City		TEXT		NOT NULL,
		Province	TEXT,
		Postal_code	TEXT
	);'''
	cur.execute(sql)
	return 'USER'

def makePhoneTable(cur):
	return 'PHONE'

def makeAdminTable(cur):
	return 'ADMIN'

def makeReportTable(cur):
	return 'REPORT'

def makeCategoryTable(cur):
	return 'CATEGORY'

def makeItemTable(cur):
	return 'ITEM'

def makeItem_BlackoutTable(cur):
	return 'ITEM_BLACKOUT'

def makeTransactionTable(cur):
	return 'TRANSACTION'

def makeInterested_InTable(cur):
	return 'INTERESTED_IN'

def msg(name):
	print("\tTable created:",name)

def create():
	print("Creating ourStuff.db")
	con = sqlite3.connect('ourStuff.db')
	cur = con.cursor()
	msg(makeUserTable(cur))
	msg(makePhoneTable(cur))
	msg(makeAdminTable(cur))
	msg(makeReportTable(cur))
	msg(makeCategoryTable(cur))
	msg(makeItemTable(cur))
	msg(makeItem_BlackoutTable(cur))
	msg(makeTransactionTable(cur))
	msg(makeInterested_InTable(cur))
	con.commit()
	con.close()
