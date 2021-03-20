import sqlite3, flask
from flask import jsonify, render_template, redirect, url_for
# redirect and url_for can be used to call different routes, ex: redirect(url_for('function_name'))

# create the app
app = flask.Flask(__name__)
# idk what this does
app.config["DEBUG"] = True


# home page
@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
def home():
    # temporary
    return render_template('home.html')


# register for account
@app.route('/register', methods=['GET', 'POST'])
def register():
    # if GET, return a html form for user to sign up
    # if POST, save user information in DB and return a redirect to login\home page

    # POST if user presses submit, before they press submit its a GET request
    return render_template() # remove later


# login
@app.route('/login', methods=['GET', 'POST'])
def login():
    # if GET, return a html form for user to log in
    # if POST, check if entered information is valid/is in the DB
        # if yes, redirect to profile page?
        # if no, display error message but don't redirect or return anything, user stays on login page

    return render_template() # temporary

# view all items
@app.route('/browse/all', methods=['GET'])
def view_all():
    # Load all items from DB, then pass to browse.html file to display?
    return render_template() #temporary

# filter item by city, category, price
# ex:  http://127.0.0.1:5000/browse/item?city=Calgary
# ex:  http://127.0.0.1:5000/browse/item?city=Calgary&category=sports+equipment
@app.route('/browse/item', methods=['GET'])
def filter_item():
    # store all request arguments in variables
    # query the DB based on these arguments
    # pass data to html file to display? ex: return render_template('browse.html', items = DB_items)

    return render_template() # temporary


# user requests to rent item
# not sure if route is correct
@app.route('/browse/item/rent', methods=['GET', 'POST'])
def rent_item():
    # if GET, return a html form for user to enter their transaction + rental information
    # if POST, create a transaction entry in DB using user information -> then redirect back to home page?
    return render_template()


# view profile (where user can view their transactions and items)
@app.route('/user/<username>', methods=['GET'])
def profile(username):
    # if user is not logged in , redirect(url_for(login))
    # load user information and display profile html page
    return render_template()

# view all renter transactions
@app.route('/user/<username>/renter/transactions/all', methods = ['GET'])
def rentals(username):
    # display all transactions user has rented
    return render_template()


# filter rental transactions by active, user can mark them as complete
@app.route('/user/<username>/renter/transactions/active', methods = ['GET', 'PUT'])
def active_rentals(username):
    # if GET, find only active rentals and display them
    # if PUT, change status of selected transaction to complete -> redirect to review page
    return render_template()

# view all owner transactions
@app.route('/user/<username>/owner/transactions/all', methods = ['GET'])
def transactions(username):
    return render_template()

# filter owner transactions by pending, user can approve or reject
@app.route('/user/<username>/owner/transactions/pending', methods = ['GET', 'PUT'])
def pending_transactions(username):
    # if GET, find only pending transactions and display them
    # if PUT, change status of selected transaction, then reload page?
    return render_template()

# view all owner's items, can choose to black out dates or delete
@app.route('/user/<username>/owner/items/all', methods = ['GET', 'POST', 'DELETE'])
def owner_items(username):
    return render_template()

# still need: writing reivews, reporting, adding new categories, and admin functionality

@app.route('/users',methods=['GET'])
def sampleQuery1():
    con = sqlite3.connect('ourStuff.db')
    cur = con.cursor()
    users = cur.execute('SELECT * FROM USER;').fetchall()
    return jsonify(users)

app.run()
