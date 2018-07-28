#!/bin/bash

pip install --upgrade pip

pip install flask
pip install pika
pip install sqlalchemy
pip install psutil
pip install pandas

python ./srv/setup.py install
python ./client_sms/setup.py install