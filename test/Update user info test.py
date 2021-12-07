from requests import sessions
from pprint import pprint
from rocketchat_API.rocketchat import RocketChat

username = input("Current username: ")
password = input("Current Password: ")
    

with sessions.Session() as session:
    rocket = RocketChat(username, password, server_url='http://justa.chat:3000/', session=session)
    
    userobj = rocket.me().json()
    userID = userobj["_id"]
    
    new_email = input("Type a new email: ")
    new_name = input("Type a new name: ")
    new_password = input("Type a new password: ")
    new_username = input("Type a new username: ")
    
    pprint(rocket.users_update(userID, email=new_email, name=new_name, password= new_password, username=new_username).json())