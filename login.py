from requests import sessions
from rocketchat_API.rocketchat import RocketChat


attempts = 1

with sessions.Session() as session:

    # Henter user ID for brugeren


    while attempts < 4:
    #Brugeren har tre forsøg til at få sit brugernavn og kodeord korrekt
        nickname = input("Username: ")
        password = input("Password: ")

        try:
            rocket = RocketChat(nickname, password, server_url='http://justa.chat:3000/', session=session) #Fra rocket skal hentes: brugernavn, passwor, server url og session
            userobj = rocket.me().json() #henter på denne måde det nødvendige data via json, som vi kan matche login oplysninger med
        except Exception as e:
            print(f'You got: {e}')

        try:
            if userobj["success"] is True: #Netop success er json navnet for om login session er succesfuld, og det matcher de loginoplysninger der allerede er lavet i rocketchat
                print("Welcome! :-)")
                break
            else:
                print("Incorrect, please try again.") #Dette bruges lige nu ikke grundet exception
        except NameError:
            print("Login object wasn't created")

        attempts += 1
        print(f'Number of attempts left: {4 - attempts}') #Taster man forkerte detaljer ind, fortæller programmet hvor mange forsøg der er tilbage