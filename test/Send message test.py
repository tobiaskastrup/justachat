from requests import sessions
from pprint import pprint
from rocketchat_API.rocketchat import RocketChat

username = input("Input username: ")
password = input("Input password: ")

with sessions.Session() as session:
    room = input("Which channel do you want to send your message?: ")
    message = input("Type message here: ")
    rocket = RocketChat(username, password, server_url='http://justa.chat:3000/', session=session)
    pprint(rocket.chat_post_message(message, channel=room).json())
