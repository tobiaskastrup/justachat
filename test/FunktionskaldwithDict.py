
from requests import sessions
from pprint import pprint
from rocketchat_API.rocketchat import RocketChat

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
    publicChannels = {}

    if "channels" in channelobj:
        channelliste = channelobj["channels"]
        if type(channelliste) is list:
            for xyz in channelliste:
                publicChannels[xyz["name"]] = xyz["_id"]

    return publicChannels

def choosePublicRoom(_publicChannels):
    # Printer mulige rum
    print("Choose a room to connect:")
    n=1
    for rooms in _publicChannels:
        print(f'{rooms}: {rooms}')
        n = n+1
    
#     # Vælg et rum
#     while True:
#         try:
#             i = int(input(f"Vælg et nummer mellem 1 og {len(_channelsnames)}: "))
#             break
#         except ValueError:
#             print('\nYou did not enter a valid integer')
#         if i < len(_channelsnames):
#             print("\nFail")
#         elif i < 1:
#             print("\nFail")
    
#     return i, _channelsid[i-1]

# def printMessages(RoomNo, _publicRoomID, _msgCount):
#     msg = rocket.channels_history(_publicRoomID, count=_msgCount).json()

#     # Itterer igennem beskeder fra rummet
#     print(f"\n<<< Beskeder fra {cNames[RoomNo-1]} >>>")
#     if "messages" in msg:
#         msgliste = msg["messages"]
#         if type(msgliste) is list:
#             for xyz in reversed(msgliste):
#                 print(f'{xyz["u"]["username"]}:     {xyz["msg"]}')

# #### TEST AF FUNKTIONER ####
createSession(nickname, password)
print(getUserID("christian"))
publicChannels = getPublicChatRooms()
choosePublicRoom(publicChannels)
# printMessages(chosenRoomNo, chosenPublicChatRoom, 10)