from requests import sessions
from pprint import pprint
from rocketchat_API.rocketchat import RocketChat
from MyUserClass import MyUser
from ChannelClass import PublicChannels
from OtherUsersClass import OtherUsers
from IMClass import IM


# nickname = input("Username: ")
# password = input("Password: ")

nickname = "emil"
password = "SuperStrong123!"

def createSession(_nickname, _password):
    with sessions.Session() as session:
        global rocket
        rocket = RocketChat(_nickname, _password, server_url='http://justa.chat:3000/', session=session)
        #rocket.users_set_status())
        

def createAnonSession():
    with sessions.Session() as session:
        global anonrocket
        anonrocket = RocketChat(server_url='http://justa.chat:3000/', session=session)

# createAnonSession()
# anonrocket.users_register("peter@justa.chat", "Peter P", "Mahman", "peter")

### OBJEKTER ###
createSession(nickname, password)
myUser = MyUser(username=nickname, rocket=rocket)
tobias = OtherUsers("tobias", rocket)
im_room = IM(rocket, myUser.getUsername())
publicRooms = PublicChannels(rocket)

# myUser.setUserStatus("Bla", None)  
# print(myUser.getStatusText()) 
# print(myUser.getStatus())


### USER TESTS ###
# pprint(tobias.getID())
# myUser = MyUser(username=nickname, rocket=rocket)


### IM TESTS ###
# chosenIMRoom = im_room.chooseMyRoom()
# sendMsg = input("Hvad vil du sende: ")
# im_room.sendNewMsg(chosenIMRoom, sendMsg)
# print(im_room.checkForNewMsg())

# chosenIMRoom = im_room.chooseMyRoom()
# print(im_room.deleteIMChannel(chosenIMRoom))



#cRoom = publicRooms.chooseMyRoom()
# print(publicRooms.closeChannel(cRoom))

# print(publicRooms.inviteUser(cRoom, tobias))

# print(myUser.getID())
# print(publicRooms.getRoomID(cRoom))
# publicRooms.printMessages(cRoom, 15)
