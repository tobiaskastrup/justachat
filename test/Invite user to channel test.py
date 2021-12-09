from requests import sessions
from pprint import pprint
from rocketchat_API.rocketchat import RocketChat

nickname = "christian"
password = "SuperStrong123!"

userID = '4iwtXDRrYFqikHxhL'
roomID = 'M6C4s9HKTZXznmTS4'

with sessions.Session() as session:
    rocket = RocketChat(nickname, password, server_url='http://justa.chat:3000/', session=session)
    pprint(rocket.channels_invite(roomID, userID).json())