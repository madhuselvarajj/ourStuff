# Reinitializes the Our Stuff db by deleting ourStuff.db, creating a new database and finally populating it with fake data
import createDB, populateDB
import os

def clean():
	if os.path.exists("ourStuff.db"):
		print("Cleaning...")
		os.remove("ourStuff.db")
	else:
		print("ourStuff.db does not exist.")
	createDB.create()
	populateDB.populate()

if __name__ == '__main__':
	clean()
