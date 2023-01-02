from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)

app.secret_key = 'your secret key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'EjirO251@'
app.config['MYSQL_DB'] = 'flaskapp'

mysql = MySQL(app)


@app.route('/')
@app.route('/landingpage')
def landingpage():
    return render_template('landingpage.html')
@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM speech WHERE username = % s AND password = % s', (username, password, ))
        user = cursor.fetchone()
        if user:
                session['loggedin'] = True
                session['userid'] = user['userid']
                userid = user['userid']
                session['username'] = user['username']
                msg = 'Logged in successfully !'
                return redirect(url_for('userprofile', userid=userid))
        else:
            msg = 'Please enter correct email / password !'
    return render_template('login.html', msg=msg)


@app.route("/userprofile", methods=['GET', 'POST'])
def userprofile():
    msg = ''
    if 'loggedin' in session:
        editUserId = request.args.get('userid')
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM speech WHERE userid = % s', (editUserId, ))
        editUser = cursor.fetchone()
        if request.method == 'POST' and 'username' in request.form and 'email' in request.form and 'fname' in request.form and 'lname' in request.form:
            username = request.form['username']
            fname = request.form['fname']
            email = request.form['email']
            lname = request.form['lname']
            userId = request.form['userid']
            if not re.match(r'[A-Za-z0-9]+', username):
                msg = 'name must contain only characters and numbers !'
            else:
                cursor.execute('UPDATE speech SET  username =% s, email =%s, fname =% s, lname =% s WHERE userid =% s', (
                    username, email, fname, lname, (userId, ), ))
                mysql.connection.commit()
                msg = 'User updated !'
                return redirect(url_for('users'))
        elif request.method == 'POST':
            msg = 'Please fill out the form !'
        return render_template("userprofile.html", msg=msg, editUser=editUser)
    return redirect(url_for('userprofile'))

@app.route('/logout')



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        fname = request.form['fname']
        lname = request.form['lname']
        eursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        eursor.execute(
            'SELECT * FROM speech WHERE email = % s', (email, ))
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM speech WHERE username = % s', (username, ))
        account = cursor.fetchone()
        mail = eursor.fetchone()
        if account and mail:
            msg = 'Username and Email already exists !'
        elif mail:
            msg = 'email already exists !'
        elif account:
            msg = 'Username already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO speech VALUES (NULL, % s, % s, % s, % s, % s)',
                           (username, email, password, fname, lname, ))
            mysql.connection.commit()
            msg = 'New user created!'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('signup.html', msg=msg)





