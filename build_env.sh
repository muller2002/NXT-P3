#!/bin/bash
set -e
sudo apt-get install libbluetooth-dev python3-virtualenv >> LEGO.log
virtualenv -p python3 venv3 >> LEGO.log
. ./venv3/bin/activate >> LEGO.log
wget https://github.com/Eelviny/nxt-python/archive/master.zip >> LEGO.log
unzip master.zip >> LEGO.log
cd nxt-python-master
python3 setup.py install >> ../LEGO.log
cd ..
pip install -r requirements.txt >> LEGO.log
python3 setup.py install >> LEGO.log
cd pf_nxt/website
chmod +x bash.sh >> ../../LEGO.log
cd ..
cd ..
