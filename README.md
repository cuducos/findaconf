# Find a Conference

## About

_Find a Conference_ is under development.

## Installation

First of all, make sure your system has the following tools installed properly:

* Python 2.7+
* PostgreSQL 9.3+
* [virtualenv](https://virtualenv.pypa.io/) and [virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/) are not required, but are recommended.
* [pip](https://github.com/pypa/pip) is not required, but I’m using it in install instructions – if you want to install it, download [get-pip.py](https://bootstrap.pypa.io/get-pip.py) and run this command on your download folder `$ python get-pip.py`.


Then, simply clone the repository:

```
$ git clone git@github.com:cuducos/findaconf.git
```

Install all the dependencies (if you want, get your [virtualenv](https://pypi.python.org/pypi/virtualenv) running):

```
$ cd findaconf
$ pip install -r requirements.txt
```

Also install [Node.js](http://nodejs.org/), [CoffeeScript](http://coffeescript.org/) and [Bower](http://bower.io/):


```
$ curl -sL https://deb.nodesource.com/setup | sudo bash - 
$ apt-get install nodejs
$ npm install -g coffee-script
$ npm install -g bower
```

Remember to meet the dependencies in [bower.json](/bower.json) (if you want, specify a different installation path using [.bowerrc](/.bowerrc)):

```
$ bower install 
```

Create and feed the database:

 ```
 $ python manage.py db upgrade
 ```

Then, run the server:

```
$ python manage.py runserver -r -d
```
### Using Vagrant

Before installing, make sure you have recent versions of
[Git](http://www.git-scm.com/), [Vagrant](https://www.vagrantup.com/)
and [VirtualBox](https://www.virtualbox.org/) installed on your
development machine.

Then, simply clone the repository:

```
$ git clone git@github.com:cuducos/findaconf.git.
```

And create a Vagrant machine from the root of the project:

```
$ cd findaconf
$ vagrant up && vagrant ssh
```

## Tests

We're using [Nose](https://nose.readthedocs.org) for testing. You might prefer to use `$ nosetest --rednose` for legibility. 

Nose has serious difficulties in finding tests in executable files, thus if you wanna change the permissions of the tests files just run: `$ chmod -x $(find findaconf/tests/ -name '*.py')`.

## License

Copyright (c) 2014 Eduardo Cuducos

Licensed under the [MIT LICENSE](LICENSE).
