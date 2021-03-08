#!/bin/sh
cd `dirname "$0"`
set -e

[ -n "$venv" ] || python3 -m venv venv
[ -n "$(which deactivate)" ] && deactivate
. ./venv/bin/activate

pip3 install wheel
pip3 install -r requirements.txt
pip3 install pyinstaller

pyinstaller --onefile smtp2tg.py
docker build -t smtp2tg .


