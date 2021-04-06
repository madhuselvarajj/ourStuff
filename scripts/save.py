import sqlite3
import os

# define database name
db = "ourStuff.db"

def save():
    if os.path.exists(db):
        con = sqlite3.connect(db)
        cur = con.cursor()
    else:
        print("ourStuff.db not found.\nAborting save.")
        return

    f = open('./scripts/populate_db.sql','w')


    cur.execute('SELECT name FROM sqlite_master WHERE type= "table"')
    tables = cur.fetchall()

    for table in tables:
        # fetch all tuples from this table
        cur.execute(f'SELECT * FROM {table[0]}')
        results = cur.fetchall()

        # insertion statement for this table
        f.write(f'INSERT INTO {table[0]} VALUES')

        # write this table's tuples to the sql script
        first = True
        for row in results:
            if first: # no preceding tuple, begin first one
                f.write('\n\t(')
                first = False
            else: # finish preceding tuple, begin next one
                f.write('),\n\t(')

            # write all values of tuple to sql script (based on their type)
            first = True
            for e in row:
                if not first: # precede all values with a comma
                    f.write(', ')
                else: first = False # first value has no preceding comma

                if (isinstance(e, str)): # print string encapsulated with ""
                    f.write(f'"{e}"')
                else:
                    if e == None: # print None types as NULL
                        f.write('NULL')
                    else: # print value as is
                        f.write(f'{e}')
        f.write(');\n\n') # finish table insertion
    print("Database state saved in ./scripts/populate_db.sql")
    f.close()
    return

if __name__ == '__main__':
    save()