# Find a Conference

## About

_Find a Conference_ is under development.

## Installation

If you wanr to get a development version of *Find a Conference* running, this session might be helpful. If it is not, let us know.

### Requirements

* Python 2.7+ (but not Python 3)
* PostgreSQL 9.3+
* [virtualenv](https://virtualenv.pypa.io/) and [virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/) are not required, but are recommended.
* [pip](https://github.com/pypa/pip) is not required, but I’m using it in install instructions
* [Node.js](http://nodejs.org/) with [CoffeeScript](http://coffeescript.org/) and [Bower](http://bower.io/)

### Step-by-step installation

1. Clone the repository and step in its directory: `$ git clone git@github.com:cuducos/findaconf.git && cd findaconf`
1. If you want, get your [virtualenv](https://pypi.python.org/pypi/virtualenv) running
1. Install the dependencies: `$ pip install -r requirements.txt && bower install` 
1. Create and feed the database: `$ python manage.py db upgrade`
1. Run the server with something like: `$ python manage.py runserver -r -d -h 0.0.0.0`

### Further notes

If you need further instructions to configure your develeopment environment, take a look at our [Vagrant bootstrap script](/Vagrant.sh). It has all the commands to instal Python, Node.js, CoffeeScript, Bower and PostgreSQL, dependencies and to create databases and users. It is designed to work with [Ubuntu 14.04](http://releases.ubuntu.com/trusty/), but works with most [Debian](http://debian.org) distributions.

Note that the included [.bowerrc](/.bowerrc) sets up a customized directory to store Bower files.

By this point, if you are a [Vagrant](https://www.vagrantup.com/) user, you guessed it right: you can hit the road after cloning the repository: `$ vagrant up && vagrant ssh`.

## Tests

We're using [Nose](https://nose.readthedocs.org) for testing. You might prefer to use `$ nosetest --rednose` for legibility. 

Nose has serious difficulties in finding tests in executable files, thus if you wanna change the permissions of the tests files just run: `$ chmod -x $(find findaconf/tests/ -name '*.py')`.

## License

Copyright (c) 2014 Eduardo Cuducos

Licensed under the [MIT LICENSE](LICENSE).
