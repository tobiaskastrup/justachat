################################################
#           Rocket.chat server setup           #
################################################
#
# Installere Rocket.chat, som er vores backend
# server til vores chat funktion. Minder om
# ejabberd som kører over XMPP protokollen,
# men mere udbygget og med bedre API support
# Support: https://docs.rocket.chat/
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

# Rocket chat variabler (skal muligvis ændres)
mongoserver="10.1.2.7"
rocketadmin="rockadmin"
rocketmail="admin@enode.dk"
rocketpass="Mahman"

# Tilføjer nodejs repository til apt
sudo apt -y update && sudo apt install -y curl && curl -sL https://deb.nodesource.com/setup_12.x | sudo bash -

# Apt update og henter build-essential, nodejs og graphicsmagick
sudo apt update
sudo apt install -y build-essential nodejs graphicsmagick

#Installere inherits og n.
sudo npm install -g inherits n
sudo npm install bcrypt

#Opretter en symbolic link for nodens binære fil til
sudo ln -s /usr/bin/node /usr/local/bin/node

###### Install Rocket.Chat ########
#Henter den seneste version af Rocket.Chat med det følgende:

curl -L https://releases.rocket.chat/latest/download -o /tmp/rocket.chat.tgz

# Udpakker den downloadede fil til /tmp mappen
tar -xzf /tmp/rocket.chat.tgz -C /tmp

#Installerer Rocket.Chatt til /opt/Rocket.Chat

cd /tmp/bundle/programs/server && npm install
cd ~/
sudo mv /tmp/bundle /opt/Rocket.Chat

#Create a rocketchat user and assign ownership to the Rocket.Chat folder.
sudo useradd -M rocketchat && sudo usermod -L rocketchat
sudo chown -R rocketchat:rocketchat /opt/Rocket.Chat

# Fixer fejl ved 
npm audit fix

############################
#
#
#############################

cat << EOF |sudo tee -a /etc/systemd/system/rocketchat.service
[Unit]
Description=The Rocket.Chat server
After=network.target remote-fs.target nss-lookup.target nginx.service mongod.service
[Service]
ExecStart=/usr/local/bin/node /opt/Rocket.Chat/main.js
StandardOutput=syslog
StandardError=syslog
SyslogIdentifier=rocketchat
User=rocketchat
Environment=MONGO_URL=mongodb://$mongoserver:27017/rocketchat?replicaSet=rs01
Environment=MONGO_OPLOG_URL=mongodb://$mongoserver:27017/local?replicaSet=rs01 
Environment=ROOT_URL=http://admin.justa.chat
Environment=PORT=3000
Environment=ADMIN_USERNAME=$rocketadmin
Environment=ADMIN_EMAIL=$rocketmail
Environment=ADMIN_PASS=$rocketpass
[Install]
WantedBy=multi-user.target
EOF

# Enabler og starter servicen
sudo systemctl enable rocketchat && sudo systemctl start rocketchat

############### UFW (Firewall) ################
#
# Vi opsætter en UFW (Uncomplicated Firewall)
# som kun tillader forbindelse fra webserver over
# port 3000, samt SSH er åbne i vores VM
# fra Bastion subnettet
#
################################################
sudo ufw allow from 10.1.0.5 to any port 3000
sudo ufw allow from 10.1.3.0/24 to any port 22 #SSH from bastion
sudo ufw --force enable

# Restart 2 gange, da den ikke altid når at have alting klar når
# servicen starter.
sleep 30 # pauser koden i 30 sek
sudo systemctl restart rocketchat
sleep 30
sudo systemctl restart rocketchat