#!/bin/bash

sudo apt install unzip -y

#Install Gophish
cd /opt
wget https://github.com/gophish/gophish/releases/download/v0.11.0/gophish-v0.11.0-linux-64bit.zip
unzip gophish-v0.11.0-linux-64bit.zip -d gophish
rm gophish-v0.11.0-linux-64bit.zip
cd gophish
chmod +x /opt/gophish/gophish
sed -i 's/127.0.0.1/0.0.0.0/g' config.json # replace localhost to open

#gophish service
chmod +x /tmp/gophish.sh
systemctl start gophish.service

#create readme file
echo "systemctl start gophish.service (start the service)" >> /opt/gophish/OVERLORD_README.txt
echo "systemctl stop gophish.service (stop the service)" >>/opt/gophish/OVERLORD_README.txt

sleep 20s

# get initial password
cat /var/log/gophish.err | grep 'Please login with the username admin and the password' > /opt/gophish/password.txt
