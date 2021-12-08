from pprint import pprint
class MyUser:

    def __init__(self,rocket, username=None):
        self.username = username
        self.id = None
        self.rocket = rocket
        self.status = None
        self.statusText = None
        if username is not None:
            self.updateUser()
        #else:
            #
        

    def updateUser(self):
        userObj = self.rocket.me().json()
        #pprint(userObj)
        if userObj["_id"] is not None:
            self.statusText = userObj['statusText']
            self.status = userObj["status"]
            self.id = userObj["_id"]
        
    def getStatusText(self) -> str:
        return self.statusText

    def getStatus(self) -> str:
        return self.status

    def getID(self) -> str:
        return self.id

    def getUsername(self) -> str:
        return self.username

    def setUserStatus(self, status_msg=None, set_avail=None):

        if set_avail is None:
            set_avail = self.status

        if status_msg is None:
            status_msg = self.statusText

        self.rocket.users_set_status(message=status_msg, status=set_avail).json()
        self.updateUser()