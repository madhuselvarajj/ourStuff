# create a db for Our Stuff
import sqlite3

# TODO
#	Set Primary Keys for each table
#	Set Foreign Keys for each table
#	Enforce type checking for:
#		Date
#		Time
#		Phone number
#		Postal Code
#		Names (alpha characters only)

def makeUserTable(cur):
	sql = '''CREATE TABLE USER (
		Email			TEXT		NOT NULL,
		Password		TEXT		NOT NULL,
		First_name		TEXT		NOT NULL,
		Last_name		TEXT		NOT NULL,
		DoB				TEXT,
		Owner			INTEGER,
		Renter			INTEGER,
		Street_address	TEXT,
		City			TEXT		NOT NULL,
		Province		TEXT,
		Postal_code		TEXT
		);'''
	cur.execute(sql)
	return 'USER'

def makePhoneTable(cur):
	sql = '''CREATE TABLE PHONE (
		Email			TEXT		NOT NULL,
		Area_code		TEXT		NOT NULL,
		Phone_number	TEXT		NOT NULL
		);'''
	cur.execute(sql)
	return 'PHONE'

def makeAdminTable(cur):
	sql = '''CREATE TABLE ADMIN (
		Admin_ID		INTEGER		NOT NULL,
		Password		TEXT		NOT NULL	
		);'''
	cur.execute(sql)
	return 'ADMIN'

def makeReportTable(cur):
	sql = '''CREATE TABLE REPORT (
		User_email			TEXT		NOT NULL,
		Reported_user_email	TEXT		NOT NULL,
		Admin_ID			TEXT,
		Offense_description	TEXT,
		Date_of_offense		TEXT		NOT NULL,
		Date_of_report		TEXT		NOT NULL	
		);'''
	cur.execute(sql)
	return 'REPORT'

def makeCategoryTable(cur):
	sql = '''CREATE TABLE CATEGORY (
		Name			TEXT		NOT NULL,
		Parent			TEXT	
		);'''
	cur.execute(sql)
	return 'CATEGORY'

def makeItemTable(cur):
	sql = '''CREATE TABLE ITEM (
		Title			TEXT,
		Category_name	TEXT,
		Owner_email		TEXT,
		Description		TEXT,
		Daily_rate		INTEGER	
		);'''
	cur.execute(sql)
	return 'ITEM'

def makeItem_BlackoutTable(cur):
	sql = '''CREATE TABLE ITEM_BLACKOUT (
		Title			TEXT,
		Owner_email		TEXT,
		Start_date		TEXT,
		End_date		TEXT
		);'''
	cur.execute(sql)
	return 'ITEM_BLACKOUT'

def makeRentalTable(cur):
	sql = '''CREATE TABLE RENTAL (
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
		);'''
	cur.execute(sql)
	return 'RENTAL'

def makeInterested_InTable(cur):
	sql = '''CREATE TABLE INTERESTED_IN (
		User_email		TEXT		NOT NULL,
		Category_name	TEXT		NOT NULL
		);'''
	cur.execute(sql)
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
	msg(makeRentalTable(cur))
	msg(makeInterested_InTable(cur))
	con.commit()
	con.close()
