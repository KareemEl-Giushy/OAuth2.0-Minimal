from flask import Flask, render_template, redirect, request, abort, session, url_for
import secrets
import sqlite3

app = Flask(__name__)
app.secret_key = 'this is my secret key'

def get_db_connection():
    conn = sqlite3.connect('./db/database.db')
    conn.row_factory = sqlite3.Row
    return conn

def check_parameters():
    if "client_name" not in request.args:
        return False

    if "redirect_uri" not in request.args:
        return False

    if "response_type" not in request.args:
        return False

    if "scope" not in request.args:
        return False

    return True


@app.route("/")
def home():
    if session.get('logged_in') == True:
        return "<p>Hello, " + session['user']['name'].title() + ". Have A Great Day!</p>"

    return "<p>Hello, World!</p>"

@app.route("/login", methods=["POST", 'GET'])
def login():
    if request.method == "GET":
        if session.get('logged_in') == True:
            return redirect(url_for('home'))

        return render_template("login.html")

    if request.method == "POST":
        
        if 'email' in request.form:
            email = request.form.get('email')
        else:
            abort(403)
        if 'password' in request.form:
            password = request.form.get('password')
        else:
            abort(403)

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE email = ? AND password = ?', [email, password]).fetchall()
        conn.close()

        if user and len(user) == 1:
            session['logged_in'] = True
            session['user'] = {
                "id": user[0]['id'],
                "name": user[0]['name'],
                "email": user[0]['email'],
                "phone": user[0]['phone'],
                "created_at": user[0]['created_at']
            }

            return redirect(url_for("prompt_page"))

        # if not open login again
        return render_template("login.html", error="Invalid Login")

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.clear()
    return redirect(url_for('home'))

@app.route("/prompt", methods=['POST', 'GET'])
def prompt_page():
    if request.method == "POST":
        if not session.get('oauth') or "decision" not in request.form:
            abort(403)

        if request.form.get('decision') == 'accept':
            conn = get_db_connection()
            auth_code = secrets.token_hex(15)
            conn.execute('INSERT INTO tokens(auth_code, user_id) VALUES (?, ?)', [auth_code, session['user']['id']])
            conn.close()

            return redirect(session['oauth']['redirect_uri'] +"?auth_code=" + auth_code)
    
        return "<p>Permission Denied to " + session['oauth']['client_name'] + "</p>"

    if request.method == "GET":

        if not session.get('oauth'):
            if not check_parameters():
                abort(403)

            session['oauth'] = request.args.to_dict()

        if "logged_in" not in session or session['logged_in'] != True:
            return redirect(url_for('login'))

        return render_template("prompt.html", client_name=session['oauth']['client_name'])
    else:
        return redirect(url_for('home'))

@app.route("/get_token")
def get_token():
    return "Hello"