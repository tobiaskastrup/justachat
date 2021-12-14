from pprint import pprint

class IM:

    def __init__(self, rocket, myUsername):
        self.rooms = {}
        self.rocket = rocket
        self.myUsername = myUsername
        self.lastMsg = {}
        self.newMsg = {}

        self.updateMyRooms()
        self.checkForFirstMsg()


# Create/Start Direct Message
    def createImRroom(self, username):
       createIMResponse = self.rocket.im_create(username).json()
       return createIMResponse['success']

#Lists Latest Direct Message in ALL DM Channels, pprint(rocket.im_list_everyone().json()) Mangler i IMClass
    # def list_latest(self):
    #     pprint(self.rocket.im_list_everyone().json())

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
                

#Direct Message History, pprint(rocket.im_history('room_id').json()) Mangler i IMClass
    def printMessages(self, chosenIMChannel):
    # '''Printer beskeder fra en channel'''
        msg = self.rocket.im_history(self.rooms[chosenIMChannel]).json()

        # Itterer igennem beskeder fra rummet
        print(f"\n<<< Beskeder fra {chosenIMChannel} >>>")
        if "messages" in msg:
            msgliste = msg["messages"]
            if type(msgliste) is list:
                for xyz in reversed(msgliste):
                    print(f'{xyz["u"]["username"]}:     {xyz["msg"]}')

#HEr er ny funktion
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




# Lists Members in Direct Message, pprint(rocket.im_members('room_id').json()) Mangler i IMClass
    def list_members(self):
        pprint(self.rocket.im_members('room_id').json())

# Lists All Direct Messages, pprint(rocket.im_list().json()) Mangler i IMClass
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

# Lists Direct Message Counters, pprint(rocket.im_counters('room_id', 'username').json()) Mangler i IMClass
    def list_direct_counters(self):
        pprint(self.rocket.im_counters('room_id', 'username').json())

# "Delete" a Direct Message, pprint(rocket.im_close('room_id').json()) Mangler i IMClass
    def deleteIMChannel(self, chosenIMChannel):
        deleteIMResponse = self.rocket.im_close(self.rooms[chosenIMChannel]).json()
        return deleteIMResponse['success']
        

# "Reopen" a Direct Message, pprint(rocket.im_open('room_id').json()) Mangler i IMClass
    def reopen_dm(self):
        pprint(self.rocket.im_open('room_id').json())
