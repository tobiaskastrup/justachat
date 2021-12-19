#########################################################################
#
#                  GRUPPE 5's justa.chat application
#
#                    Emil Cramer, Mathilde Elkjær, 
#               Christian Ruhwedell & Tobias Jul Kastrup
#
#########################################################################
#/////////////////////////// INSTRUKTIONER /////////////////////////////#
#########################################################################
#
# Kræver følgende moduler installeret flask, request, rocketchat_API
# eg:
# pip install flask request rocketchat_API
#
# Opdater serverURL til rocket.chat server IP og evt porten
# serverURL = 'http://ROCKET-SERVER-IP:3000/'
#
#########################################################################
#                                LIBRARY                                #
#########################################################################

# Sætter dir path til at være hvor app eksekveres, for at undgå modul
# import fejl fra maskine til maskine
import os, sys
dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
sys.path.insert(0, parent_dir_path)
# Påkrævede moduler
from flask import Flask, render_template, request, url_for, session, redirect
from requests import sessions
from rocketchat_API.rocketchat import RocketChat
from rocketchat_API.APIExceptions.RocketExceptions import RocketAuthenticationException
# Vores egne classes
from webapp.py.MyUser import MyUser
from webapp.py.Channels import PublicChannels
from webapp.py.DirectMessages import DM

#########################################################################
#                               VARIABLER                               #
#########################################################################

# Hvor app oprettes og secret key sættes
app = Flask(__name__)
app.config['SECRET_KEY'] = "ahd34h398rbisfb3i4tb5_sg43454wefgdff34"

# Rocket.chat application IP og port
serverURL = 'http://10.1.1.6:3000/'

# Dicts vi bruger til at gemme rocket objekterne i
# Forbedring ville være at gemme det i database eller server side cache
global rocket
global myUser
global dmRooms
global publicRooms
rocket = {}
myUser = {}
dmRooms = {}
publicRooms = {}

#########################################################################
#                               @APP.ROUTES                             #
#########################################################################

# Home Page
@app.route("/")
def home():
    logged_in()

    # Hvis den er logget ind, så opdateres alle rum man er del af og venner man 
    # har samtaler med.
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

# App route som opdatere valgte rum
@app.route("/behindthescenes", methods=["GET", "POST"])
def layout():

    #Funktion som tjekker om der er logget ind
    logged_in()
    if session['is_logged_in']:
        # Tjekker om der er lavet en POST request og tager værdier fra formularen
        # I dette tilfælde om man trykker på et chatrums navn
        if request.method == "POST":
            roomid_info = request.form

            # Gemmer det valgte rum navn fra værdien vi får fra formularen
            session['chosenRoomName'] = roomid_info["channelbutton"]

            #Henter alle nuværende rum navne fra vores 2 klasser og gemmer i dict
            pRooms = publicRooms[session['username']].getMyRooms()
            dRooms = dmRooms[session['username']].getRooms()

            # Gennemgår vores 2 dicts og tjekker om rumnavnet fra formularen
            # passer med en key i vores dicts. Hvis det gør, tager den værdien for
            # dens key, som er ID'et for rummet og gemmer i session['chosenRoomID']
            # samt om det er et DM eller Channel rum
            if session['chosenRoomName'] in dRooms:
                session['chosenRoomID'] = dRooms[session['chosenRoomName']]
                session['chosenRoomType'] = "DM"
            elif session['chosenRoomName'] in pRooms:
                session['chosenRoomID'] = pRooms[session['chosenRoomName']]
                session['chosenRoomType'] = "C"
            
            # Redirect til /phd for at opdatere chatbeskederne der vises
            return redirect(url_for('phd'))

    # Retunere layout template
    return render_template("layout.html")

# Forgot page
@app.route("/forgot", methods=["GET", "POST"])
def forgot():
    logged_in()
    if session['is_logged_in'] == False:
        # Tjekker om der er logget ind og tjekker så for POST requests på /forgot
        if request.method == "POST":
            forgotmail_info = request.form

            # Laver en Anon session til at connecte til Azure uden login og laver en forgot password
            # funktionskald, som sender en mail til brugeren igennem Rocket.chat applicationen
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
            # Tjekker om der er logget ind og tjekker så for POST requests på /phd
            sendmsg = request.form
            # Forsøger at sende en besked til det room ID man pt er inde på.
            if dmRooms[session['username']].sendNewMsg(session['chosenRoomID'], sendmsg['textmsg']):
                # Hvis det lykkes 
                return redirect(url_for("phd"))

        # Tjekker hvilken type Chatrum eller DM, der blev valgt ved /behindthescenes
        # Gemmer efterfølgende alle navne og beskeder for det rum i to lister, som så kan vises i chatten
        if session['chosenRoomType'] == "DM":
            session["currentChatNames"], session["currentChatMsg"] = dmRooms[session['username']].getMessages(session['chosenRoomID'])
        elif session['chosenRoomType'] == "C":
            session["currentChatNames"], session["currentChatMsg"] = publicRooms[session['username']].getMessages(session['chosenRoomID'], 100)

    else:
        return redirect(url_for("login"))

    return render_template("phd.html")

# Profile Page
@app.route("/profile", methods=["GET", "POST"])
def dashboard():

    logged_in()

    if session['is_logged_in']:
        if request.method == "POST":
            
            # Tjekker om der er logget ind og tjekker så for POST requests på /profile
            if request.form.get("submit_b"):
                userreg_info = request.form

                # Forsøger at opdatere bruger profilens email, username, display og password
                if rocket[session['username']].users_update(user_id=myUser[session['username']].getID(), 
                name=userreg_info["displayname"], 
                email=userreg_info["email"], 
                username=userreg_info["username"], 
                password=userreg_info["password"]).json()["success"] == True:
                    # Returnere til Home hvis det lykkes
                    return redirect(url_for("home")) 
            # Går tilbage til home, hvis man vælger cancel
            elif request.form.get("cancel"):
                return redirect(url_for("home")) 
            
    else:
        # Går til login, hvis man ikke er logget ind
        return redirect(url_for("login"))

    #Retunere html templaten for profile.html
    return render_template("profile.html")

# Settings Page - IKKE IMPLEMENTERET!
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
    # Tjekker om der er ikke logget ind og tjekker så for POST requests på /signup
    if session['is_logged_in'] is False:
        if request.method == "POST":

            # Tager bruger input fra signup felterne
            if request.form.get("submit_b"):
                userreg_info = request.form

                # Gemmer variablerne
                reg_displayname = userreg_info["displayname"]
                reg_username = userreg_info["username"]
                reg_password = userreg_info["password"]
                reg_email = userreg_info["email"]

                # Opretter en Anon session (uden brugernavn og password) til
                # at oprette en bruger
                if createAnonSession():
                    # Hvis session oprettes forsøges det at registere en bruger
                    signuprespons = anonrocket.users_register(email=reg_email, name=reg_displayname, password=reg_password, username=reg_username).json()
                    # Hvis brugeren oprettes redirectes til /login
                    if signuprespons["success"]:
                        return redirect(url_for('login'))
                    else:
                        return redirect(url_for('signup'))
            # Cancelknap redirects til /home
            elif request.form.get("cancel"):
                return redirect(url_for("home")) 
            
    else:
        # Er man logget ind redirectes til /home
        return redirect(url_for("home"))

    return render_template("signup.html")

#########################################################################
#                               FUNCTIONS                               #
#########################################################################

#Oprettelse af en session og efterfølgende rocket opjekt, som er forbindelsen til vores rocketchat server
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

# Funktion som tjekker om der er gemt et usernavn i session og om det usernavn
# har en key i rocket dict, som betyder der er en rocket session åben
# i en clients browser.
def logged_in():
    if 'username' in session:
        if session['username'] in rocket:
            session['is_logged_in'] = True
        else:
            session['is_logged_in'] = False
    else:
        session['is_logged_in'] = False

#########################################################################
#                               INITIALIZE                              #
#########################################################################

# Her sættes de parameter som flask serveren skal starte med.
# Vi starter dog appen fra wsgi.py på gunicorn serveren, hvorfor 
# Dette kun bruges ved kørsel af app.py direkte

if __name__ == "__main__":
    app.run(debug=True)