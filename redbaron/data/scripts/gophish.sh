#!/bin/bash
#install Go
wget https://dl.google.com/go/go1.12.5.linux-amd64.tar.gz
tar -xvf go1.12.5.linux-amd64.tar.gz
mv go /usr/local
rm go1.12.5.linux-amd64.tar.gz
cd /opt && mkdir goapps && cd goapps
export GOROOT=/usr/local/go         #its better to change the .profile file of root
export GOPATH=/opt/goapps
export PATH=$GOPATH/bin:$GOROOT/bin:$PATH
go version
go env
#Install Gophish
go get github.com/gophish/gophish
cd /opt/goapps/src/github.com/gophish/gophish
go build
sed -i 's/127.0.0.1/0.0.0.0/g' config.json # replace localhost to open
#gophish service
chmod +x /root/gophish.sh
systemctl start gophish.service
#Update .profile file
echo "export GOROOT=/usr/local/go" >> /root/.profile
echo "export GOPATH=/opt/goapps" >> /root/.profile
echo "export PATH=$GOPATH/bin:$GOROOT/bin:$PATH" >> /root/.profile
source /root/.profile
#create readme file
echo "systemctl start gophish.service (start the service)" >> /root/README.txt
echo "systemctl stop gophish.service (stop the service)" >> /root/README.txt
#file: /lib/systemd/system/gophish.service 
#file: /root/gophish.sh
#systemctl start gophish.service (start the service)
#systemctl stop gophish.service (stop the service)

#/opt/goapps/src/github.com/gophish/gophish/config.json
#listen_url": "0.0.0.0:3333", must change to this!