# Rocketchat #
##############

mongoserver="10.1.2.7"
rocketadmin="rockadmin"
rocketmail="admin@enode.dk"
rocketpass="Mahman"

sudo apt -y update && sudo apt install -y curl && curl -sL https://deb.nodesource.com/setup_12.x | sudo bash -

sudo apt update
sudo apt install -y build-essential nodejs graphicsmagick

#Install inherits and n.
sudo npm install -g inherits n

#Create a symbolic link for the node binary file to
sudo ln -s /usr/bin/node /usr/local/bin/node

###### Install Rocket.Chat ########
#Download the latest version of Rocket.Chat with the following

curl -L https://releases.rocket.chat/latest/download -o /tmp/rocket.chat.tgz

#Extract the downloaded file to /tmp folder
tar -xzf /tmp/rocket.chat.tgz -C /tmp

#Install Rocket.Chat to a directory of your choice. 
#In this guide, we shall install it in /opt directory

cd /tmp/bundle/programs/server && npm install
cd ~/
sudo mv /tmp/bundle /opt/Rocket.Chat

#Create a rocketchat user and assign ownership to the Rocket.Chat folder.
sudo useradd -M rocketchat && sudo usermod -L rocketchat
sudo chown -R rocketchat:rocketchat /opt/Rocket.Chat

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

sudo systemctl enable rocketchat && sudo systemctl start rocketchat

sudo ufw allow from 10.1.0.5 to any port 3000
sudo ufw allow ssh
sudo ufw --force enable

sleep 30

sudo systemctl restart rocketchat

sleep 30

sudo systemctl restart rocketchat