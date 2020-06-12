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

#Update .profile file

echo "export GOROOT=/usr/local/go" >> /root/.profile
echo "export GOPATH=/opt/goapps" >> /root/.profile
echo "export PATH=$GOPATH/bin:$GOROOT/bin:$PATH" >> /root/.profile

#Installation of go-dep

wget http://tw.archive.ubuntu.com/ubuntu/pool/universe/g/go-dep/go-dep_0.5.4-2_amd64.deb
dpkg -i go-dep_0.5.4-2_amd64.deb

#Installation of goDoH/

git clone https://github.com/sensepost/goDoH.git /opt/goapps/src/github.com/goDoH
cd /opt/goapps/src/github.com/goDoH && dep init
cd /opt/goapps/src/github.com/goDoH && dep ensure
cd /opt/goapps/src/github.com/goDoH && make key
cd /opt/goapps/src/github.com/goDoH && mkdir upx_temp
cd /opt/goapps/src/github.com/goDoH/upx_temp && wget https://github.com/upx/upx/releases/download/v3.95/upx-3.95-amd64_linux.tar.xz
cd /opt/goapps/src/github.com/goDoH/upx_temp && tar xf upx-3.95-amd64_linux.tar.xz
mv /opt/goapps/src/github.com/goDoH/upx_temp/upx-3.95-amd64_linux/upx /usr/local/bin
cd /opt/goapps/src/github.com/goDoH/ && make
