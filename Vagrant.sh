#!/usr/bin/env bash

# Update repository and add dev packages
apt-get update
apt-get upgrade -y
apt-get autoremove -y
apt-get install -y wget curl git ipython build-essential
apt-get install -y libffi-dev libcairo2-dev

# Python
apt-get install -y python-setuptools python-dev
easy_install pip

# Node.js, CoffeeScript and Bower
curl -sL https://deb.nodesource.com/setup | sudo bash -
apt-get install -y nodejs
npm install -g coffee-script
npm install -g bower

# PostgreSQL
apt-get install -y postgresql postgresql-contrib libpq-dev
apt-get install -y python-psycopg2
sudo -u postgres psql -c "CREATE ROLE vagrant WITH PASSWORD 'vagrant' LOGIN SUPERUSER"
sudo -u postgres createdb -O vagrant findaconf
sudo -u postgres createdb -O vagrant findaconf_test

# install project dependencies
pip install -r /vagrant/requirements.txt

