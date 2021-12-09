
from requests import sessions
from pprint import pprint
from rocketchat_API.rocketchat import RocketChat
import re
# nickname = input("Username: ")
# password = input("Password: ")

nickname = "tobias"
password = "Mahman"
    

def getUserID(_username):
    otheruserobj = rocket.users_info(_username).json()
    if otheruserobj["user"]["_id"] is not None:
        otherUserID = otheruserobj["user"]["_id"]
        return otherUserID

    
def createSession(_nickname, _password):
    with sessions.Session() as session:
        global rocket
        rocket = RocketChat(_nickname, _password, server_url='http://justa.chat:3000/', session=session)

def getPublicChatRooms():
    channelobj = rocket.channels_list().json()

    # Henter mulige rum
    channelsnames = []
    channelsid = []
    if "channels" in channelobj:
        channelliste = channelobj["channels"]
        if type(channelliste) is list:
            for xyz in channelliste:
                channelsnames.append(xyz["name"])
                channelsid.append(xyz["_id"])
    
    return channelsnames, channelsid

def choosePublicRoom(_channelsnames, _channelsid):
    # Printer mulige rum
    print("Choose a room to connect:")
    n=1
    for rooms in _channelsnames:
        print(f'{n}: {rooms}')
        n = n+1
    
    # Vælg et rum
    while True:
        try:
            i = int(input(f"Vælg et nummer mellem 1 og {len(_channelsnames)}: "))
            break
        except ValueError:
            print('\nYou did not enter a valid integer')
        if i < len(_channelsnames):
            print("\nFail")
        elif i < 1:
            print("\nFail")
    
    return i, _channelsid[i-1]

def printChannelMessages(RoomNo, _publicRoomID, _msgCount):
    msg = rocket.channels_history(_publicRoomID, count=_msgCount).json()

    # Itterer igennem beskeder fra rummet
    print(f"\n<<< Beskeder fra {cNames[RoomNo-1]} >>>")
    if "messages" in msg:
        msgliste = msg["messages"]
        if type(msgliste) is list:
            for xyz in reversed(msgliste):
                print(f'{xyz["u"]["username"]}:     {xyz["msg"]}')

def createIM():
    recipient_username = input("Input username of the person you want to chat with: ")
    rocket.im_create(recipient_username).json()

# Mangler "username already exists check"
def createNewUser():
    pattern = "^.*(?=.{8,})(?=.*\d)(?=.*[a-zøæå])(?=.*[A-ZÆØÅ)(?=.*[$&+,:;=?@#|'<>.-^*()%!_]).*$"
    nickname = input("Type your desired username: ")
    username = input("Type your first name: ")
    # Checker om password er stærkt nok
    while True:
        password = input("Type a password here: ")
        result = re.findall(pattern, password)
        if (result):
            print("Password is okay!")
            break
        else:
            print("Password doesn't meet the requirments")



    with sessions.Session() as session:
        rocket = RocketChat('UserCreateAdmin', 'SuperStrong123!',server_url='http://justa.chat:3000/', session=session)
        rocket.users_create(username+'@justa.chat', username, password, nickname).json()

def deleteUser():
    user_id = input("Type the name of the user to be deleted: ")
    delobj = rocket.users_info(user_id).json()
    if delobj["user"] is not None:
        userID = delobj["user"]["_id"]
        pprint(rocket.users_delete(userID))

# Henter user ID for brugeren
def getUserID():
    userobj = rocket.me().json()
    if userobj["_id"] is not None:
        userID = userobj["_id"]
        myusername = userobj["username"]

def getAvailableIM():
    imsobj = rocket.im_list().json()

    # Henter mulige rum
    imsnames = []
    imsid = []
    if "ims" in imsobj:
        imslist = imsobj["ims"]
        if type(imslist) is list:
            for xyz in imslist:
                usernameobj = xyz["usernames"]
                for usernames in usernameobj:
                    if usernames != myusername:
                        imsnames.append(usernames)
                        imsid.append(xyz["_id"])
    
    return imsnames, imsid
    
def chooseIMRoom():
    # Printer mulige rum
    print("Choose a room to connect:")
    n=1
    for rooms in imsnames:
        print(f'{n}: {rooms}')
        n = n+1
    
    # Vælg et rum
    while True:
        try:
            i = int(input(f"Vælg et nummer mellem 1 og {len(imsnames)}: "))
            break
        except ValueError:
            print('\nYou did not enter a valid integer')
        if i < len(imsnames):
            print("\nFail")
        elif i <= 1:
            print("\nFail")

def printIMMessages():
    # Henter beskeder fra valgte rum
    msg = rocket.im_history(imsid[i-1], count=10).json()

    # Itterer igennem beskeder fra rummet
    print(f"\n<<< Beskeder fra {imsnames[i-1]} >>>")
    if "messages" in msg:
        msgliste = msg["messages"]
        if type(msgliste) is list:
            for xyz in reversed(msgliste):
                print(f'{xyz["u"]["username"]}: {xyz["msg"]}')

# Mangler Password sikkerhed og "username already exists"
def updateUserInfo():
    userobj = rocket.me().json()
    userID = userobj["_id"]
    new_email = input("Update email: ")
    new_name = input("Update name: ")
    new_password = input("Update password: ")
    new_username = input("Update username: ")
    rocket.users_update(userID, email=new_email, name=new_name, password= new_password, username=new_username).json()

#### TEST AF FUNKTIONER ####
createSession(nickname, password)
print(getUserID("christian"))
cNames, cIDs = getPublicChatRooms()
chosenRoomNo, chosenPublicChatRoom = choosePublicRoom(cNames, cIDs)
printMessages(chosenRoomNo, chosenPublicChatRoom, 10)