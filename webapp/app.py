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

serverURL = 'http://10.1.1.6:3000/'

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

    return render_template("home.html")

# Login Page
@app.route("/login", methods=["GET", "POST"])
def login():
    # If løkke som kikker om der bliver lavet en POST request fra /login siden
    if request.method == "POST":
        # Informationen der er indsat i text boksene 
        # username og password gemmes i en dict login_info
        login_info = request.form

        # Bruges username gemmes i en session, som bruges i mens man er logget ind
        session['username'] = login_info["username"]
        password = login_info["password"]

        # Der forsøges at laves en session med login informationerne 
        if createSession(session['username'], password):
            #Hvis det lykkes oprettes der user, DM og Channel objekter for bruger
            makeChatObjects(session['username'])

            #Efter login omdiregeres brugeren til home siden
            return redirect(url_for('home'))
        else:
            pass # Besked om login ikke virker (ikke implementeret)
    
    # login html template sendes til brugerens browser
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
                    signuprespons = anonrocket.users_register(email=reg_email, name=reg_displayname, password=reg_password, username=reg_username).json()
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

#Oprettelse af en session og efterfølgende rocket opjekt, som er forbindelsen til vores rocketchat server
def createSession(_nickname, _password) -> bool:
    with sessions.Session() as session:
        try:
            #Forsøger at lave et objekt med login oplysningerne
            rocket[_nickname] = RocketChat(_nickname, _password, server_url=serverURL, session=session)
            return True
        except RocketAuthenticationException as e:
            # Hvis login oplysningerne er forkerte printer den en fejl besked
            # !! Mangler at implementer besked til brugeren
            print(_nickname, ": Login auth failed", e)
            return False
        except Exception as ve:
            # Andre fejl giver følgende besked (fx manglende forbindelse)
            print(_nickname, ": Something went wrong")
            return False

def makeChatObjects(username):
    # Gemmer objekter af klasserne myUser, DM og PublicChannels 
    #  som en value til key (ens username) i dict
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

#########################################################################
#                               INITIALIZE                              #
#########################################################################

if __name__ == "__main__":
    app.run(debug=True)