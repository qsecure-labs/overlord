#!/bin/bash

sudo curl https://raw.githubusercontent.com/rapid7/metasploit-omnibus/master/config/templates/metasploit-framework-wrappers/msfupdate.erb > /tmp/msfinstall
sudo chmod 755 /tmp/msfinstall
sudo /tmp/msfinstall
