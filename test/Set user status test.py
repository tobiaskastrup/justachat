from requests import sessions
from pprint import pprint
from rocketchat_API.rocketchat import RocketChat

with sessions.Session() as session:
    nickname = input("Current username: ")
    password = input("Current Password: ")
    rocket = RocketChat(nickname, password, server_url='http://justa.chat:3000/', session=session)
    status_to_display = input("Input status to display: ")
    set_status = input("Are you 'online/offline/away/busy?: ")
    pprint(rocket.users_set_status(message=status_to_display, status=set_status).json())