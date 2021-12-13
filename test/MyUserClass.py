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
        # Laver et objekt der kan bruges til at opdatere brugers info.
        userObj = self.rocket.me().json()
        # Hvis bruger info ikke eksisterer lægges det i en dictionary.
        if userObj["_id"] is not None:
            self.statusText = userObj['statusText']
            self.status = userObj["status"]
            self.id = userObj["_id"]
        
    def getStatusText(self) -> str:
        # Returnerer statusText fra updateUser.
        return self.statusText

    def getStatus(self) -> str:
        # Returnerer status fra updateUser.
        return self.status

    def getID(self) -> str:
        # Returnerer eget ID fra updateUser.
        return self.id

    def getUsername(self) -> str:
        return self.username

    def setUserStatus(self, status_msg=None, set_avail=None):
        '''Sætter en availability status & status besked for brugeren for brugeren.'''
        # Hvis der ikke sættes en ny availability status, bruges den sidste status.
        if set_avail is None:
            set_avail = self.status

        # Hvis der ikke sættes en ny status besked, bruges den sidste status.
        if status_msg is None:
            status_msg = self.statusText

        self.rocket.users_set_status(message=status_msg, status=set_avail).json()
        self.updateUser()

    def getAllUsers(self):
        '''Tager Information fra brugere og lægger det i en Dictionary'''
        allUserObj = self.rocket.users_list().json()
        
        allUsers = {}

        if "users" in allUserObj:
            userList = allUserObj["users"]
            if type(userList) is list:
                for xyz in userList:
                    if xyz["username"] != self.username:
                        allUsers = {xyz["username"]: [{"Username": xyz["username"],
                        "Id": xyz["_id"],
                        "Status": xyz["status"],
                        #"Email": xyz["email"]["address"],
                        "Roles": xyz["roles"],
                        "Active": xyz["active"]}]
        return allUsers
        