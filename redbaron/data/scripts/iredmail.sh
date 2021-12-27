#bin/bash

wget https://github.com/iredmail/iRedMail/archive/refs/tags/1.5.0.tar.gz
tar -xf 1.4.0.tar.gz

cd iRedMail-1.4.0

echo -e "AUTO_USE_EXISTING_CONFIG_FILE=y \
\nAUTO_INSTALL_WITHOUT_CONFIRM=y \
\nAUTO_CLEANUP_REMOVE_SENDMAIL=y \
\nAUTO_CLEANUP_REMOVE_MOD_PYTHON=y \
\nAUTO_CLEANUP_REPLACE_FIREWALL_RULES=y \
\nAUTO_CLEANUP_RESTART_IPTABLES=y \
\nAUTO_CLEANUP_REPLACE_MYSQL_CONFIG=y \
\nAUTO_CLEANUP_RESTART_POSTFIX=n \
\nbash iRedMail.sh" > new_iR.sh

chmod 777 new_iR.sh

echo -e "export STORAGE_BASE_DIR='/var/vmail'
export WEB_SERVER='NGINX'
export BACKEND_ORIG='MYSQL'
export BACKEND='MYSQL'
export VMAIL_DB_BIND_PASSWD='changeme!'
export VMAIL_DB_ADMIN_PASSWD='changeme!'
export MLMMJADMIN_API_AUTH_TOKEN='changeme!'
export NETDATA_DB_PASSWD='changeme!'
export MYSQL_ROOT_PASSWD='changeme!'
export FIRST_DOMAIN='domain-to-change.com'
export DOMAIN_ADMIN_PASSWD_PLAIN='changeme!'
export USE_IREDADMIN='YES'
export USE_ROUNDCUBE='YES'
export USE_NETDATA='YES'
export USE_FAIL2BAN='NO'
export AMAVISD_DB_PASSWD='changeme!'
export IREDADMIN_DB_PASSWD='changeme!'
export RCM_DB_PASSWD='changeme!'
export SOGO_DB_PASSWD='changeme!'
export SOGO_SIEVE_MASTER_PASSWD='changeme!'
export IREDAPD_DB_PASSWD='changeme!'
#EOF" > config

yes | ./new_iR.sh

