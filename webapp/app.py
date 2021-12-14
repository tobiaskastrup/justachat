#########################################################################
#                                LIBRARY                                #
#########################################################################

from flask import Flask, render_template
from requests import sessions
from rocketchat_API.rocketchat import RocketChat
from webapp.py.MyUser import MyUser
from webapp.py.Channels import PublicChannels
from webapp.py.OtherUsers import OtherUsers
from webapp.py.DirectMessages import DM



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



#########################################################################
#                                WEB PAGES                              #
#########################################################################

# Placeholder: This is a web page structure reference
# layout.html is base layout all other pages refer to
# newpage.html is quick pasteable template for creating a new page
@app.route("/behindthescenes")
def layout():
    # Web page code
    return render_template("layout.html")

@app.route("/phd")
def phd():
    # Web page code
    return render_template("phd.html")

# Home Page
@app.route("/")
def home():
    return render_template("home.html")

# Login Page
@app.route("/login")
def login():
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

# List of available chatrooms (incomplete, need database stuff)
# def get_data_from_db():
    # cur = db.cursor()
    # cur.execute("SELECT room FROM chatrooms")
    # chatroom_list = cur.fetchall()
    # chatroom_list = [i[0] for i in chatroom_list]
    # return chatroom_list



#########################################################################
#                               INITIALIZE                              #
#########################################################################
if __name__ == "__main__":
    app.run(debug=True)