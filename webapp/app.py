#########################################################################
#                                LIBRARY                                #
#########################################################################

from flask import Flask, render_template, request, url_for

# We need to use sessions yaaaay

from jinja2 import FileSystemLoader, Environment

from requests import sessions
from rocketchat_API.rocketchat import RocketChat
from rocketchat_API.APIExceptions.RocketExceptions import RocketAuthenticationException
from werkzeug.utils import redirect
from py.MyUser import MyUser
from py.Channels import PublicChannels
from py.OtherUsers import OtherUsers
from py.DirectMessages import DM


#########################################################################
#                                   X                                   #
#########################################################################

app = Flask(__name__)

# db = mysql.connector.connect(
    # host = "",
    # user = "",
    # password = "",
    # database = ""
# )

serverURL = 'http://justa.chat:3000/'
errormsg = ""

is_logged_in = None

def logged_in():
    try:
        rocket
    except NameError:
        is_logged_in = False
        print(is_logged_in)
    else:
        is_logged_in = True
        print(is_logged_in)

#########################################################################
#                                WEB PAGES                              #
#########################################################################

# Placeholder: This is a web page structure reference
# layout.html is base layout all other pages refer to
# newpage.html is quick pasteable template for creating a new page
@app.route("/behindthescenes")
def layout():
    return render_template("layout.html", logged=is_logged_in)

@app.route("/phd")
def phd():
    # Web page code
    return render_template("phd.html", logged=is_logged_in)

# Home Page
@app.route("/")
def home():
    return render_template("home.html", logged=is_logged_in)

# Login Page
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        login_info = request.form

        username = login_info["username"]
        password = login_info["password"]

        if createSession(username, password):
            logged_in()
            return redirect(url_for('home'))
        else:
            pass

    return render_template("login.html", logged=is_logged_in)

# Profile Page
@app.route("/profile")
def dashboard():
    return render_template("profile.html", logged=is_logged_in)

# Settings Page
@app.route("/settings")
def settings():
    return render_template("settings.html", logged=is_logged_in)

# Signup
@app.route("/signup")
def signup():
    return render_template("signup.html", logged=is_logged_in)



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



#########################################################################
#                               INITIALIZE                              #
#########################################################################

if __name__ == "__main__":
    app.run(debug=True)