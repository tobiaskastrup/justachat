from requests import sessions
from pprint import pprint
from rocketchat_API.rocketchat import RocketChat
from MyUserClass import MyUser
from PublicChannelClass import PublicChannels
from OtherUsersClass import OtherUsers

# nickname = input("Username: ")
# password = input("Password: ")

nickname = "christian"
password = "SuperStrong123!"

def createSession(_nickname, _password):
    with sessions.Session() as session:
        global rocket
        rocket = RocketChat(_nickname, _password, server_url='http://justa.chat:3000/', session=session)
        #rocket.users_set_status())
        

createSession(nickname, password)
myUser = MyUser(username=nickname, rocket=rocket)



# myUser.setUserStatus("Bla", None)  
# print(myUser.getStatusText()) 
# print(myUser.getStatus())

# tobias = OtherUsers("tobias", rocket)
# pprint(tobias.getUsername())
# myUser = MyUser(username=nickname, rocket=rocket)


# publicRooms = PublicChannels(rocket)
# print(myUser.getID())
# cRoom = publicRooms.choosePublicRoom()
# print(publicRooms.getRoomID(cRoom))
#publicRooms.printMessages(cRoom, 15)
