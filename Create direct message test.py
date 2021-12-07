from requests import sessions
from pprint import pprint
from rocketchat_API.rocketchat import RocketChat


with sessions.Session() as session:
    nickname = input("Input username: ")
    password = input("Input password: ")
    recipient_username = input("Input recipient username: ")
    rocket = RocketChat(nickname, password, server_url='http://justa.chat:3000/', session=session)
    pprint(rocket.im_create(recipient_username).json())