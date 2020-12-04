#!/bin/bash
git clone https://github.com/BC-SECURITY/Empire.git
cd Empire
sudo pip3 install poetry
sudo ./setup/install.sh <<< "RandomSTRING"
sudo poetry install