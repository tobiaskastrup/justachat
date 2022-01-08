#!/bin/bash

################################################
#     nginx, Flask, gunicorn server setup      #
################################################
#
# Installere Gunicorn (Green Unicorn)
# som er en Python WSGI HTTP Server for UNIX
# (Kører flask projektet som en wsgi application
# Den installere også en nginx reversed proxy 
# server for gunicorn, den er frontend server, 
# og står også for at levere static pages (HTML,
# css, billeder osv)
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

# Token til at tilgå private respo i github
# SKAL EVT OPDATES FØR BRUG !!!!!!!!!!

rocketip="10.1.1.6"

########### apt install + www mappe #############
# Installere python pip3 og nginx til at eksekvere
# Python og pipenv til at lave en environment til

sudo apt update && sudo apt install -y python3-pip nginx certbot python3-certbot-nginx
sudo pip3 install pipenv

# Tilføjer HOME/.local/bin til PATH, så pip kan bruges
# "Source ~/.bashrc" opdater PATH
sudo echo "export PATH="$HOME/.local/bin:$PATH"" >> ~/.bashrc
source ~/.bashrc

# Laver en mappe til vores projekt,
# sætter tillader for mappen til $USER:www-data
sudo mkdir -p /var/www/justa.chat
sudo chown -R $USER:www-data /var/www/justa.chat
cd /var/www/justa.chat

# Henter vores webapplication fra github og gemmer i /var/www/justa.chat
git clone https://github.com/tobiaskastrup/justachat /var/www/justa.chat

########### pipenv indstillinger ###############
#
# Laver en .venv mappe som sikre at vores 
# environment ligger i vores application mappe 
# og ikke default. Laver en .env hvor vores 
# application indstilling tilføres nedenunder 
#
################################################
sudo mkdir -p /var/www/justa.chat/.venv
sudo touch /var/www/justa.chat/.env

# Tilføjer vores app startup variabler til .env
cat << EOF |sudo tee -a /var/www/justa.chat/.env
FLASK_APP=wsgi.py
FLASK_ENV=production
EOF

################### pipenv #####################
# 
# Vores environment oprettes og modulerne som
# er nødvendige for python koden inkl 
# rocketchat API'en tilføjes i denne
#
################################################
sudo pipenv install flask gunicorn requests rocketchat_API

############## wsgi application ################
#
# Vores wsgi application oprettes og er den som
# gunicorn kan bruge til at oprette instanser af
# justa.chat hjemmesiden
#
################################################
sudo touch /var/www/justa.chat/wsgi.py

cat << EOF |sudo tee -a /var/www/justa.chat/wsgi.py
from webapp.app import app

if __name__ == '__main__':
	app.run(debug=False)
EOF

############## justachat.service ###############
#
# Opretter en mappe til gunicorn logs
# Opretter en servicefil til at starte vores 
# gunicorn server op og enabler og starter den
# efterfølgende
#
################################################

sudo mkdir -p /var/log/gunicorn
sudo chown -R $USER:www-data /var/log/gunicorn

# Indsætter service konfiguration i justachat.service
cat << EOF |sudo tee -a /etc/systemd/system/justachat.service
[Unit]
Description=justachat.service - A Flask application run with Gunicorn.
After=network.target
 
[Service]
User=$USER
Group=www-data
WorkingDirectory=/var/www/justa.chat/
ExecStart=/var/www/justa.chat/.venv/bin/gunicorn --workers 1 --threads 10 --worker-connections 1000 --error-logfile /var/log/gunicorn/error.log --log-level=debug --bind unix:/var/www/justa.chat/justachat.sock wsgi:app

[Install]
WantedBy=multi-user.target
EOF

# Enabler (sørge for service start ved reboot) og starter vores justachat.service 
sudo systemctl enable justachat.service && sudo systemctl start justachat.service 

########### nginx + justachat.conf #############
#
# Opretter en configurationsfil til nginx for
# vores application, og sætte den til at proxy vores
# gunicorn sock, fjerner default conf 
# fra sites-enabled og tilføjer vores nye fil 
# i stedet. Slutter af med at enable og starte
# nginx. 
#
################################################
cat << EOF |sudo tee -a /etc/nginx/conf.d/justachat.conf
server {
	listen 80;
	server_name justa.chat;

	access_log /var/log/nginx/justachat.access.log;
		error_log /var/log/nginx/justachat.error.log;
 
		location / {
				include proxy_params;
				proxy_pass http://unix:/var/www/justa.chat/justachat.sock;
		}
}
EOF

# Tilføjer indhold til /etc/nginx/conf.d/admin.justachat.conf filen, 
# som laver en proxy til vores rocketchat side 
# rocketip:3000 > admin.justa.chat
cat << EOF |sudo tee -a /etc/nginx/conf.d/admin.justachat.conf
upstream rocket_backend {
  server $rocketip:3000;
}

server {
    listen 80;
    server_name admin.justa.chat;
    access_log /var/log/nginx/rocketchat-access.log;
    error_log /var/log/nginx/rocketchat-error.log;

    location / {
        proxy_pass http://rocket_backend/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host \$http_host;

        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forward-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forward-Proto http;
        proxy_set_header X-Nginx-Proxy true;

        proxy_redirect off;
    }
}
EOF
# Sletter default nginx config og enabler og starter nginx service
sudo rm /etc/nginx/sites-enabled/default
sudo systemctl enable nginx && sudo systemctl start nginx
# Henter et SSL ertifikat fra Let's Encrypt
certbot run -n --nginx --agree-tos -d justa.chat -m admin@enode.dk --no-eff-email --redirect
certbot run -n --nginx --agree-tos -d admin.justa.chat -m admin@enode.dk --no-eff-email --redirect
# Genstarter nginx efter SSL certifikat er implmenteret
sudo systemctl restart nginx

############### UFW (Firewall) ################
#
# Vi opsætter en UFW (Uncomplicated Firewall)
# som kun tillader http, https og ssh portene er
# åbne i vores VM fra Bastion subnettet
#
################################################
sudo ufw allow http
sudo ufw allow https
sudo ufw allow from 10.1.3.0/24 to any port 22 #SSH from bastion
sudo ufw --force enable