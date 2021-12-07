
```from requests import sessions
from pprint import pprint
import json
from rocketchat_API.rocketchat import RocketChat

user = input('Indtast dit brugernavn: ')
password = input('Indtast dit password: ')

with sessions.Session() as session:
    # Opretter en session med login oplysninger
    rocket = RocketChat(user, password, server_url='http://justa.chat:3000', session=session)

    # Henter user ID for brugeren
    userobj = rocket.me().json()
    if userobj["_id"] is not None:
        userID = userobj["_id"]

    channelobj = rocket.channels_list().json()

    # Henter mulige rum
    channelsnames = []
    channelsid = []
    if "channels" in channelobj:
        channelliste = channelobj["channels"]
        if type(channelliste) is list:
            for xyz in channelliste:
                channelsnames.append(xyz["name"])
                channelsid.append(xyz["_id"])
        
        # Printer mulige rum
        print("Choose a room to connect:")
        n=1
        for rooms in channelsnames:
            print(f'{n}: {rooms}')
            n = n+1
        
        # Vælg et rum
        while True:
            try:
                i = int(input(f"Vælg et nummer mellem 1 og {len(channelsnames)}: "))
                break
            except ValueError:
                print('\nYou did not enter a valid integer')
            if i < len(channelsnames):
                print("\nFail")
            elif mark < 1:
                print("\nFail")
        
        # Henter beskeder fra valgte rum
        msg = rocket.channels_history(channelsid[i-1], count=10).json()

        # Itterer igennem beskeder fra rummet
        print(f"\n<<< Beskeder fra {channelsnames[i-1]} >>>")
        if "messages" in msg:
            msgliste = msg["messages"]
            if type(msgliste) is list:
                for xyz in reversed(msgliste):
                    print(f'{xyz["u"]["username"]}:     {xyz["msg"]}')```