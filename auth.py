import functools
import sqlite3

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from db import get_db, close_db

from forms import RegisterForm, LoginForm

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.before_app_request
def load_logged_in_user():
    # session['user_id'] is set by Login() and passed on before every
    # app request until the user logs out.
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:  
        g.user = get_db().execute(
            'SELECT * FROM user WHERE email = ?', (user_id,)
        ).fetchone()

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            flash("Please login or sign up to continue", "primary")
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view

# Register
#   Register page for creating new user accounts.
#
# GET
#   http://127.0.0.1:5000/auth/register
#   Renders 'register.html' which prompts the user to enter details for account creation.
#
# POST
#   http://127.0.0.1:5000/auth/register
#   Creates a new user with the values from the registration form:
#       - Insert into USER values from registration form:
#         (
#           Email,
#           Password (hashed),
#           First_name,
#           Last_name,
#           DoB,
#           Street_address,
#           City,
#           Province,
#           Postal Code
#         )
#           If INSERT fails:
#           - Flash warning that user already exists with email.
#           - Reload 'register.html'
#       - Redirect to Login
@bp.route('/register', methods=('GET', 'POST'))
def register():
    form = RegisterForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            db = get_db()
            cur = db.cursor()
            try:
                registration = cur.execute('INSERT INTO USER (Email, Password, First_name, Last_name, DoB,Street_address ,City,Province, Postal_code) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', (form.email.data, generate_password_hash(form.password.data), form.fname.data, form.lname.data, form.dob.data, form.street.data, form.city.data, form.province.data, form.postalCode.data))
                db.commit()
                return redirect(url_for('auth.login'))
            except sqlite3.IntegrityError:
                flash('Username already in use', 'warning')
        else:
            flash('Please enter the appropriate information in the fields. Make sure Date of Birth is in the form yyyy-mm-dd.', 'error')
    return render_template('register.html', form=form)

# Login
#   Logs in a user.
#
# GET
#   http://127.0.0.1:5000/auth/login
#   Renders 'login.html' which prompts the user to enter their email & password
#
# POST
#   http://127.0.0.1:5000/auth/login
#   Logs in the user with the values from the login form:
#       - Select from USER where form['email'] = USER.Email
#           If query result is empty:
#           - Flash warning that email is incorrect
#           - Reload 'login.html'
#       - Checks the password hash from the form against the one belonging to the user tuple
#           If password hashes don't match:
#           - Flash warning that the password is incorrect
#           - Reload 'login.html'
#       - Update session['user_id'] to this user (this logs the user in)
#       - Redirect to Home
@bp.route('/login', methods=('GET', 'POST'))
def login():
    #login
    form = LoginForm()
    # POST: login form submission
    if request.method == 'POST':
        if form.validate_on_submit():
            username = request.form['email']
            # connect to db
            db = get_db()
            cur = db.cursor()
            error = None

            # Find matching user
            user = cur.execute('SELECT * FROM USER WHERE Email=?', (username,)).fetchone()

            if user is None:
                error = 'Incorrect username.'
            elif not check_password_hash(user['Password'], request.form['password']):
                error = 'Incorrect passsword.'

            if error is None:
                session.clear() # remove any session data
                session['user_id'] = user['Email'] # set session['user_id'] to logged in user
                return redirect(url_for('home'))
            else:
                flash(error,'warning') # flash warning, and re-display login page
    # GET: display login page
    return render_template('login.html', form=form)

# Logout
#   Logs out the active user.
#
# GET
#   http://127.0.0.1:5000/auth/logout
#   Logs out the user:
#       - Clears the session data (this logs the user out)
#       - Closes the db connection
#       - Redirects to Home
@bp.route('/logout')
def logout():
    session.clear()
    close_db()
    return redirect(url_for('home'))
