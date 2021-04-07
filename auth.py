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
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE email = ?', (user_id,)
        ).fetchone()

def user_logged_in():
    return g.user is not None

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            flash("Please login or sign up to continue", "primary")
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view

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

    # if GET, return a html form for user to sign up
    # if POST, save user information in DB and return a redirect to login

    # POST if user presses submit, before they press submit its a GET request

@bp.route('/login', methods=('GET', 'POST'))
def login():
    #login
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            username = request.form['email']
            db = get_db()
            error = None

            user = db.execute('SELECT * FROM USER WHERE Email=?', (username,)).fetchone()

            if user is None:
                error = 'Incorrect username.'
            elif not check_password_hash(user['Password'], request.form['password']):
                error = 'Incorrect passsword.'

            if error is None:
                session.clear()
                session['user_id'] = user['Email']
                return redirect(url_for('home'))
            flash(error,'warning')
    return render_template('login.html', form=form)

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))
