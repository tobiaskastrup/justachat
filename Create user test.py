from requests import sessions
from pprint import pprint
from rocketchat_API.rocketchat import RocketChat

import re
pattern = "^.*(?=.{8,})(?=.*\d)(?=.*[a-zøæå])(?=.*[A-ZÆØÅ)(?=.*[$&+,:;=?@#|'<>.-^*()%!_]).*$"
nickname = input("Type your username: ")
username = input("Type your first name: ")

while True:
    password = input("Type a password here: ")
    result = re.findall(pattern, password)
    if (result):
        print("Password is okay!")
        break
    else:
        print("Password doesn't meet the requirments")



with sessions.Session() as session:
    rocket = RocketChat('UserCreateAdmin', 'SuperStrong123!',server_url='http://justa.chat:3000/', session=session)
    pprint(rocket.users_create(username+'@justa.chat', username, password, nickname).json())