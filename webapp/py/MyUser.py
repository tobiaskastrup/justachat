from pprint import pprint
class MyUser:

    def __init__(self,rocket, username=None):
        self.username = username
        self.id = None
        self.rocket = rocket
        self.status = None
        self.statusText = None
        self.displayName = None
        self.email = None

        if username is not None:
            self.updateUser()
        #else:
            #
        

    def updateUser(self):
        # Laver et objekt der kan bruges til at opdatere brugers info.
        userObj = self.rocket.me().json()
        # Hvis bruger info ikke eksisterer lægges det i en dictionary.
        if '_id' in userObj:
            if "statusText" in userObj:
                self.statusText = userObj['statusText']
            self.status = userObj["status"]
            self.id = userObj["_id"]
            self.displayName = userObj["name"]
            self.email = userObj["emails"][0]["address"]

    def getMail(self) -> str:
        self.updateUser()
        return self.email

    def getDisplayName(self) -> str:
        self.updateUser()
        return self.displayName
        
    def getStatusText(self) -> str:
        # Returnerer statusText fra updateUser.
        self.updateUser()
        return self.statusText

    def getStatus(self) -> str:
        # Returnerer status fra updateUser.
        self.updateUser()
        return self.status

    def getID(self) -> str:
        # Returnerer eget ID fra updateUser.
        return self.id

    def getUsername(self) -> str:
        self.updateUser()
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