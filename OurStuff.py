import sqlite3, flask
from flask import jsonify, render_template, redirect, url_for, request, flash
from forms import LoginForm, UserInfoForm
from forms import registerForm
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
    form = registerForm()
    if form.validate_on_submit():
        con = sqlite3.connect('ourStuff.db')
        cur = con.cursor()
        registration = cur.execute('INSERT INTO USER (Email, Password, First_name, Last_name, DoB,Street_address ,City,Province, Postal_code) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', (form.email.data, form.password.data, form.fname.data, form.lname.data, form.dob.data, form.street.data, form.city.data, form.province.data, form.postalCode.data))
        con.commit()
        cur.close()
        if registration:
            return redirect(url_for('login'))
        else:
            flash('Please enter the appropriate information in the fields. Make sure Date of Birth is in the form yyyy-mm-dd.', 'danger')
    else:
        return render_template('register.html', form=form)


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
            flash('Incorrect username or password. Please try again.', 'danger')
    return render_template('login.html', form=form)

# view all items
@app.route('/browse/all', methods=['GET'])
def view_all():
    # Load all items from DB, then pass to browse.html file to display
    con = sqlite3.connect('ourStuff.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM ITEM")
    data = cur.fetchall() #an array of all items fetched from DB
    return render_template('browse.html', data=data) #show the data in the html

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

    # once flask-login is setup, send current_user to html page instead....if user not logged in then redirect to login
    con = sqlite3.connect('ourStuff.db')
    cur = con.cursor()
    user = cur.execute('SELECT * FROM USER WHERE Email=?', ('madhuselvaraj24@gmail.com',)).fetchone() #just temporary, once flask-login is setup don't need to query DB
    return render_template('profile.html', user=user)

@app.route('/user/<username>/edit', methods=['GET', 'POST'])
def editProfile(username):
    form = UserInfoForm()
    con = sqlite3.connect('ourStuff.db')
    cur = con.cursor()
    user = cur.execute('SELECT * FROM USER WHERE Email=?', ('madhuselvaraj24@gmail.com',)).fetchone() #temporary until flask-login is setup

    # TODO: add validators to each of the form fields, then finish populating the form with the current_user's information
    if form.validate_on_submit():
        sql = '''UPDATE USER SET Street_address = form.street.data WHERE Email='madhuselvaraj24@gmail.com' '''
        cur.execute(sql)
        cur.close()
        return redirect(url_for('profile', username='user[2]-user[3]'))
    elif request.method=='GET': #populates the form with the current_user's information
        form.email.data = user[0] #later do current_user.emai

    return render_template('editProfile.html', form=form, user=user) #later user=current_user

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
