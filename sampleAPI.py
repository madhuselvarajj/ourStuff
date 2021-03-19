import sqlite3, flask
from flask import jsonify

# create the app
app = flask.Flask(__name__)
# idk what this does
app.config["DEBUG"] = True

@app.route('/',methods=['GET'])
def sampleQuery1():
    con = sqlite3.connect('ourStuff.db')
    cur = con.cursor()
    users = cur.execute('SELECT * FROM USER;').fetchall()
    return jsonify(users)

app.run()