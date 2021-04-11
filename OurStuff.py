import sqlite3, flask
from flask import jsonify, render_template, redirect, url_for, request, flash, g
from forms import LoginForm, UserInfoForm, FilterForm, RentalRequestForm, ReportForm
from datetime import datetime, timedelta, date
import auth
from auth import login_required, get_db
import admin

# create the app
# TODO: make a create_app function
app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config['SECRET_KEY'] = 'a722544382860619226245081983ab8f' #needed to use flask_wtforms
app.register_blueprint(auth.bp)
app.register_blueprint(admin.bp)

# home page
@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
def home():
    return render_template('home.html')

# view all items
@app.route('/browse/all', methods=['GET', 'POST'])
def view_all():
    # Load all items from DB, then pass to browse.html file to display
    #use the global variable filter_item
    form = FilterForm()

    # connect to db
    db = get_db()
    cur = db.cursor()

    # TODO: remove default none parameter. may be able to condense to a single sql statement?
    if request.method == 'POST' and form.validate_on_submit():
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
    data = cur.fetchall() #an array of all items fetched from DB
    return render_template('browse.html', data=data, form=form) #show the data in the html

# user requests to rent item
# not sure if route is correct
@app.route('/browse/item/rent/<string:title>', methods=['GET', 'POST'])
@login_required
def rent_item(title):
    form = RentalRequestForm()
    if request.method == 'POST':
        # if GET, return a html form for user to enter their transaction + rental information
        # if POST, create a transaction entry in DB using user information -> then redirect back to home page
        if form.validate_on_submit():
            start = form.startDate.data
            duration = form.duration.data
            pickup = form.pickup.data
            dropoff = form.dropoff.data
            #connect to the database so we can add a new entry
            db = get_db()
            cur = db.cursor()
            #get the relevant information about this item
            item = cur.execute("SELECT * FROM ITEM WHERE Title=?", (title,)).fetchone()
            #title is probably not returning anything!
            #return an error message if nobody is logged in at the moment
            if (g.user is None):
                flash('Please login or register for an account if you would like to rent this item', 'success')
                return render_template('rentItem.html', title=title, form=form) #render the home page again or a confirmation page

            cur.execute("INSERT INTO RENTAL (Renter_email, Owner_email, Item_title, Start_date, Duration, Pick_up_time, Drop_off_time, Type) VALUES (?,?,?,?,?,?,?,?)", (g.user['Email'], item[2], item[0], start, duration, pickup, dropoff, "PENDING"))
            db.commit()
            flash('The rental request has been submitted successfully.', 'success')
        return redirect(url_for('home'))
    return render_template('rentItem.html', title=title, form=form) #render the home page again or a confirmation page

# view profile (where user can view their transactions and items)
@app.route('/profile', methods=['GET'])
@login_required
def profile():
    db = get_db()
    cur = db.cursor()

    # get the number of items rented out, items borrowed, items posted, and interests
    owner_rentals = cur.execute('SELECT COUNT (*) FROM RENTAL WHERE Owner_email=?', (g.user['Email'],))
    num_owner_rentals = cur.fetchone()[0]
    renter_rentals = cur.execute('SELECT COUNT (*) FROM RENTAL WHERE Renter_email=?', (g.user['Email'],))
    num_renter_rentals = cur.fetchone()[0]
    all_items = cur.execute('SELECT COUNT (*) FROM ITEM WHERE Owner_email=?', (g.user['Email'],))
    num_items = cur.fetchone()[0]
    interests = cur.execute('SELECT * FROM INTERESTED_IN WHERE User_email=?', (g.user['Email'],)).fetchall()
    all_interests = ""

    if interests:
        for i in interests:
            all_interests += i[1] + ", "
        return render_template('profile.html', o_rentals = num_owner_rentals, r_rentals = num_renter_rentals, items = num_items, interests = all_interests[:-2])
    else:
        return render_template('profile.html', o_rentals = num_owner_rentals, items = num_items, r_rentals = num_renter_rentals, itmes = num_items)

# updates profile information
@app.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def editProfile():
    form = UserInfoForm()
    db = get_db()
    cur = db.cursor()
    user = cur.execute('SELECT * FROM USER WHERE Email=?', (g.user['Email'],)).fetchone()

    if form.validate_on_submit():
        cur.execute('UPDATE USER SET Email=?, First_name=?, Last_name=?, Dob=?, Street_address =?, City=?, Province=?, Postal_code=? WHERE Email=?',(form.email.data, form.fname.data, form.lname.data, form.dob.data, form.street.data, form.city.data, form.province.data, form.postalCode.data, g.user['Email'],))
        db.commit()
        cur.close()
        return redirect(url_for('profile'))
    elif request.method=='GET': #populates the form with the current_user's information
        form.email.data = user[0]
        form.fname.data = user[2]
        form.lname.data = user[3]
        form.dob.data = datetime.strptime(user[4], '%Y-%m-%d')
        form.street.data = user[5]
        form.city.data = user[6]
        form.province.data = user[7]
        form.postalCode.data = user[8]

    return render_template('editProfile.html', form=form, user=user)

# determines the number of days remaining in each booked rental
def determineDaysRemaining(booked):
    days_remaining=[]
    for r in booked:
        start = datetime.strptime(r[4], '%Y-%m-%d')
        today = datetime.now()
        diff = today - start
        remaining = r[5] - diff.days
        days_remaining.append(remaining)
    return days_remaining

# view all renter transactions
@app.route('/profile/renter/transactions/all', methods = ['GET', 'POST'])
@login_required
def renterTransactions():
    db = get_db()
    cur = db.cursor()
    pending = cur.execute('SELECT * FROM RENTAL WHERE Renter_email=? AND Type=?', (g.user['Email'],'pending',)).fetchall() #owner hasn't approved yet
    booked = cur.execute('SELECT * FROM RENTAL WHERE Renter_email=? AND Type=?', (g.user['Email'],'booked',)).fetchall() #active rental
    days_remaining = determineDaysRemaining(booked)
    complete = cur.execute('SELECT * FROM RENTAL WHERE Renter_email=? AND Type=?', (g.user['Email'],'complete',)).fetchall() #completed rental (item returned)

    if request.method == 'GET':
        if pending and booked and complete:
            return render_template('renterTransactions.html', pending = pending, booked = booked, days_remaining = days_remaining, complete = complete, zip=zip)
        elif pending and booked:
            return render_template('renterTransactions.html', pending = pending, booked = booked, days_remaining = days_remaining, zip=zip)
        elif pending and complete:
            return render_template('renterTransactions.html', pending = pending, complete = complete)
        elif booked and complete:
            return render_template('renterTransactions.html', booked = booked, days_remaining = days_remaining, complete = complete, zip=zip)
        elif pending:
            return render_template('renterTransactions.html', pending = pending)
        elif booked:
            return render_template('renterTransactions.html', booked = booked, days_remaining = days_remaining, zip=zip)
        elif complete:
            return render_template('renterTransactions.html', complete = complete)
        else:
            return render_template('renterTransactions.html')

    elif request.method == 'POST':
        #stores either the user's rating or review
        rate = request.args.get('rate')
        if complete and rate == '1' and request.form['ratingBtn'] is not None:
            cur.execute('UPDATE RENTAL SET Rating=? WHERE tID=?',(int(request.form['rating']),request.form['ratingBtn']))
        elif complete and rate == '0' and request.form['reviewBtn'] is not None:
            cur.execute('UPDATE RENTAL SET Review=? WHERE tID=?',(request.form['review'],request.form['reviewBtn']))

        db.commit()
        cur.close()
        return redirect(url_for('renterTransactions'))

#request a report on another user where the transaction was with tID
@app.route('/profile/renter/report/<ownerEmail>', methods = ['GET', 'POST'])
@login_required
def report(ownerEmail):
    form = ReportForm()
    if request.method == 'GET':
        return render_template('report.html', form=form)
    elif request.method == 'POST':
        description = form.description.data
        date = form.dateOfOffense.data
        todaysDate = datetime.date(datetime.now())
        db = get_db()
        cur = db.cursor()
        cur.execute("INSERT INTO REPORT (User_email, Reported_user_email, Admin_ID, Offense_description, Date_of_offense, Date_of_report) VALUES (?,?,?,?,?,?)", (g.user['Email'], ownerEmail, None, description, date, todaysDate))
        return redirect(url_for('renterTransactions'))

# view all owner transactions
@app.route('/profile/owner/transactions/all', methods = ['GET', 'POST'])
@login_required
def ownerTransactions():
    db = get_db()
    cur = db.cursor()
    pending = cur.execute('SELECT * FROM RENTAL WHERE Owner_email=? AND Type=?', (g.user['Email'],'pending',)).fetchall() #need to approve
    booked = cur.execute('SELECT * FROM RENTAL WHERE Owner_email=? AND Type=?', (g.user['Email'],'booked',)).fetchall() #active rental
    days_remaining = determineDaysRemaining(booked)
    complete = cur.execute('SELECT * FROM RENTAL WHERE Owner_email=? AND Type=?', (g.user['Email'],'complete',)).fetchall() #item returned

    if request.method=='GET':
        if pending and booked and complete:
            return render_template('ownerTransactions.html', pending = pending, booked = booked, days_remaining = days_remaining, complete = complete, zip=zip)
        elif pending and booked:
            return render_template('ownerTransactions.html', pending = pending, booked = booked, days_remaining = days_remaining, zip=zip)
        elif pending and complete:
            return render_template('ownerTransactions.html', pending = pending, complete = complete)
        elif booked and complete:
            return render_template('ownerTransactions.html', booked = booked, complete = complete, days_remaining = days_remaining, zip=zip)
        elif pending:
            return render_template('ownerTransactions.html', pending = pending)
        elif booked:
            return render_template('ownerTransactions.html', booked = booked, days_remaining = days_remaining, zip=zip)
        elif complete:
            return render_template('ownerTransactions.html', complete = complete)
        else:
            return render_template('ownerTransactions.html')

    elif request.method == 'POST':
        # updates a pending rental to booked, or a booked rental to complete
        if pending and request.form['approveBtn'] is not None:
            cur.execute('UPDATE RENTAL SET Type=? WHERE tID=?',('booked',request.form['approveBtn']))
        elif booked and request.form['completeBtn'] is not None:
            cur.execute('UPDATE RENTAL SET Type=? WHERE tID=?',('complete',request.form['completeBtn']))
        db.commit()
        cur.close()
        return redirect(url_for('ownerTransactions'))


# view all owner's items, can choose to black out dates or delete
@app.route('/profile/items/all', methods = ['GET', 'POST', 'DELETE'])
@login_required
def ownerItems():
    db = get_db()
    cur = db.cursor()
    all_items = cur.execute('SELECT * FROM ITEM WHERE Owner_email=?', (g.user['Email'],)).fetchall()
    blackouts = cur.execute('SELECT * FROM ITEM_BLACKOUT WHERE Owner_email=?', (g.user['Email'],)).fetchall()
    if blackouts:
        return render_template('items.html', items=all_items, blackouts=blackouts, zip=zip)
    else:
        return render_template('items.html', items=all_items)
    # return render_template()
    # if request.method == "GET" :
    #     return render_template()
    # elif request.method == "POST":
    #     start_black_out = request.form["start"]
    #     end_black_out = request.form["end"] #now just update blackout dates in the backend
    #     return render_template()
    # else :
    #     return render_template() #deletion


@app.route('/users',methods=['GET'])
def sampleQuery1():
    con = sqlite3.connect(db)
    cur = con.cursor()
    users = cur.execute('SELECT * FROM USER;').fetchall()
    return jsonify(users)

app.run()
