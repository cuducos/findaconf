# Find a Conference (WIP)

## About

_Find a Conference_ is under development. This is supposed to be a free, open source and ad free platform where:

* Registered *users can post info about academic conferences* and call for papers
* Anyone can *register with external accounts* (Google, Facebook, Twitter, Yahoo, what else?) so [we don't have to deal with passwords](http://youtu.be/8ZtInClXe1Q)
* There is *no curatorial layer*, but we should add *report links for users to flag innapropriate and/or duplicated content*
* Only the user *who posted a conference can edit it* 
* The platform should not host too much stuff regarding the conferences: it is *simply a platform for users to find conferences* and then follow to universities webpages, association websites, Eventbrite registrations, planning group emails etc.
* It should be designed to be easily internationalized (*multi-language*)

## Installation

If you wanr to get a development version of *Find a Conference* running, this session might be helpful. If it is not, let us know.

### Requirements

* Python 2.7+ (but not Python 3)
* PostgreSQL 9.3+
* [virtualenv](https://virtualenv.pypa.io/) and [virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/) are not required, but are recommended.
* [pip](https://github.com/pypa/pip) is not required, but I’m using it in install instructions
* [Node.js](http://nodejs.org/) with [CoffeeScript](http://coffeescript.org/) and [Bower](http://bower.io/)

### Environment variables

This application use a series of *environment variables*. This can easily be achieved by puting a file called `.env` in the root directory of the project. This file should define this variables (most of them are optional):

* `DEBUG`: sets if the application is started in debug mode (e.g. `True`)
* `ASSETS_DEBUG`: sets if [webassets](http://webassets.readthedocs.org/en/latest/environment.html?highlight=debug#webassets.env.Environment.debug) runs in debug mode (e.g. `True`)
* `SECRET_KEY`: [Flask's default secret key](http://flask.pocoo.org/docs/0.10/api/#flask.Flask.secret_key)
* `DATABASE_URL: url and credentials to development database (e.g. `'postgres://vagrant:vagrant@localhost/findaconf'`)  
* `DATABASE_URL_TEST: url and credentials to test database (e.g. `'postgres://vagrant:vagrant@localhost/findaconf_test'`)  
* `GOOGLE_PLACES_API`: credentials to [Google Places API](https://developers.google.com/places/documentation/)
* `GOOGLE_PLACES_API_PROXY`: if you want to access Google Places API through a proxy, set the proxy URL here (it might be useful as Heroku free applications has no fixed IP and a fixed IP – even if local ones such as `0.0.0.0` or `127.0.0.1` or `localhost` – are required by Google)

### Step-by-step installation

1. Clone the repository and step in its directory: `$ git clone git@github.com:cuducos/findaconf.git && cd findaconf`
1. If you want, get your [virtualenv](https://pypi.python.org/pypi/virtualenv) running
1. Install the dependencies: `$ pip install -r requirements.txt && bower install` 
1. Create and feed the database: `$ python manage.py db upgrade`
1. Run the server with something like: `$ python manage.py runserver -r -d -h 0.0.0.0`

### Further installation notes

If you need further instructions to configure your develeopment environment, take a look at our [Vagrant bootstrap script](/Vagrant.sh). It has all the commands to instal Python, Node.js, CoffeeScript, Bower and PostgreSQL, dependencies and to create databases and users. It is designed to work with [Ubuntu 14.04](http://releases.ubuntu.com/trusty/), but works with most [Debian](http://debian.org) distributions.

Note that the included [.bowerrc](/.bowerrc) sets up a customized directory to store Bower files.

By this point, if you are a [Vagrant](https://www.vagrantup.com/) user, you guessed it right: you can hit the road after cloning the repository: `$ vagrant up && vagrant ssh`.

## Tests

We're using [Nose](https://nose.readthedocs.org) for testing. You might prefer to use `$ nosetest --rednose` for legibility. 

Nose has serious difficulties in finding tests in executable files, thus if you wanna change the permissions of the tests files just run: `$ chmod -x $(find findaconf/tests/ -name '*.py')`.

## Contributing

You can discuss the project, further features, implementation and report issues [here on GitHub](https://github.com/cuducos/findaconf/issues). And pull requests are very welcomed indeed:

* Fork this repository
* Create a new branch: `git checkout -b my-new-feature`
* Commit your changes: `git commit -am 'Add some feature'`
* Push to the branch: `git push origin my-new-feature`
* Go to your fork page at GitHub and create new pull request

## License

Copyright (c) 2014 Eduardo Cuducos

Licensed under the [MIT LICENSE](LICENSE).
