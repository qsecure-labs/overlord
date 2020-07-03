sudo wget https://packages.microsoft.com/config/debian/10/packages-microsoft-prod.deb -O packages-microsoft-prod.deb
#replace https://packages.microsoft.com/config/debian/10/packages-microsoft-prod.deb with the correct distreo package (debian package tested on DO ubuntu and it works)
sudo apt install -y apt-transport-https
sudo dpkg -i packages-microsoft-prod.deb
sudo apt-get update
sudo apt-get install -y dotnet-sdk-3.1
git clone --recurse-submodules https://github.com/cobbr/Covenant
cd Covenant/Covenant
dotnet build