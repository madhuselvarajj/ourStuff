import sqlite3, flask
from flask import jsonify, render_template, redirect, url_for, request, flash
from forms import LoginForm
# redirect and url_for can be used to call different routes, ex: redirect(url_for('function_name'))

# create the app
app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config['SECRET_KEY'] = 'a722544382860619226245081983ab8f' #needed to use flask_wtforms


# home page
@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
def home():
    # temporary
    return render_template('home.html')


# register for account
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST" :
        #get all of the info to load into the database into variables for now
        #could do differently later on
        firstname = request.form["fname"]
        lname = request.form["lname"]
        password = request.form["pass"]
        email = request.form["email"]
        dob = request.form["DOB"]
        str = request.form["street"]
        city = request.form["city"]
        prov = request.form["province"]
        postal = request.form["postal"]
        return redirect(url_for('home'))


    else :
        return render_template('register.html')
    # if GET, return a html form for user to sign up
    # if POST, save user information in DB and return a redirect to login\home page

    # POST if user presses submit, before they press submit its a GET request

#login
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        #look for user in db with matching email + password
        con = sqlite3.connect('ourStuff.db')
        cur = con.cursor()
        user = cur.execute('SELECT * FROM USER WHERE Email=? AND Password=?', (form.email.data, form.password.data,)).fetchone()

        #if login successful redirect to home page....else stay on login page
        if user:
            return redirect(url_for('home'))
        else:
            flash('Incorrect username or password. Please try again.', 'error')
    return render_template('login.html', form=form)

# view all items
@app.route('/browse/all', methods=['GET'])
def view_all():
    # Load all items from DB, then pass to browse.html file to display
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
    # if POST, create a transaction entry in DB using user information -> then redirect back to home page
    if request.method == "GET" :
        return render_template() #render the template of the rental screen
    else :
        startRentalDate = request.form["start"]
        endRentalDate = request.form["end"]
        return render_template() #render the home page again or a confirmation page

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
    if request.method == "GET" :
        return render_template()
    else :
        return render_template(); #first change status of the transaction


# view all owner transactions
@app.route('/user/<username>/owner/transactions/all', methods = ['GET'])
def transactions(username):
    return render_template()

# filter owner transactions by pending, user can approve or reject
@app.route('/user/<username>/owner/transactions/pending', methods = ['GET', 'PUT'])
def pending_transactions(username):
    # if GET, find only pending transactions and display them
    # if PUT, change status of selected transaction, then reload page
    if request.method == "GET" :
        return render_template()
    else :
        return render_template()


# view all owner's items, can choose to black out dates or delete
@app.route('/user/<username>/owner/items/all', methods = ['GET', 'POST', 'DELETE'])
def owner_items(username):
    return render_template()
    if request.method == "GET" :
        return render_template()
    elif request.method == "POST":
        start_black_out = request.form["start"]
        end_black_out = request.form["end"] #now just update blackout dates in the backend
        return render_template()
    else :
        return render_template() #deletion


@app.route('/users',methods=['GET'])
def sampleQuery1():
    con = sqlite3.connect('ourStuff.db')
    cur = con.cursor()
    users = cur.execute('SELECT * FROM USER;').fetchall()
    return jsonify(users)

app.run()
