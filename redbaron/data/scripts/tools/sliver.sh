#!/bin/bash

# Install sliver pre-requisites
sudo apt install unzip mingw-w64 binutils-mingw-w64 g++-mingw-w64 wget -y

# Install MSF nightly installer, sliver uses this for some functionality
curl https://raw.githubusercontent.com/rapid7/metasploit-omnibus/master/config/templates/metasploit-framework-wrappers/msfupdate.erb > msfinstall && \
  chmod 755 msfinstall && \
  ./msfinstall

# Install the latest sliver. This grepping is ugly, don't judge me.
LOCATION=$(wget -qO - https://github.com/BishopFox/sliver/releases/latest \
| grep -w "sliver-server_linux.zip" \
| cut -d  '"' -f 2 \
| grep "zip" \
| grep -v sig) \
; wget -cq https://github.com$LOCATION

mkdir ~/sliver
unzip sliver-server_linux.zip -d ~/sliver
rm sliver-server_linux.zip
chmod +x /sliver/sliver-server