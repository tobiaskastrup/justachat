from requests import sessions
from pprint import pprint
import json
from rocketchat_API.rocketchat import RocketChat

user = input('Indtast dit brugernavn: ')
password = input('Indtast dit password: ')

with sessions.Session() as session:
    # Opretter en session med login oplysninger
    rocket = RocketChat(user, password, server_url='http://justa.chat:3000', session=session)


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

        