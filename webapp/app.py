#########################################################################
#                                LIBRARY                                #
#########################################################################

import os, sys
dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
sys.path.insert(0, parent_dir_path)

from flask import Flask, render_template, request, url_for, session, redirect

from jinja2 import FileSystemLoader, Environment

loader = FileSystemLoader('/tmp')
env = Environment(autoescape=True, loader=loader)

import threading
import time
from requests import sessions
from rocketchat_API.rocketchat import RocketChat
from rocketchat_API.APIExceptions.RocketExceptions import RocketAuthenticationException
from webapp.py.MyUser import MyUser
from webapp.py.Channels import PublicChannels
from webapp.py.OtherUsers import OtherUsers
from webapp.py.DirectMessages import DM
from pprint import pprint



#########################################################################
#                                   X                                   #
#########################################################################

app = Flask(__name__)
app.secret_key = "asdas3tgdsv4"

serverURL = 'http://justa.chat:3000/'



#########################################################################
#                                WEB PAGES                              #
#########################################################################

# Placeholder: This is a web page structure reference
# layout.html is base layout all other pages refer to
# newpage.html is quick pasteable template for creating a new page
@app.route("/behindthescenes", methods=["GET", "POST"])
def layout():
    if request.method == "POST":
        roomid_info = request.form

        session['chosenRoom'] = roomid_info["channelbutton"]

        return redirect(url_for('phd'))

    return render_template("layout.html")

# Chatroom page
@app.route("/phd")
def phd():
    if session['is_logged_in']:
        session["currentChatNames"], session["currentChatMsg"] = publicRooms.getMessages(session['chosenRoom'], 100)
        print(session['chosenRoom']) 
        print(session["currentChatMsg"])
    else:
        return redirect(url_for("login"))

    return render_template("phd.html")

# Home Page
@app.route("/")
def home():
    logged_in()

    if session['is_logged_in']:
        session['cRoomNames'], session['cRoomIDs'] = publicRooms.getMyRoomsAsLists()
        # if session.get('chosenRoom') == True:
        #     print(session['chosenRoom'])

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
            makeChatObjects()

            return redirect(url_for('home'))
        else:
            pass # Besked om login ikke virker

    return render_template("login.html")

# Profile Page
@app.route("/profile")
def dashboard():
    if session['is_logged_in']:
        pass
    else:
        return redirect(url_for('home'))

    return render_template("profile.html")

# Settings Page
@app.route("/settings")
def settings():

    if session['is_logged_in']:
        pass
    else:
        return redirect(url_for("login"))

    return render_template("settings.html")

# Signup
@app.route("/signup", methods=["GET", "POST"])
def signup():

    if session['is_logged_in'] is False:
        if request.method == "POST":

            if request.form.get("submit_b"):
                userreg_info = request.form

                reg_displayname = userreg_info["displayname"]
                reg_username = userreg_info["username"]
                reg_password = userreg_info["password"]
                reg_email = "".join([reg_username, "@justa.chat"])

                if createAnonSession():
                    signuprespons = anonrocket.users_register(reg_email, reg_displayname, reg_password, reg_username).json()
                    print("signup: ", signuprespons["success"])
                    if signuprespons["success"]:
                        
                        return redirect(url_for('login'))
                
                    else:
                        pass

            elif request.form.get("cancel"):
                return redirect(url_for("home")) 
            
    else:
        return redirect(url_for("home"))

    return render_template("signup.html")



#########################################################################
#                               FUNCTIONS                               #
#########################################################################

def createSession(_nickname, _password) -> bool:
    with sessions.Session() as session:
        try:
            global rocket
            rocket = RocketChat(_nickname, _password, server_url=serverURL, session=session)
            return True
        except RocketAuthenticationException as e:
            print("Login or connection failed")
            return False
        except Exception as ve:
            print("Something went wrong")
            return False

def createAnonSession():
    with sessions.Session() as session:
        try:
            global anonrocket
            anonrocket = RocketChat(server_url=serverURL, session=session)
            return True
        except RocketAuthenticationException as e:
            print("Connection failed")
            return False
        except Exception as ve:
            print("Something went wrong")
            return False

def makeChatObjects():
    global myUser
    global dmRooms
    global publicRooms
    myUser = MyUser(username=session["username"], rocket=rocket)
    dmRooms = DM(rocket, myUser.getUsername())
    publicRooms = PublicChannels(rocket)

def logged_in():
    try:
        rocket
    except NameError:
        session['is_logged_in'] = False
    else:
        session['is_logged_in'] = True
    print("Logged in: ", session['is_logged_in'])

# def updateChosenRoom(roomid):
#     session['chosenRoom'] = roomid
#     print(roomid)
#     #print(session['cRoomNames'])
#     #print(session['cRoomIDs'])

# app.jinja_env.globals.update(updateChosenRoom=updateChosenRoom)

#########################################################################
#                               INITIALIZE                              #
#########################################################################

if __name__ == "__main__":
    app.run(debug=True)