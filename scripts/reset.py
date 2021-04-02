import sqlite3
import os

# Reset the database.
# 	1. Delete
# 	2. Declare
# 	3. Populate
#	4. Commit
def reset():
	if os.path.exists("ourStuff.db"):
		os.remove("OurStuff.db")
	
	# Connect to the db (which creates it)
	con = sqlite3.connect("OurStuff.db")
	cur = con.cursor()

	# Run create db script
	script = open("scripts/create_db.sql")
	sql_script = script.read()
	cur.executescript(sql_script)
	script.close()

	# Run populate db script
	script = open("scripts/populate_db.sql")
	sql_script = script.read()
	cur.executescript(sql_script)
	script.close()	

	# Commit the changes
	con.commit()
	con.close()

	print("OurStuff.db has been reset.")
	return 0

if __name__ == '__main__':
	reset()
