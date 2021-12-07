from requests import sessions
from pprint import pprint
from rocketchat_API.rocketchat import RocketChat

userID = '976W3MHhz6mFTSL6z'
channelID = 'a4G7QCvzYyfjHrQMu'

with sessions.Session() as session:
    nickname = input("Input username: ")
    password = input("Input password: ")
    room_id = input("Input room id: ")
    recipient_user_id = input("Input recipient user id: ")
    rocket = RocketChat(nickname, password, server_url='http://justa.chat:3000/', session=session)
    pprint(rocket.channels_invite(room_id, recipient_user_id).json())