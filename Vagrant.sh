#!/usr/bin/env bash

# Python
apt-get update
apt-get install -y python-setuptools ipython python-dev build-essential libffi-dev libcairo2-dev python-pip
easy_install pip

# Node.js, CoffeeScript and Bower
apt-get install -y curl
curl -sL https://deb.nodesource.com/setup | sudo bash -
apt-get install -y nodejs
npm install -g coffee-script
npm install -g bower

# install project dependencies
cd /vagrant
pip install -r requirements.txt
bower install