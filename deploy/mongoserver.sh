################################################
#             MongoDB server setup             #
################################################
#
# Installere MongoDB, som er vores backed 
# database til justa.chat
#
# Fra Wikipedia:
# "MongoDB er et dokumentorienteret databaseprogram.
# Klassificeret som et NoSQL-databaseprogram 
# bruger MongoDB JSON-lignende dokumenter med 
# valgfri skemaer."
#
#################### How to #####################
#
# > nano install.sh
# Tilføj scriptet til install.sh og gem
# > sudo chmod a+x install.sh
# Kør som følgende (vigtigt med 2 x . !):
# > . ./install.sh
#
################################################

# Tilføjer mongodb repository til apt
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 9DA31620334BD75D9DCB49F368818C72E52529D4
wget -qO - https://www.mongodb.org/static/pgp/server-4.4.asc | sudo apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/4.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.4.list

# Opdatere apt og installere build-essential og mongodb-org
sudo apt update
sudo apt install -y build-essential mongodb-org

#################
# Vi skal tilføje DB serverens egen IP til dens config sådan her:
#################

# Gemmer vores interne IP adresse som MYHOSTIP
MYHOSTIP=$(hostname -I)
FILENAME="/etc/mongod.conf"

# Tilføjer vores internet IP til mongo konfiguration
# så den lytter til netværket og tillader forbindelser
# som kommer udenfra serveren. Default er kan mongodb
# kun bruges internt på serveren.
ORIGINAL_STRING="  bindIp: 127.0.0.1"
NEW_STRING="  bindIp: 127.0.0.1, $MYHOSTIP"
sudo sed -i "s/${ORIGINAL_STRING}/${NEW_STRING}/g" $FILENAME

# Mongo servicen startes
sudo systemctl start mongod

# Konfigurere storage engine og replication for MongoDB
# Kræver den har været startet en gang.
sudo sed -i "s/^# engine:/ engine: mmapv1/" /etc/mongod.conf
sudo sed -i "s/^#replication:/replication:\n replSetName: rs01/" /etc/mongod.conf


#Restart og enable MongoDB servicen
sudo systemctl daemon-reload
sudo systemctl enable mongod && sudo systemctl restart mongod

# DEBUG (test om rs01 replication set er oprettet)
# mongo --eval "printjson(rs.initiate())"

############### UFW (Firewall) ################
#
# Vi opsætter en UFW (Uncomplicated Firewall)
# som kun tillader forbindelse fra rocketserveren
# over port 3000, samt SSH er åbne i vores VM
# fra Bastion subnettet
#
################################################
sudo ufw allow from 10.1.1.6 to any port 27017
sudo ufw allow from 10.1.3.0/24 to any port 22 #SSH from bastion
sudo ufw --force enable