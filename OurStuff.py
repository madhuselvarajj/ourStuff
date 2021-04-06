import sqlite3, flask
from flask import jsonify, render_template, redirect, url_for, request, flash
from forms import LoginForm, UserInfoForm
from forms import registerForm
from datetime import datetime
from forms import filterForm

# redirect and url_for can be used to call different routes, ex: redirect(url_for('function_name'))

filer_item = "" #define the global variable used in multiple functions below

# define database name
db = "ourStuff.db"

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
        con = sqlite3.connect(db)
        cur = con.cursor()
        registration = cur.execute('INSERT INTO USER (Email, Password, First_name, Last_name, DoB,Street_address ,City,Province, Postal_code) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', (form.email.data, form.password.data, form.fname.data, form.lname.data, form.dob.data, form.street.data, form.city.data, form.province.data, form.postalCode.data))
        con.commit()
        cur.close()
        if registration:
            return redirect(url_for('login'))
        else:
            flash('Please enter the appropriate information in the fields. Make sure Date of Birth is in the form yyyy-mm-dd.', 'error')
    else:
        return render_template('register.html', form=form)

    # if GET, return a html form for user to sign up
    # if POST, save user information in DB and return a redirect to login

    # POST if user presses submit, before they press submit its a GET request

#login
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        #look for user in db with matching email + password
        con = sqlite3.connect(db)
        cur = con.cursor()
        user = cur.execute('SELECT * FROM USER WHERE Email=? AND Password=?', (form.email.data, form.password.data,)).fetchone()
        loggedInUser = form.email.data
        loggedInPass = form.password.data

        #if login successful redirect to home page....else stay on login page
        if user:
            return redirect(url_for('home'))
        else:
            flash('Incorrect username or password. Please try again.', 'error')
    return render_template('login.html', form=form)

# view all items
@app.route('/browse/all', methods=['GET', 'POST'])
def view_all():
    # Load all items from DB, then pass to browse.html file to display
    #use the global variable filter_item
    form = filterForm()
    con = sqlite3.connect(db)
    cur = con.cursor()
    if form.validate_on_submit():
        if (form.category.data != 'none' and form.city.data != 'none' and form.maxPrice.data != 'none'):
            cur.execute("SELECT * FROM ITEM, USER WHERE USER.Email = ITEM.Owner_email AND Category_name=? AND Daily_rate<=? AND USER.City =?", (form.category.data, form.maxPrice.data, form.city.data))
        elif (form.category.data != 'none' and form.city.data != 'none'):
            cur.execute("SELECT * FROM ITEM, USER WHERE Category_name=? AND USER.Email = ITEM.Owner_email AND USER.City =?", (form.category.data, form.city.data))

        elif (form.category.data != 'none' and form.maxPrice.data != 'none'):
            cur.execute("SELECT * FROM ITEM WHERE Category_name=? AND Daily_rate<=?", (form.category.data, form.maxPrice.data))

        elif (form.maxPrice.data != 'none' and form.city.data != 'none'):
            cur.execute("SELECT * FROM ITEM, USER WHERE Daily_rate<=? AND USER.Email = ITEM.Owner_email AND USER.City =?", (form.maxPrice.data, form.city.data))

        elif (form.category.data != 'none'):
            cur.execute("SELECT * FROM ITEM WHERE Category_name=?", (form.category.data,))

        elif (form.city.data != 'none'):
            cur.execute("SELECT * FROM ITEM, USER WHERE USER.Email = ITEM.Owner_email AND USER.City =?", (form.city.data,))

        elif (form.maxPrice.data != 'none'):
            cur.execute("SELECT * FROM ITEM WHERE Daily_rate<=?", (form.maxPrice.data,))

        else:
            cur.execute("SELECT * FROM ITEM")

    else:
        cur.execute("SELECT * FROM ITEM")
    if request.method == 'GET':
        cur.execute("SELECT * FROM ITEM")
    data = cur.fetchall() #an array of all items fetched from DB
    return render_template('browse.html', data=data, form=form) #show the data in the html

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
@app.route('/profile', methods=['GET'])
def profile():
    # TODO: once flask-login is setup, first check if current_user is logged in (redirect to login if not)
    con = sqlite3.connect('ourStuff.db')
    cur = con.cursor()
    user = cur.execute('SELECT * FROM USER WHERE Email=?', ('madhuselvaraj24@gmail.com',)).fetchone() #just temporary, once flask-login is setup don't need to query DB
    return render_template('profile.html', user=user)

@app.route('/profile/edit', methods=['GET', 'POST'])
def editProfile():
    form = UserInfoForm()
    con = sqlite3.connect('ourStuff.db')
    cur = con.cursor()
    user = cur.execute('SELECT * FROM USER WHERE Email=?', ('madhuselvaraj24@gmail.com',)).fetchone() #temporary until flask-login is setup

    # TODO: once flask-login is setup, change everything to current_user
    if form.validate_on_submit():
        cur.execute('UPDATE USER SET Email=?, Password=?, First_name=?, Last_name=?, Dob=?, Owner=0, Renter=0, Street_address =?, City=?, Province=?, Postal_code=? WHERE Email=?',(form.email.data, form.password.data, form.fname.data, form.lname.data, form.dob.data, form.street.data, form.city.data, form.province.data, form.postalCode.data, 'madhuselvaraj24@gmail.com',))
        con.commit()
        cur.close()
        return redirect(url_for('profile'))
    elif request.method=='GET': #populates the form with the current_user's information
        form.email.data = user[0] #later do current_user.email
        form.password.data = user[1]
        form.fname.data = user[2]
        form.lname.data = user[3]
        form.dob.data = datetime.strptime(user[4], '%Y-%m-%d')
        form.street.data = user[7]
        form.city.data = user[8]
        form.province.data = user[9]
        form.postalCode.data = user[10]

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
    con = sqlite3.connect(db)
    cur = con.cursor()
    users = cur.execute('SELECT * FROM USER;').fetchall()
    return jsonify(users)

app.run()
