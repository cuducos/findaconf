#!/usr/bin/env bash

###############################################################################
# Update Ubuntu and install developer tools                                   #
###############################################################################

apt-get update
apt-get upgrade -y
apt-get autoremove -y
apt-get install -y wget curl git build-essential
apt-get install -y libffi-dev libcairo2-dev

###############################################################################
# Install Pyhton, Node & PostgreSQL                                           #
###############################################################################

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

###############################################################################
# Install Python developer packages                                           #
###############################################################################

pip install ipython coverage flake8 rednose

###############################################################################
# Create the database and its user                                            #
###############################################################################

sudo -u postgres psql -c "CREATE ROLE vagrant WITH PASSWORD 'vagrant' LOGIN SUPERUSER"
sudo -u postgres createdb -O vagrant findaconf
sudo -u postgres createdb -O vagrant findaconf_test

###############################################################################
# Install Python and Bower dependencies                                       #
###############################################################################

cd /vagrant
pip install -r requirements.txt
su -c "bower install" -s /bin/sh vagrant

###############################################################################
# Create and edit new .env file                                               #
###############################################################################

# create new .env file as a copy of .env.sample
cp .env.sample .env

# set database
sed -i "s/user:password@host\/database/vagrant:vagrant@localhost\/findaconf/g" .env
sed -i "s/_for_tests/_test/g" .env

# set a secret key
sed -i "s/SECRET_KEY = ''/SECRET_KEY = 'insert a real secret here as soon as you read this!'/g" .env

# remove fake Google Places proxy
sed -i "s/http:\/\/example.com\/google_places//g" .env

# set debug to True
sed -i "s/DEBUG = False/DEBUG = True/g" .env

###############################################################################
# Go live                                                                     #
###############################################################################

# migrate & feed db
su -c "python manage.py db upgrade" -s /bin/sh vagrant
