class DM:

    def __init__(self, rocket, myUsername):
        self.rooms = {}
        self.rocket = rocket
        self.myUsername = myUsername
        self.lastMsg = {}
        self.newMsg = {}

        self.updateMyRooms()
        self.checkForFirstMsg()


# Create/Start Direct Message
    def createDMRoom(self, username):
       createDMResponse = self.rocket.im_create(username).json()
       return createDMResponse['success']

    def sendNewMsg(self, recipient, msg) -> bool:
        sendMsgRespond = self.rocket.chat_post_message(msg, channel=self.rooms[recipient]).json()
        return sendMsgRespond["success"]

    
    def checkForFirstMsg(self) -> list:
        lastMessagesObj = self.rocket.im_list().json()

        if "ims" in lastMessagesObj:
            lastMsgListe = lastMessagesObj["ims"]
            if type(lastMsgListe) is list:
                for xyz in lastMsgListe:
                    usernames = xyz["usernames"]
                    for users in usernames:
                        if users != self.myUsername:
                            self.newMsg[users] = xyz["lastMessage"]["msg"]
        
        for newMessages in self.newMsg:
            if newMessages not in self.lastMsg:
                self.lastMsg[newMessages] = self.newMsg[newMessages]

    def checkForNewMsg(self) -> list:
        lastMessagesObj = self.rocket.im_list().json()

        if "ims" in lastMessagesObj:
            lastMsgListe = lastMessagesObj["ims"]
            if type(lastMsgListe) is list:
                for xyz in lastMsgListe:
                    usernames = xyz["usernames"]
                    for users in usernames:
                        if (users != self.myUsername) and (xyz["lastMessage"]["u"]["username"] != self.myUsername):
                            self.newMsg[users] = xyz["lastMessage"]["msg"]
        
        newMsgFromUsers = []

        for newMessages in self.newMsg:
            if self.lastMsg[newMessages] != self.newMsg[newMessages]:
                newMsgFromUsers.append(newMessages)
                self.lastMsg[newMessages] = self.newMsg[newMessages]
                
        
        print("3 Last msgs: ", self.lastMsg)
        print("3 New msg: ", self.newMsg)
        
        return newMsgFromUsers
                
#Direct Message History, pprint(rocket.im_history('room_id').json()) Mangler i DMClass
    def printMessages(self, chosenDMChannel):
    # '''Printer beskeder fra en channel'''
        msg = self.rocket.im_history(self.rooms[chosenDMChannel]).json()

        # Itterer igennem beskeder fra rummet
        print(f"\n<<< Beskeder fra {chosenDMChannel} >>>")
        if "messages" in msg:
            msgliste = msg["messages"]
            if type(msgliste) is list:
                for xyz in reversed(msgliste):
                    print(f'{xyz["u"]["username"]}:     {xyz["msg"]}')

# Choose what room you want
    def chooseMyRoom(self):
        '''Vælger et rum fra egen channel liste'''
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

# Lists Members in Direct Message, pprint(rocket.im_members('room_id').json()) Mangler i DMClass
    def listMembers(self):
        pprint(self.rocket.im_members('room_id').json())

# Lists All Direct Messages, pprint(rocket.im_list().json()) Mangler i DMClass
    def updateMyRooms(self):
        '''Opdaterer brugerens egen channel liste'''
        mychannelobj = self.rocket.im_list().json()
        
        if "ims" in mychannelobj:
            channelliste = mychannelobj["ims"]
            if type(channelliste) is list:
                for xyz in channelliste:
                    usernames = xyz["usernames"]
                    for users in usernames:
                        if users != self.myUsername:
                            self.rooms[users] = xyz["_id"]    

# "Delete" a Direct Message, pprint(rocket.im_close('room_id').json()) Mangler i DMClass
    def deleteDMChannel(self, chosenDMChannel):
        deleteDMResponse = self.rocket.im_close(self.rooms[chosenDMChannel]).json()
        return deleteDMResponse['success']
        
