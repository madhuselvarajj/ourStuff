import sqlite3
import os

# declare db name
db = "ourStuff.db"

# Reset the database.
# 	1. Delete
# 	2. Declare
# 	3. Populate
#	4. Commit
def reset():
	if os.path.exists(db):
		os.remove(db)
	
	# Connect to the db (which creates it)
	con = sqlite3.connect(db)
	cur = con.cursor()

	# Run create db script
	script = open("scripts/create_db.sql")
	sql_create_script = script.read()
	cur.executescript(sql_create_script)
	script.close()

	# Run populate db script
	script = open("scripts/populate_db.sql")
	sql_populate_script = script.read()
	cur.executescript(sql_populate_script)
	script.close()	

	# Commit the changes
	con.commit()
	con.close()

	print("ourStuff.db has been reset.")
	return 0

if __name__ == '__main__':
	reset()
