from requests import sessions
from pprint import pprint
from rocketchat_API.rocketchat import RocketChat

with sessions.Session() as session:
    nickname = input("Input username: ")
    password = input("Input password: ")
    room = input("Which channel do you want to send your message?: ")
    message = input("Type message here: ")
    rocket = RocketChat(nickname, password, server_url='http://justa.chat:3000/', session=session)
    pprint(rocket.chat_post_message(message, channel=room).json())
