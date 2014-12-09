#!/usr/bin/env bash

# Update repository and add dev packages
apt-get update
apt-get upgrade
apt-get autoremove -y
apt-get install -y wget curl git ipython build-essential libffi-dev libcairo2-dev

# Python
apt-get install -y python-setuptools python-dev
easy_install pip

# Node.js, CoffeeScript and Bower
curl -sL https://deb.nodesource.com/setup | sudo bash -
apt-get install -y nodejs
npm install -g coffee-script
npm install -g bower

# install project dependencies
cd /vagrant
pip install -r requirements.txt
