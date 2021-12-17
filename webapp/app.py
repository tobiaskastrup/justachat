#########################################################################
#                                LIBRARY                                #
#########################################################################

import os, sys
dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
sys.path.insert(0, parent_dir_path)

from flask import Flask, render_template, request, url_for, session, redirect

from requests import sessions
from rocketchat_API.rocketchat import RocketChat
from rocketchat_API.APIExceptions.RocketExceptions import RocketAuthenticationException
from webapp.py.MyUser import MyUser
from webapp.py.Channels import PublicChannels
from webapp.py.DirectMessages import DM

#########################################################################
#                                   X                                   #
#########################################################################

app = Flask(__name__)
app.config['SECRET_KEY'] = "ahd34h398rbisfb3i4tb5_sg43454wefgdff34"

serverURL = 'http://justa.chat:3000/'

global rocket
global myUser
global dmRooms
global publicRooms

rocket = {}
myUser = {}
dmRooms = {}
publicRooms = {}

#########################################################################
#                                WEB PAGES                              #
#########################################################################

# Placeholder: This is a web page structure reference
# layout.html is base layout all other pages refer to
# newpage.html is quick pasteable template for creating a new page
@app.route("/behindthescenes", methods=["GET", "POST"])
def layout():
    logged_in()
    if session['is_logged_in']:
        if request.method == "POST":
            roomid_info = request.form

            session['chosenRoomName'] = roomid_info["channelbutton"]
            pRooms = publicRooms[session['username']].getMyRooms()
            dRooms = dmRooms[session['username']].getRooms()

            # Finds ID for room by checking in room dict for Channel and DM rooms
            if session['chosenRoomName'] in dRooms:
                session['chosenRoom'] = dRooms[session['chosenRoomName']]
                session['chosenRoomType'] = "DM"
            elif session['chosenRoomName'] in pRooms:
                session['chosenRoom'] = pRooms[session['chosenRoomName']]
                session['chosenRoomType'] = "C"
            

            return redirect(url_for('phd'))

    return render_template("layout.html")

# Forgot page
@app.route("/forgot", methods=["GET", "POST"])
def forgot():
    logged_in()
    if session['is_logged_in'] == False:
        if request.method == "POST":
            forgotmail_info = request.form

            if createAnonSession():
                forgotrespons = anonrocket.users_forgot_password(forgotmail_info["email"]) .json()
                
                if forgotrespons["success"]:
                    return redirect(url_for('home'))
            
                else:
                    return redirect(url_for('forgot'))

    else:
        return redirect(url_for("home"))

    return render_template("forgot.html")

# Chatroom page
@app.route("/phd", methods=["GET", "POST"])
def phd():
    logged_in()
    if session['is_logged_in']:
        if request.method == "POST":

            sendmsg = request.form
            print("Send", sendmsg['textmsg'])
            if dmRooms[session['username']].sendNewMsg(session['chosenRoom'], sendmsg['textmsg']):
                return redirect(url_for("phd"))

        if session['chosenRoomType'] == "DM":
            session["currentChatNames"], session["currentChatMsg"] = dmRooms[session['username']].getMessages(session['chosenRoom'])
        elif session['chosenRoomType'] == "C":
            session["currentChatNames"], session["currentChatMsg"] = publicRooms[session['username']].getMessages(session['chosenRoom'], 100)

    else:
        return redirect(url_for("login"))

    return render_template("phd.html")

# Home Page
@app.route("/")
def home():
    logged_in()

    if session['is_logged_in']:
        session['cRoomNames'] = publicRooms[session['username']].getMyRoomsAsLists()
        session['dRoomNames'] = dmRooms[session['username']].getMyRoomsAsLists()
        session['displayName'] = myUser[session['username']].getDisplayName()
        session['myMailAddress'] = myUser[session['username']].getMail()

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
            makeChatObjects(session['username'])

            return redirect(url_for('home'))
        else:
            pass # Besked om login ikke virker

    return render_template("login.html")

# Profile Page
@app.route("/profile", methods=["GET", "POST"])
def dashboard():

    logged_in()

    if session['is_logged_in']:
        if request.method == "POST":

            if request.form.get("submit_b"):
                userreg_info = request.form

                if rocket[session['username']].users_update(user_id=myUser[session['username']].getID(), 
                name=userreg_info["displayname"], 
                email=userreg_info["email"], 
                username=userreg_info["username"], 
                password=userreg_info["password"]).json()["success"] == True:

                    return redirect(url_for("home")) 

            elif request.form.get("cancel"):
                return redirect(url_for("home")) 
            
    else:
        return redirect(url_for("login"))

    return render_template("profile.html")

# Settings Page
@app.route("/settings")
def settings():
    logged_in()

    if session['is_logged_in']:
        pass
    else:
        return redirect(url_for("login"))

    return render_template("settings.html")

# Signup
@app.route("/signup", methods=["GET", "POST"])
def signup():
    logged_in()

    if session['is_logged_in'] is False:
        if request.method == "POST":

            if request.form.get("submit_b"):
                userreg_info = request.form

                reg_displayname = userreg_info["displayname"]
                reg_username = userreg_info["username"]
                reg_password = userreg_info["password"]
                reg_email = userreg_info["email"]

                if createAnonSession():
                    signuprespons = anonrocket.users_register(reg_email, reg_displayname, reg_password, reg_username).json()
                    anonrocket.users_register()
                    if signuprespons["success"]:
                        return redirect(url_for('login'))
                
                    else:
                        return redirect(url_for('signup'))

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
            rocket[_nickname] = RocketChat(_nickname, _password, server_url=serverURL, session=session)
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

def makeChatObjects(username):
    myUser[username] = MyUser(username=session["username"], rocket=rocket[username])
    dmRooms[username] = DM(rocket[username], myUser[username].getUsername())
    publicRooms[username] = PublicChannels(rocket[session['username']])

def logged_in():
    if 'username' in session:
        print(session['username'])
        print(rocket)
        if session['username'] in rocket:
            session['is_logged_in'] = True
        else:
            session['is_logged_in'] = False
    else:
        session['is_logged_in'] = False
        
    print("Logged in: ", session['is_logged_in'])

#########################################################################
#                               INITIALIZE                              #
#########################################################################

if __name__ == "__main__":
    app.run(debug=True)