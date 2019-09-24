cmd="sudo apt-get install -y python"
until eval $cmd
do
    sleep 10
done
git clone https://github.com/trustedsec/ptf.git /opt/ptf
cd /opt/ptf/ && sudo ./ptf<< EOF
use modules/exploitation/install_update_all
yes
use modules/intelligence/install_update_all
yes
use modules/post_exploitaion/install_update_all
yes
use modules/powershell/install_update_all
yes
use modules/vulnerability-analysis/install_update_all
yes
EOF

#we can use the ptf framework to install specific tools:
#use modules/exploitation/metasploit
#run
