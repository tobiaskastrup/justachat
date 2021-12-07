from requests import sessions
from pprint import pprint
from rocketchat_API.rocketchat import RocketChat

nickname = input("Username: ")
password = input("Password: ")

with sessions.Session() as session:
    rocket = RocketChat(nickname, password, server_url='http://justa.chat:3000/', session=session)
    pprint(rocket.me().json())