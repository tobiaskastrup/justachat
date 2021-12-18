#############
# DB Server #
#############

sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 9DA31620334BD75D9DCB49F368818C72E52529D4
wget -qO - https://www.mongodb.org/static/pgp/server-4.4.asc | sudo apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/4.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.4.list
sudo apt update
sudo apt-get install -y build-essential mongodb-org

#################
# Vi skal tilføje DB serverens egen IP til dens config sådan her:
#################

MYHOSTIP=$(hostname -I)
FILENAME="/etc/mongod.conf"

ORIGINAL_STRING="  bindIp: 127.0.0.1"
NEW_STRING="  bindIp: 127.0.0.1, $MYHOSTIP"

sudo sed -i "s/${ORIGINAL_STRING}/${NEW_STRING}/g" $FILENAME

sudo systemctl start mongod


#Configure the storage engine and replication for MongoDB then start MongoDB service.
sudo sed -i "s/^# engine:/ engine: mmapv1/" /etc/mongod.conf
sudo sed -i "s/^#replication:/replication:\n replSetName: rs01/" /etc/mongod.conf


#Start and enable MongoDB service
sudo systemctl daemon-reload
sudo systemctl enable mongod && sudo systemctl restart mongod

#mongo --eval "printjson(rs.initiate())"

sudo ufw allow from 10.1.1.3 to any port 27017
sudo ufw allow ssh
sudo ufw --force enable



