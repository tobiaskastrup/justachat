from requests import sessions
from pprint import pprint
from rocketchat_API.rocketchat import RocketChat

username = input("Current username: ")
password = input("Current Password: ")


with sessions.Session() as session:
    rocket = RocketChat(username, password,
                        server_url='http://justa.chat:3000/', session=session)

    user_id = input("Type the name of the user to be deleted: ")
    delobj = rocket.users_info(user_id).json()
    if delobj["user"] is not None:
        userID = delobj["user"]["_id"]
        pprint(rocket.users_delete(userID))