from flask import Flask, render_template, redirect, request, abort, session, url_for
import requests as re
from urllib.parse import quote

app = Flask(__name__)
app.secret_key = 'this is another secret key'

SECRET_KEY = "this is my secret key"
AUTH_SERVER = "http://localhost:5000"

@app.route("/")
def home():
  return "<p>Hello, This Is A Client Application That wants to connect to a service</p>"

@app.route("/user", methods=["GET"])
def user():
  if 'accessToken' not in session:
    return redirect(url_for("home"))

  userData = re.post(f"{AUTH_SERVER}/user_data", {"token": session['accessToken']})

  return userData.json()

@app.route("/connect", methods=['GET'])
def connect():
  if request.method == "GET":
    client_name = "External App"
    redirect_uri = "http://localhost:5050/callback"
    response_type = ""
    scope = "profile"
    return render_template("connect.html", client_name = quote(client_name), redirect_uri = quote(redirect_uri), response_type = quote(response_type), scope = quote(scope))

@app.route("/callback", methods=['GET'])
def callback():
  if request.method == "GET":
    if "auth_code" not in request.args:
      abort(403)

    auth_code = request.args.get('auth_code')

    accessToken = re.post(f"{AUTH_SERVER}/get_token", {"auth_code": auth_code, "secret_key": SECRET_KEY})

    session['accessToken'] = accessToken.content

    return  accessToken.content