import functools
import sqlite3

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from db import get_db, close_db

from forms import LoginForm

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.before_app_request
def load_logged_in_admin():
    admin = session.get('admin')

    if admin is None:
        g.admin = None
    else:
        g.admin = get_db().execute(
            'SELECT * FROM ADMIN WHERE Admin_ID = ?', (admin,)
        ).fetchone()

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.admin is None:
            flash('Please login to continue', 'primary')
            return redirect(url_for('admin.login'))
        return view(**kwargs)
    return wrapped_view

@bp.route('/login', methods=('GET','POST'))
def login():
    # admin login
    form = LoginForm()
    if request.method == 'POST':
        Admin_ID = request.form['email']
        
        # connect to db
        db = get_db()
        cur = db.cursor()
        error = None
        
        # Find matching admin
        admin = cur.execute('SELECT * FROM ADMIN WHERE Admin_ID=?', (Admin_ID,)).fetchone()

        if admin is None:
            error = 'Incorrect id.'
        elif not check_password_hash(admin['Password'], request.form['password']):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['admin'] = admin['Admin_ID']
            print(session['admin'])
            return redirect(url_for('admin.view_reports'))
        else:
            flash(error, 'warning')
    return render_template('admin_login.html', form=form)

@bp.route('/logout')
def logout():
    # admin logout
    session.clear()
    close_db()
    return redirect(url_for('home'))

@bp.route('/reports', methods=('GET','POST'))
@login_required
def view_reports():
    db = get_db()
    cur = db.cursor()

    recent = cur.execute(
        'SELECT * FROM REPORT WHERE (Admin_ID) IS NULL ORDER BY (Date_of_report)'
    ).fetchall()

    resolved = cur.execute(
        'SELECT * FROM REPORT WHERE (Admin_ID) IS NOT NULL ORDER BY (Date_of_report)'
    ).fetchall()
    
    return render_template('admin_reports.html', len1=len(recent), len2=len(resolved), recent=recent, resolved=resolved)
    
@bp.route('/reports/resolve/<user_email>/<reported_user_email>/<date_of_offense>')
@login_required
def resolve_report(user_email,reported_user_email,date_of_offense):
    db = get_db()
    cur = db.cursor()

    cur.execute(
        'UPDATE REPORT SET Admin_ID = ? WHERE User_email = ? AND Reported_user_email = ? AND Date_of_offense = ?',
        (g.admin['Admin_ID'], user_email, reported_user_email, date_of_offense)
    )
    
    db.commit()
    cur.close()

    return redirect(url_for('admin.view_reports'))
