from flask import Flask, render_template, redirect, request
import requests as re

app = Flask(__name__)

@app.route("/")
def home():
  return "<p>Hello, This Is An External Application</p>"

@app.route("/connect", methods=['GET', 'POST'])
def connect():
  if request.method == "POST":
    client_name = ""
    redirect_uri = ""
    response_type = ""
    scope = ""

    return redirect(f"http://localhost:5000/prompt?client_name=${client_name}&redirect_uri={redirect_uri}&response_type={response_type}&scope={scope}")

  if request.method == "GET":
    return render_template("connect.html")

@app.route("/callback")
def callback():
  return ''