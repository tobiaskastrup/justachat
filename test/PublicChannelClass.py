class PublicChannels:

    def __init__(self, rocket):
        self.rooms = {}
        self.rocket = rocket
        self.updateRooms()

    def updateRooms(self):
        channelobj = self.rocket.channels_list().json()
        
        if "channels" in channelobj:
            channelliste = channelobj["channels"]
            if type(channelliste) is list:
                for xyz in channelliste:
                    self.rooms[xyz["name"]] = xyz["_id"]

    def choosePublicRoom(self):
        # Printer mulige rum
        print("Choose a room to connect:")
        tempRooms = {}
        n=1
        for rooms in self.rooms:
            tempRooms[n] = rooms
            print(f'{n}: {tempRooms[n]}')
            n = n+1
        
        # Vælg et rum
        while True:
            try:
                i = int(input(f"Vælg et nummer mellem 1 og {len(self.rooms)}: "))
                break
            except ValueError:
                print('\nYou did not enter a valid integer')
            if i < len(self.rooms):
                print("\nFail")
            elif i < 1:
                print("\nFail")
        
        return tempRooms[i]

    def getRoomID(self, roomName) -> str:
        return self.rooms[roomName]

    def printMessages(self, chosenPublicChannel, msgCount):

        msg = self.rocket.channels_history(self.rooms[chosenPublicChannel], count=msgCount).json()

        # Itterer igennem beskeder fra rummet
        print(f"\n<<< Beskeder fra {chosenPublicChannel} >>>")
        if "messages" in msg:
            msgliste = msg["messages"]
            if type(msgliste) is list:
                for xyz in reversed(msgliste):
                    print(f'{xyz["u"]["username"]}:     {xyz["msg"]}')
