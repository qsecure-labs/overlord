#!/bin/bash

CSTRIKE_KEY='xxxx-xxxx-xxxx-xxxx'

sudo apt install openjdk-11-jdk -y
sudo update-java-alternatives -s java-1.11.0-openjdk-amd64 -y

token=`curl -s https://www.cobaltstrike.com/download -d "dlkey=${CSTRIKE_KEY}" | grep 'href="/downloads/' | cut -d '/' -f3`
curl -s https://www.cobaltstrike.com/downloads/${token}/cobaltstrike-dist.tgz -o /tmp/cobaltstrike.tgz

echo ${CSTRIKE_KEY} > ~/.cobaltstrike.license
sudo cp ~/.cobaltstrike.license /root/.cobaltstrike.license

mkdir ~/cobaltstrike
tar zxf /tmp/cobaltstrike.tgz -C ~/
rm /tmp/cobaltstrike.tgz

git clone https://github.com/rsmudge/Malleable-C2-Profiles.git ~/cobaltstrike/c2-profiles
git clone https://github.com/killswitch-GUI/CobaltStrike-ToolKit ~/cobaltstrike/cs-toolkit

cd ~/cobaltstrike
./update
