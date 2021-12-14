#########################################################################
#                                LIBRARY                                #
#########################################################################

import os, sys
dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
sys.path.insert(0, parent_dir_path)


from flask import Flask, render_template, request, url_for, session, redirect

# We need to use sessions yaaaay

from jinja2 import FileSystemLoader, Environment

import threading
import time
from requests import sessions
from rocketchat_API.rocketchat import RocketChat
from rocketchat_API.APIExceptions.RocketExceptions import RocketAuthenticationException
from webapp.py.MyUser import MyUser
from webapp.py.Channels import PublicChannels
from webapp.py.OtherUsers import OtherUsers
from webapp.py.DirectMessages import DM


#########################################################################
#                                   X                                   #
#########################################################################

app = Flask(__name__)
app.secret_key = "asdas3tgdsv4"

serverURL = 'http://justa.chat:3000/'
errormsg = ""

#########################################################################
#                                WEB PAGES                              #
#########################################################################

# Placeholder: This is a web page structure reference
# layout.html is base layout all other pages refer to
# newpage.html is quick pasteable template for creating a new page
@app.route("/behindthescenes")
def layout():
    return render_template("layout.html")

@app.route("/phd")
def phd():
    session["currentChat"] = {"emil": "hej",
            "tobias": "godav"}
    return render_template("phd.html")

# Home Page
@app.route("/")
def home():
    logged_in()
    if session['is_logged_in']:
        pass

    session['channelNames'] = {"Channel 1": "asfesf243afs",
    "Channel 2": "asdf45hsfe",
    "Channel 3": "adv45g4gd43",}
    
    return render_template("home.html")

# Login Page
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        login_info = request.form

        session['username'] = login_info["username"]
        password = login_info["password"]
        logged_in()

        if createSession(session['username'], password):
            global myUser
            global dmRooms
            global publicRooms
            myUser = MyUser(username=session['username'], rocket=rocket)
            dmRooms = DM(rocket, myUser.getUsername())
            publicRooms = PublicChannels(rocket)

            return redirect(url_for('home'))
        else:
            pass

    return render_template("login.html")

# Profile Page
@app.route("/profile")
def dashboard():
    return render_template("profile.html")

# Settings Page
@app.route("/settings")
def settings():
    return render_template("settings.html")

# Signup
@app.route("/signup")
def signup():
    return render_template("signup.html")



#########################################################################
#                               FUNCTIONS                               #
#########################################################################

# def database_query(x, y, z):
    # cur = db.cursor()
    # cur.execute("INSERT INTO a(x, y, z) VALUES (%s, %s, %s)", (x, y, z))
    # db.commit()
    # cur.close()

# List of available chatrooms (incomplete, need database stuff)
# def get_data_from_db():
    # cur = db.cursor()
    # cur.execute("SELECT room FROM chatrooms")
    # chatroom_list = cur.fetchall()
    # chatroom_list = [i[0] for i in chatroom_list]
    # return chatroom_list

def createSession(_nickname, _password) -> bool:
    with sessions.Session() as session:
        try:
            global rocket
            rocket = RocketChat(_nickname, _password, server_url=serverURL, session=session)
            return True
        except RocketAuthenticationException as e:
            errormsg = "Login or connection failed"
            return False
        except Exception as ve:
            errormsg = "Something went wrong"
            return False

def createAnonSession():
    with sessions.Session() as session:
        try:
            global anonrocket
            anonrocket = RocketChat(server_url=serverURL, session=session)
            return True
        except RocketAuthenticationException as e:
            errormsg = "Connection failed"
            return False
        except Exception as ve:
            errormsg = "Something went wrong"
            return False

def logged_in():
    try:
        rocket
    except NameError:
        session['is_logged_in'] = False
    else:
        session['is_logged_in'] = True

def checker():
    pass

def checker_thread():
    while True:
        if session['is_logged_in']:
            checker()
        time.sleep(5)

#########################################################################
#                               INITIALIZE                              #
#########################################################################

if __name__ == "__main__":
    x = threading.Thread(target=checker_thread)
    x.start()
    app.run(debug=True)