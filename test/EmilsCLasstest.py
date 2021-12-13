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
        

createSession(nickname, password)
myUser = MyUser(username=nickname, rocket=rocket)

# myUser.setUserStatus("Bla", None)  
# print(myUser.getStatusText()) 
# print(myUser.getStatus())

tobias = OtherUsers("tobias", rocket)
pprint(rocket.im_list().json())
# pprint(tobias.getID())
# myUser = MyUser(username=nickname, rocket=rocket)

# im_room = IM(rocket, myUser.getUsername())
# chosenIMRoom = im_room.chooseMyRoom()
# print(im_room.deleteIMChannel(chosenIMRoom))


publicRooms = PublicChannels(rocket)
#cRoom = publicRooms.chooseMyRoom()
# print(publicRooms.closeChannel(cRoom))

# print(publicRooms.inviteUser(cRoom, tobias))

# print(myUser.getID())
# print(publicRooms.getRoomID(cRoom))
# publicRooms.printMessages(cRoom, 15)
