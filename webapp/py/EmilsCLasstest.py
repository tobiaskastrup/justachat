from requests import sessions
from pprint import pprint
from rocketchat_API.rocketchat import RocketChat
from rocketchat_API.APIExceptions.RocketExceptions import RocketAuthenticationException
from MyUser import MyUser
from Channels import PublicChannels
from OtherUsers import OtherUsers
from DirectMessages import DM


# nickname = input("Username: ")
# password = input("Password: ")

serverURL = 'http://justa.chat:3000/'
nickname = "emil"
password = "SuperStrong123!"
errormsg = ""

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
        

# createAnonSession()
# anonrocket.users_register("peter@justa.chat", "Peter P", "Mahman", "peter")

### OBJEKTER ###
createSession(nickname, password)
myUser = MyUser(username=nickname, rocket=rocket)
# tobias = OtherUsers("tobias", rocket)
# im_room = IM(rocket, myUser.getUsername())
# publicRooms = PublicChannels(rocket)

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
