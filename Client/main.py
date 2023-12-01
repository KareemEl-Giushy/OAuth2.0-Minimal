from flask import Flask
import requests

app = Flask(__name__)

@app.route("/")
def home():
  return

@app.route("/Callback")
def callback():
  AccessToken = requests.post("get token")