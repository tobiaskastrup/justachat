from requests import sessions
from pprint import pprint
from rocketchat_API.rocketchat import RocketChat

user = input("Input username: ")
password = input("Input password: ")

with sessions.Session() as session:
    rocket = RocketChat(
        user, password, server_url='http://justa.chat:3000/', session=session)

    recipient_username = input("Input username: ")
    
    pprint(rocket.im_create(recipient_username).json())
