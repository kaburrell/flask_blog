# blog.py
# Controller

from flask import Flask, render_template, request, session, flash, redirect, url_for, g

import sqlite3
from functools import wraps



# configuration
# IN-LINE configuration, config will look inside THIS file for config parameters, config variables MUST be UPPERCASE
DATABASE = 'db/blog.sqlite3'
USERNAME = 'admin'
PASSWORD = 'admin'
SECRET_KEY = 'admin'



app = Flask(__name__)

# get config variables
# stores ALL uppercase variables found in this script a config variables
# a quick and easy config mechanism
app.config.from_object(__name__)



"""checks to make sure that a user is authorized/logged_in
before allowing access to certain pages.
This function which will be used to restrict access to main.html.

USES: functools
a Python module for higher order functions
extends the capabilities of functions with other functions
login_required() is used as a function decorator that we can use to wrap
other functions when a login check is needed

"""
def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You MUST login first!')
            return redirect(url_for('login'))
    return wrap

# get database connection
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

# ---------------------
# link routes to views
# ---------------------

# validate login
# automatically force a login when access the web app
# note: http://localhost:5000/main will BYPASS loginn
# address this in the next version
@app.route('/', methods=['GET', 'POST'] )
def login():
    error = None
    if request.method =='POST':
        if request.form['username'] != app.config['USERNAME'] or request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid Credentials . Please try again'
        else:
            session['logged_in'] = True
            return redirect(url_for('main'))

    return render_template('login.html', error=error)


# cleanup after logging out
# Logout is a link on the main page
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('login'))


@app.route('/add', methods=['POST'])
@login_required
def add():
    title = request.form['title']
    post = request.form['post']
    if not title or not post:
        flash("All fields are required. Please try again.")
        return redirect(url_for('main'))
    else:
        g.db = connect_db()
        g.db.execute('insert into posts (title, post) values (?,?)', [request.form['title'], request.form['post']])
    g.db.commit()
    g.db.close()
    flash('New entry was successfully posted!')
    return redirect(url_for('main'))




# login_required() will restrict access to the main page
# fixes the unauthorized access to main page if not logged in
@app.route('/main')
@login_required
def main():
    g.db = connect_db()
    cur = g.db.execute('select * from posts')
    posts = [dict(title=row[0], post=row[1]) for row in cur.fetchall()]
    g.db.close()

    return render_template('main.html', posts=posts)


if __name__  == '__main__':
    app.run(debug=True)
