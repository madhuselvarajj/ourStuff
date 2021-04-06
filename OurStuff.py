import sqlite3, flask
from flask import jsonify, render_template, redirect, url_for, request, flash
from forms import LoginForm, UserInfoForm
from forms import registerForm
from datetime import datetime
from forms import filterForm

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
            flash('Login Successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Incorrect username or password. Please try again.', 'danger')

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
    con = sqlite3.connect(db)
    cur = con.cursor()
    user = cur.execute('SELECT * FROM USER WHERE Email=?', ('madhuselvaraj24@gmail.com',)).fetchone() #just temporary, once flask-login is setup don't need to query DB
    owner_rentals = cur.execute('SELECT COUNT (*) FROM RENTAL WHERE Owner_email=?', ('madhuselvaraj24@gmail.com',)) #after flask-login is setup, check if owner_email = current_user.email
    num_owner_rentals = cur.fetchone()[0]
    renter_rentals = cur.execute('SELECT COUNT (*) FROM RENTAL WHERE Renter_email=?', ('madhuselvaraj24@gmail.com',))
    num_renter_rentals = cur.fetchone()[0]
    interests = cur.execute('SELECT * FROM INTERESTED_IN WHERE User_email=?', ('madhuselvaraj24@gmail.com',)).fetchall()
    all_interests = ""
    if interests:
        for i in interests:
            all_interests += i[1] + ", "
        return render_template('profile.html', user=user, o_rentals = num_owner_rentals, r_rentals = num_renter_rentals, interests = all_interests[:-2])
    else:
        return render_template('profile.html', user=user, o_rentals = num_owner_rentals, r_rentals = num_renter_rentals)

@app.route('/profile/edit', methods=['GET', 'POST'])
def editProfile():
    form = UserInfoForm()
    con = sqlite3.connect(db)
    cur = con.cursor()
    user = cur.execute('SELECT * FROM USER WHERE Email=?', ('madhuselvaraj24@gmail.com',)).fetchone() #temporary until flask-login is setup

    # TODO: once flask-login is setup, change everything to current_user
    if form.validate_on_submit():
        cur.execute('UPDATE USER SET Email=?, Password=?, First_name=?, Last_name=?, Dob=?, Street_address =?, City=?, Province=?, Postal_code=? WHERE Email=?',(form.email.data, form.password.data, form.fname.data, form.lname.data, form.dob.data, form.street.data, form.city.data, form.province.data, form.postalCode.data, 'madhuselvaraj24@gmail.com',))
        con.commit()
        cur.close()
        return redirect(url_for('profile'))
    elif request.method=='GET': #populates the form with the current_user's information
        form.email.data = user[0] #later do current_user.email
        form.password.data = user[1]
        form.fname.data = user[2]
        form.lname.data = user[3]
        form.dob.data = datetime.strptime(user[4], '%Y-%m-%d')
        form.street.data = user[5]
        form.city.data = user[6]
        form.province.data = user[7]
        form.postalCode.data = user[8]

    return render_template('editProfile.html', form=form, user=user) #later user=current_user

# view all renter transactions
@app.route('/profile/renter/transactions/all', methods = ['GET'])
def renterTransactions():
    con = sqlite3.connect(db)
    cur = con.cursor()
    #once flask-login is setup check for current_user.email instead
    pending = cur.execute('SELECT * FROM RENTAL WHERE Renter_email=? AND Type=?', ('madhuselvaraj24@gmail.com','pending',)).fetchall() #owner hasn't approved yet
    booked = cur.execute('SELECT * FROM RENTAL WHERE Renter_email=? AND Type=?', ('madhuselvaraj24@gmail.com','booked',)).fetchall() #active rental
    complete = cur.execute('SELECT * FROM RENTAL WHERE Renter_email=? AND Type=?', ('madhuselvaraj24@gmail.com','complete',)).fetchall() #completed rental (item returned)
    if pending and booked and complete:
        return render_template('renterTransactions.html', pending = pending, booked = booked, complete = complete)
    elif pending and booked:
        return render_template('renterTransactions.html', pending = pending, booked = booked)
    elif pending and complete:
        return render_template('renterTransactions.html', pending = pending, complete = complete)
    elif booked and complete:
        return render_template('renterTransactions.html', booked = booked, complete = complete)
    elif pending:
        return render_template('renterTransactions.html', pending = pending)
    elif booked:
        return render_template('renterTransactions.html', booked = booked)
    elif complete:
        return render_template('renterTransactions.html', complete = complete)
    else:
        return render_template('renterTransactions.html')

# view all owner transactions
@app.route('/profile/owner/transactions/all', methods = ['GET'])
def ownerTransactions():
    con = sqlite3.connect(db)
    cur = con.cursor()
    #once flask-login is setup check for current_user.email instead
    pending = cur.execute('SELECT * FROM RENTAL WHERE Owner_email=? AND Type=?', ('madhuselvaraj24@gmail.com','pending',)).fetchall() #need to approve
    booked = cur.execute('SELECT * FROM RENTAL WHERE Owner_email=? AND Type=?', ('madhuselvaraj24@gmail.com','booked',)).fetchall() #active rental
    complete = cur.execute('SELECT * FROM RENTAL WHERE Owner_email=? AND Type=?', ('madhuselvaraj24@gmail.com','complete',)).fetchall() #item returned
    if pending and booked and complete:
        return render_template('ownerTransactions.html', pending = pending, booked = booked, complete = complete)
    elif pending and booked:
        return render_template('ownerTransactions.html', pending = pending, booked = booked)
    elif pending and complete:
        return render_template('ownerTransactions.html', pending = pending, complete = complete)
    elif booked and complete:
        return render_template('ownerTransactions.html', booked = booked, complete = complete)
    elif pending:
        return render_template('ownerTransactions.html', pending = pending)
    elif booked:
        return render_template('ownerTransactions.html', booked = booked)
    elif complete:
        return render_template('ownerTransactions.html', complete = complete)
    else:
        return render_template('ownerTransactions.html')

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
