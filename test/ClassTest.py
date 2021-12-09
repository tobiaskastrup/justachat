from requests import sessions
from pprint import pprint
from rocketchat_API.rocketchat import RocketChat
from MyUserClass import MyUser
from ChannelClass import PublicChannels
from OtherUsersClass import OtherUsers

nickname = "christian"
password = "SuperStrong123!"

def createSession(_nickname, _password):
    with sessions.Session() as session:
        global rocket
        rocket = RocketChat(_nickname, _password, server_url='http://justa.chat:3000/', session=session)
        

def getAllUsers(self):
    allUserObj = self.rocket.users_list().json().json()
        if allUserObj["user"] is not None:
            self.status = allUserObj["user"]["status"]
            self.statusText = allUserObj["user"]['statusText']
            self.id = allUserObj["user"]["_id"]
            self.email = allUserObj["user"]["emails"]
            self.roles = allUserObj["user"]["roles"]
            self.active = allUserObj["user"]["active"]

createSession(nickname, password)
myUser = MyUser(username=nickname, rocket=rocket)

# myUser.setUserStatus("Bla", None)  
# print(myUser.getStatusText()) 
# print(myUser.getStatus())

# tobias = OtherUsers("tobias", rocket)
# pprint(tobias.getID())
# myUser = MyUser(username=nickname, rocket=rocket)

# publicRooms = PublicChannels(rocket)
# cRoom = publicRooms.chooseMyRoom()
# print(publicRooms.closeChannel(cRoom))

# print(publicRooms.inviteUser(cRoom, tobias))

# print(myUser.getID())
# print(publicRooms.getRoomID(cRoom))
# publicRooms.printMessages(cRoom, 15)