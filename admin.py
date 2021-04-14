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


# View Reports
#   Displays all user reports (where one user has reported another for an offense).
#   Admin's can resolve a report which moves it from the Recent reports section to the Resolved reports section
#
# GET
#   http://127.0.0.1:5000/admin/reports
#   Displays all reports:
#       Recent reports:
#           - Select from REPORT where Admin_ID is NULL
#       Resolved reports:
#           - Select from REPORT where Admin_ID is not NULL
@bp.route('/reports')
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

# Resolve Report
#   Resolves a report by updating its Admin_ID to the ID of the admin who resolved it.
#
# POST
#   http://127.0.0.1:5000/reports/resolve/<user_email>/<reported_user_email>/<date_of_offense>
#   Updates the report with the primary key (user_email, reported_user_email, date_of_offense)
#   with the Admin_ID of the logged in Admin
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
    
# Login
#   Logs in a user.
#
# GET
#   http://127.0.0.1:5000/admin/
#   http://127.0.0.1:5000/admin/login
#   Renders 'admin_login.html' which prompts the user to enter their admin_id & password
#
# POST
#   http://127.0.0.1:5000/admin/login
#   Logs in the user with the values from the login form:
#       - Select from ADMIN where form['Admin_ID'] = ADMIN.Admin_ID
#           If query result is empty:
#           - Flash warning that email is incorrect
#           - Reload 'admin_login.html'
#       - Check password hashes
#           If password hashes don't match:
#           - Flash warning that the password is incorrect
#           - Reload 'admin_login.html'
#       - Update session['admin'] to this admin (this logs the admin in)
#       - Redirect to 'admin.view_reports'
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

# Logout
#   Logs out the active administrator.
#
# GET
#   http://127.0.0.1:5000/admin/logout
#   Logs out the administrator:
#       - Clears the session data (this logs the user out)
#       - Closes the db connection
#       - Redirects to Home
@bp.route('/logout')
def logout():
    session.clear()
    close_db()
    return redirect(url_for('home'))
