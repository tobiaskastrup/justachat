#########################################################################
#                              OTHERUSERS                               #
#########################################################################
#
#       Klasse som skal bruges til opdatere andre brugers data
#
#                   ER IKKE BLEVET IMPLEMENTERET!
#
#########################################################################

from pprint import pp, pprint
from rocketchat_API.rocketchat import RocketChat


class OtherUsers:

    def __init__(self, username, rocket):
        self.username = username
        self.id = None
        self.status = None
        self.rocket = rocket
        self.statusText = None
        self.updateUser()

    def updateUser(self):
        otherUserObj = self.rocket.users_info(self.username).json()
        if otherUserObj["user"] is not None:
            self.status = otherUserObj["user"]["status"]
            self.id = otherUserObj["user"]["_id"]
            self.statusText = otherUserObj["user"]['statusText']

    def getStatusText(self) -> str:
        return self.statusText

    def getStatus(self) -> str:
        return self.status

    def getID(self) -> str:
        return self.id

    def getUsername(self) -> str:
        return self.username
        