#!/bin/bash

#install all the packages required
apt install python3
apt install python3-pip
apt install wget
apt install unzip

#install the python requirements from the txt
pip3 install -r requirements.txt

#download terraform binary
wget https://releases.hashicorp.com/terraform/0.11.14/terraform_0.11.14_linux_amd64.zip
unzip terraform_0.11.14_linux_amd64.zip
mv terraform /opt/terraform
rm terraform_0.11.14_linux_amd64.zip
echo 'export PATH="$PATH:/opt"' >> ~/.profile

#download godaddy plugin for terraform
wget https://github.com/n3integration/terraform-godaddy/releases/download/v1.6.4/terraform-godaddy_linux_amd64.tgz
tar -xvzf terraform-godaddy_linux_amd64.tgz
rm terraform-godaddy_linux_amd64.tgz
mv terraform-godaddy_linux_amd64 ../redbaron/data/plugins/terraform-provider-godaddy_v1.6.4_x4