from flask import Flask, render_template, redirect, request, session
from functools import wraps
import sqlite3


def db_conn():
    try:
        conn = sqlite3.connect("hrm.db")
        return True
    except Exception:
        return False


app = Flask(__name__)
app.secret_key = "gss03452"


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('username') is None or session.get('if_logged') is None:
            return redirect('/signin', code=302)
        return f(*args, **kwargs)

    return decorated_function


def emp_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('emp_username') is None or session.get('emp_if_logged') is None:
            return redirect('/employee/signin', code=302)
        return f(*args, **kwargs)

    return decorated_function


@app.route('/signin', methods=['GET', 'POST', 'DELETE'])
def signin():
    if request.method == "POST":
        username = request.form['uname']
        password = request.form['pwd']

        auth = ''' select * from signin where username=? AND password=? '''
        if db_conn:
            conn = sqlite3.connect("hrm.db")
            cur = conn.cursor()
            user = None
            cur.execute(auth, (username, password))
            user = cur.fetchone()

            if user != None:
                session['username'] = user[1]
                session['if_logged'] = True
                return redirect('/')
            else:
                return redirect('signin')

        else:
            print('db connection error')
            return redirect('signin')

    return render_template('signin.html')


@app.route('/signup', methods=["GET", "POST", 'DELETE'])
def signup():
    if request.method == "POST":
        username = request.form['uname']
        email = request.form['email']
        password = request.form['pwd']

        if db_conn:
            conn = sqlite3.connect("hrm.db")
            cur = conn.cursor()

            r = (username, email, password)
            l = (username, password)

            r_sql = ''' INSERT INTO signup(username,email,password)
                    VALUES(?,?,?) '''

            l_sql = ''' INSERT INTO signin(username,password)
                    VALUES(?,?) '''

            try:
                cur.execute(r_sql, r)
                cur.execute(l_sql, l)
                conn.commit()
                return redirect('signin')

            except Exception:
                return redirect('signup')

    return render_template('signup.html')


@app.route('/')
@login_required
def index():
    return render_template('index.html')


@app.route('/profile')
@login_required
def profile():
    conn = sqlite3.connect("hrm.db")
    cur = conn.cursor()

    uname = name = email = phno = location = skills = ''

    p_sql = "select * from profile where username=?"
    try:
        cur.execute(p_sql, [session.get('username')])
        details = cur.fetchone()
        uname = details[1]
        email = details[2]
        name = details[3]
        phno = details[4]
        location = details[5]
        skills = details[6]
    except:
        print('error')

    return render_template('profile.html', name=name, email=email, phno=phno, location=location, skills=skills)


@app.route('/edit', methods=["GET", "POST", 'DELETE'])
@login_required
def edit():
    if request.method == "POST":
        name = (request.form['name'])
        phno = str(request.form['phno'])
        location = str(request.form['location']).lower()
        skills = str(request.form['skills']).lower()

        e_sql = '''UPDATE profile SET name = ?, phno = ?, location = ?, skills = ? WHERE username = ? '''

        if db_conn:
            conn = sqlite3.connect("hrm.db")
            cur = conn.cursor()
            try:
                cur.execute(e_sql, (name, phno, location, skills, session.get('username')))
                conn.commit()
                return redirect('profile')
            except Exception:
                return redirect('edit')

    return render_template('edit.html')


@app.route('/employee/signin', methods=['GET', 'POST', 'DELETE'])
def emp_signin():
    if request.method == "POST":
        username = request.form['uname']
        password = request.form['pwd']

        auth = ''' select * from emp_signin where username=? AND password=? '''
        if db_conn:
            conn = sqlite3.connect("hrm.db")
            cur = conn.cursor()
            user = None
            cur.execute(auth, (username, password))
            user = cur.fetchone()

            if user != None:
                session['emp_username'] = user[1]
                session['emp_if_logged'] = True
                return redirect('/employee')
            else:
                return redirect('signin')

        else:
            print('db connection error')
            return redirect('signin')
    return render_template('emp_signin.html')


@app.route('/employee/signup', methods=['GET', 'POST', 'DELETE'])
def emp_signup():
    if request.method == "POST":
        username = request.form['uname']
        email = request.form['email']
        password = request.form['pwd']

        if db_conn:
            conn = sqlite3.connect("hrm.db")
            cur = conn.cursor()

            r = (username, email, password)
            l = (username, password)

            r_sql = ''' INSERT INTO emp_signup(username,email,password)
                    VALUES(?,?,?) '''

            l_sql = ''' INSERT INTO emp_signin(username,password)
                    VALUES(?,?) '''

            try:
                cur.execute(r_sql, r)
                cur.execute(l_sql, l)
                conn.commit()
                return redirect('signin')

            except Exception:
                return redirect('signup')
    return render_template('emp_signup.html')


@app.route('/employee', methods=['GET', 'POST', 'DELETE'])
@emp_login_required
def emp_index():
    emp_uname = session.get('emp_username')
    type = ''
    key = ''
    query = "select * from profile"
    if request.method == "POST":
        type = request.form['type']
        key = request.form['key']

        if type == 'location':
            query = "select * from profile where location LIKE LOWER('" + key + "')"
        elif type == 'skills':
            query = "select * from profile"

    results = []
    if db_conn:
        conn = sqlite3.connect("hrm.db")
        cur = conn.cursor()
        cur.execute(query)
        results = cur.fetchall()
        n = len(results)

    return render_template('emp_index.html', emp_uname=emp_uname, results=results, n=n)


@app.route('/logout')
@login_required
def logout():
    session.pop('username', None)
    session.pop('logged_in', None)

    return redirect('signin')


if __name__ == '__main__':
    app.run()
