from pprint import pprint

class IM:

    def __init__(self, rocket):
        self.rooms = {}
        self.rocket = rocket


# Create/Start Direct Message
    def createImRroom(self, username):
       IM(self.rocket.im_create(username).json())
      # return 

#Lists Latest Direct Message in ALL DM Channels, pprint(rocket.im_list_everyone().json()) Mangler i IMClass
    def list_latest(self):
        pprint(self.rocket.im_list_everyone().json())

#Direct Message History, pprint(rocket.im_history('room_id').json()) Mangler i IMClass
    def message_history(self):
        pprint(self.rocket.im_history('room_id').json())

# Lists Members in Direct Message, pprint(rocket.im_members('room_id').json()) Mangler i IMClass
    def list_members(self):
        pprint(self.rocket.im_members('room_id').json())

# Lists All Direct Messages, pprint(rocket.im_list().json()) Mangler i IMClass
    def list_all_dms(self):
        pprint(self.rocket.im_list().json())

# Lists Direct Message Counters, pprint(rocket.im_counters('room_id', 'username').json()) Mangler i IMClass
    def list_direct_counters(self):
        pprint(self.rocket.im_counters('room_id', 'username').json())

# "Delete" a Direct Message, pprint(rocket.im_close('room_id').json()) Mangler i IMClass
    def del_dm(self):
        pprint(self.rocket.im_close('room_id').json())

# "Reopen" a Direct Message, pprint(rocket.im_open('room_id').json()) Mangler i IMClass
    def reopen_dm(self):
        pprint(self.rocket.im_open('room_id').json())
