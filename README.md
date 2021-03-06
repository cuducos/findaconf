# Find a Conference (WIP)

## About

_Find a Conference_ is under development. This is supposed to be a free, open source and ad-free platform where:

* Registered *users can post info about academic conferences* and call for papers
* There is *no curatorial layer*…
* …but users can *report inappropriate/duplicated contents*
* Only the user *who posted a conference can edit it* 
* The platform should not host too much stuff regarding the conferences, instead *it should point to* universities/association websites, Eventbrite, planning group emails etc.
* It should be designed to be easily internationalized (*multi-language*)

## Installation

If you want to get a development version of *Find a Conference* running, this session might be helpful. If it is not, let us know.

### Requirements

* Python 2.7+ (many of the dependencies are not Python 3 compatible yet)
* PostgreSQL 9.3+
* [Node.js](http://nodejs.org/) with [CoffeeScript](http://coffeescript.org/) and [Bower](http://bower.io/)

[pip](https://github.com/pypa/pip) is not required, but we are using it in install instructions.

[virtualenv](https://virtualenv.pypa.io/) and [virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/) are not required but are *highly recommended*.

### Environment variables

This application requires *environment variables* in order to work properly.

Usually they are read from a `.env` (not included in the repository for security reasons). But you can copy `.env.sample` as `.env` and customize it – it is the easiest way to set these variables.

#### Databases (required)

* `DATABASE_URL`: URL and credentials to development database (e.g. `postgres://vagrant:vagrant@localhost/findaconf`)  
* `DATABASE_URL_TEST`: URL and credentials to test database (e.g. `postgres://vagrant:vagrant@localhost/findaconf_test`)  

#### Security (required)

* `SECRET_KEY`: [Flask's default secret key variable](http://flask.pocoo.org/docs/0.10/api/#flask.Flask.secret_key), i.e. just a random and long string

#### Public APIs (recommended)

* `GOOGLE_PUBLIC_API`: credentials to [Google Places API](https://developers.google.com/places/documentation/)
* `GOOGLE_PLACES_PROXY` *(optional)*: if you want to [access Google Places API through a proxy](contrib/google_places_proxy), set the proxy URL here

#### OAuth/OAuth2 APIs (recommended)

At least one of these providers should be set in order to enable users to log in.

Setting a provider involves registering an application with a OAuth/OAuth2 provider, and passing the `client id` and `client secret` tokens to *Find a Conference* through pairs from this set of variables:

* `AMAZON_CLIENT_ID` and `AMAZON_CLIENT_SECRET`
* `FACEBOOK_CLIENT_ID` and `FACEBOOK_CLIENT_SECRET`
* `GITHUB_CLIENT_ID` and `GITHUB_CLIENT_SECRET`
* `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET`
* `LINKEDIN_CLIENT_ID` and `LINKEDIN_CLIENT_SECRET`
* `TUMBLR_CLIENT_ID` and `TUMBLR_CLIENT_SECRET`
* `WINDOWS_CLIENT_ID` and `WINDOWS_CLIENT_SECRET`
* `YAHOO_CLIENT_ID` and `YAHOO_CLIENT_SECRET`

#### Debug (optional)

* `DEBUG`: sets if the application is started in debug mode (e.g. `True`)
* `ASSETS_DEBUG`: sets if [webassets](http://webassets.readthedocs.org/en/latest/environment.html?highlight=debug#webassets.env.Environment.debug) runs in debug mode (e.g. `True`)

#### Administrator

* `ADMIN`: when an user with an email listed in this variable (a string containing email addresses, comma separated) is created, it is created as `admin` (not as regular `user`)

### Step-by-step installation with Vagrant

1. Clone the repository and step in its directory: `$ git clone git@github.com:cuducos/findaconf.git && cd findaconf`
1. Start create, provision and log into your virtual machine: `$ vagrant up && vagrant ssh`
1. Go to the application directory: `$ cd /vagrant`
1. Set up your [API credentials](#oauthoauth2-apis-recommended) editing the `.env` file accordingly
1. Run the server with something like: `$ python manage.py runserver -r -d -h 0.0.0.0`

### Step-by-step installation without Vagrant

1. Clone the repository and step in its directory: `$ git clone git@github.com:cuducos/findaconf.git && cd findaconf`
1. Install the dependencies: `$ pip install -r requirements.txt && bower install` 
1. Set up your [environment variables](#environment-variables): `$ mv .env.sample .env` and then edit `.env` accordingly
1. Create and feed the database: `$ python manage.py db upgrade`
1. Run the server with something like: `$ python manage.py runserver -r -d -h 0.0.0.0`

### Further installation notes

If you need further instructions to configure your development environment, take a look at our [Vagrant bootstrap script](/Vagrant.sh). It has all the commands to install Python, Node.js, CoffeeScript, Bower and PostgreSQL dependencies, and the commands to create databases and users. It is designed to work with [Ubuntu 14.04](http://releases.ubuntu.com/trusty/), but it should work with most [Debian](http://debian.org) distributions.

Note that the included [.bowerrc](/.bowerrc) sets up a customized directory to store Bower files.

We suggest running the server with these optional arguments: `-d` enables the debug mode, `-r` reloads the server in case you change any file, and `-h 0.0.0.0` starts the server at this (local) IP.

## Tests

We're using [Nose](https://nose.readthedocs.org) for testing: `$ nosetests` from the project directory is the standard. 

If Nose isn't finding any test, it worth it to remember that [Nose's default behavior is to ignore executable files](http://nose.readthedocs.org/en/latest/usage.html#extended-usage). You can overcome this situation by any of this ways:

* Changing the permissions of tests files: `$ chmod -x $(find findaconf/tests/ -name '*.py')`
* Running Nose with the `--exe` flag

## Contributing

You can discuss the project, further features, implementation and report issues [here on GitHub](https://github.com/cuducos/findaconf/issues). And pull requests are very welcomed indeed:

* Fork this repository
* Create a new branch: `git checkout -b my-new-feature`
* Commit your changes: `git commit -am 'Add some feature'`
* Push to the branch: `git push origin my-new-feature`
* Go to your fork page at GitHub and create new pull request

### To do list

We keep track of ideas, enhancements etc. in our [TODO list](TODO.md), check it out and join us making the list longer or shorter.

## Contributors

The idea emerged within a group of PhD students in Sociology from the [University of Essex](http://essex.ac.uk): [Ale](http://www.essex.ac.uk/sociology/staff/profile.aspx?ID=3787), [Can](http://www.essex.ac.uk/sociology/staff/profile.aspx?ID=3471) and [Cuducos](http://cuducos.me).

[Mabel](http://about.me/mabel_lazzarin) and [Cuducos](http://cuducos.me) designed the UI. 

The source code is being written by:

* [Cuducos](http://cuducos.me)
* [Gabriel](http://about.me/gabrielvicente)
* [Lorenzo](http://github.com/lorenzo-pasa)
* [John](http://github.com/jbaham2)

## License

Copyright (c) 2015 Eduardo Cuducos, Gabriel Vicente and Lorenzo Pascucci

Licensed under the [MIT LICENSE](LICENSE).
