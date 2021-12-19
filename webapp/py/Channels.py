from pprint import pprint

class PublicChannels:

    def __init__(self, rocket):
        self.rooms = {}
        self.myRooms = {}
        self.rocket = rocket
        self.updateAllRooms()
        self.updateMyRooms()

    def updateAllRooms(self):
        '''Opdaterer alle channels'''
        channelobj = self.rocket.channels_list().json()
        
        if "channels" in channelobj:
            channelliste = channelobj["channels"]
            if type(channelliste) is list:
                for xyz in channelliste:
                    self.rooms[xyz["name"]] = xyz["_id"]

    def getMyRoomsAsLists(self) -> list:
        '''Retunerer alle rummenes navn, man er i, som en list'''

        self.updateMyRooms()

        tempRoomsNames = []
        n=1
        for name, id in self.myRooms.items():
            tempRoomsNames.append(name)
            n = n+1

        return tempRoomsNames
        
    def getMyRooms(self) -> dict:
        '''Retunere alle rum man self er i som et dict'''
        self.updateMyRooms()
        return self.myRooms

    def getRoomID(self, roomName) -> str:
        '''Returnerer Channel ID'''
        return self.rooms[roomName]

    def updateMyRooms(self) -> str:
        '''Opdaterer brugerens egen channel liste'''
        mychannelobj = self.rocket.channels_list_joined().json()
        
        if "channels" in mychannelobj:
            channelliste = mychannelobj["channels"]
            if type(channelliste) is list:
                for xyz in channelliste:
                    self.myRooms[xyz["name"]] = xyz["_id"]

    def getMessages(self, channelID, msgCount) -> tuple:
        msg = self.rocket.channels_history(channelID, count=msgCount).json()

        cleanedName = []
        cleanedMsg = []
        
        # Itterer igennem beskeder fra rummet
        if "messages" in msg:
            msgliste = msg["messages"]
            if type(msgliste) is list:
                for xyz in reversed(msgliste):
                    cleanedName.append(xyz["u"]["username"])
                    cleanedMsg.append(xyz["msg"])

                    
        return cleanedName, cleanedMsg

    #########################################################################   
    #                     IKKE IMPLEMENTERET I APP.PY                       #
    #########################################################################

    def inviteUser(self, roomName, userObject) -> bool:
        '''Inviterer en bruger til en channel'''
        roomID = self.myRooms[roomName]
        userID = userObject.getID()
        inviteResponse = self.rocket.channels_invite(roomID, userID).json()
        return inviteResponse["success"]

    def createChannel(self, newChannelName) -> bool:
        '''Laver en ny channel'''
        newChannelNameResponse = self.rocket.channels_create(newChannelName).json()
        return newChannelNameResponse["success"]

    def deleteChannel(self, roomName) -> bool:
        '''Sletter en Channel'''
        roomID = self.rooms[roomName]
        deleteResponse = self.rocket.channels_delete(roomID).json()
        return deleteResponse["success"]

    #########################################################################
    #                                 DEBUG                                 #
    #########################################################################

    def chooseMyRoom(self):
        '''Vælger et rum fra egen channel liste'''
        # Printer mulige rum
        print("Choose a room to connect:")
        tempRooms = {}
        n=1
        for rooms in self.myRooms:
            tempRooms[n] = rooms
            print(f'{n}: {tempRooms[n]}')
            n = n+1
        
        # Vælg et rum
        while True:
            try:
                i = int(input(f"Vælg et nummer mellem 1 og {len(self.myRooms)}: "))
                break
            except ValueError:
                print('\nYou did not enter a valid integer')
            if i < len(self.myRooms):
                print("\nFail")
            elif i < 1:
                print("\nFail")
        
        return tempRooms[i]
    def printMessages(self, chosenPrivateChannel, msgCount):
    '''Printer beskeder fra en channel'''
    msg = self.rocket.channels_history(self.myRooms[chosenPrivateChannel], count=msgCount).json()

    # Itterer igennem beskeder fra rummet
    print(f"\n<<< Beskeder fra {chosenPrivateChannel} >>>")
    if "messages" in msg:
        msgliste = msg["messages"]
        if type(msgliste) is list:
            for xyz in reversed(msgliste):
                print(f'{xyz["u"]["username"]}:     {xyz["msg"]}')