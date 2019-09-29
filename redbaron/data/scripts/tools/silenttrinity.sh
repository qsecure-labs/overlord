sudo apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev \
libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
xz-utils tk-dev libffi-dev liblzma-dev python-openssl git
curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash
cat <<'EOF' >> ~/.bashrc
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
EOF
source ~/.bashrc
pyenv install 3.7-dev
git clone https://github.com/byt3bl33d3r/SILENTTRINITY
cd SILENTTRINITY
pyenv local 3.7-dev
pip3 install pipenv && pipenv install && pipenv shell
pip3 install -r requirements.txt