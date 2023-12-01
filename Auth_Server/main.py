from flask import Flask, render_template, redirect, request, abort, session
import os

app = Flask(__name__)
# app.config.from_object(os.environ['APP_SETTINGS'])
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/login", methods=["POST", 'GET'])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        if 'email' in request.args:
            email = request.args.get('email')
        else:
            abort(403)
        if 'password' in request.args:
            password = request.args.get('password')
        else:
            abort(403)

        # Check the user in the database
            # if ok go to prompt
            # if not abort
        return redirect("/prompt")

@app.route("/prompt", methods=['POST', 'GET'])
def prompt_page():
    if request.method == "POST":
        return redirect()
    if request.method == "GET":
        if "client_name" in request.args:
            client_name = request.args.get("client_name")
        else:
            abort(403)
    
        if "redirect_uri" in request.args:
            re_uri = request.args.get("redirect_uri")
        else:
            abort(403)

        if "response_type" in request.args:
            re_type = request.args.get("response_type")
        else:
            abort(403)

        if "scope" in request.args:
            scope = request.args.get("scope")
        else:
            abort(403)

        print(re_uri, re_type, scope)
        return render_template("prompt.html", client_name=client_name)
    else:
        return redirect('/')

@app.route("/get_token")
def get_token():
    return "Hello"