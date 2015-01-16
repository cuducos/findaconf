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

This application uses some required *environment variables*. You can start costumizing them using by renaming and editing the sample file included in this repository. 

#### Databases (required)

* `DATABASE_URL`: url and credentials to development database (e.g. `postgres://vagrant:vagrant@localhost/findaconf`)  
* `DATABASE_URL_TEST`: url and credentials to test database (e.g. `postgres://vagrant:vagrant@localhost/findaconf_test`)  

#### Security (required)

* `SECRET_KEY`: [Flask's default secret key](http://flask.pocoo.org/docs/0.10/api/#flask.Flask.secret_key)

#### Public APIs (recommended)

* `GOOGLE_PUBLIC_API`: credentials to [Google Places API](https://developers.google.com/places/documentation/)
* `GOOGLE_PLACES_PROXY` *(optional)*: if you want to [access Google Places API through a proxy](contrib/google_places_proxy), set the proxy URL here

#### OAuth/OAuth2 APIs (recommended)

At least one of these providers should be set in order to enable users to log in. Setting a provider involves registering an app with a OAuth/OAuth2 provider, and passing the `client id` and `client secret` tokens to *Find a Conference* throght pairs from this set of variables:

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

### Step-by-step installation

1. Clone the repository and step in its directory: `$ git clone git@github.com:cuducos/findaconf.git && cd findaconf`
1. If you want, get your [virtualenv](https://pypi.python.org/pypi/virtualenv) running
1. Install the dependencies: `$ pip install -r requirements.txt && bower install` 
1. Set up your [environment variables](#environment-variables): `$ mv .env.sample .env` and then edit `.env` accordingly
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

### To do list

These are the next steps (there is a lot to be done, these are just some more short term tasks):

* Enhance users login (add fields/features such as `last_seen`, `remember_me`, `created_at`, `created_with`, `last_accessed_with` – these last two fields refer to the OAuth/OAuth2 provider)
* Implement more test for user login (error message, success message, redirect message)
* Redirect users after login
* Roles for user permissions have not been created (we have the table `Group` created, but we are not using it)
* Threading for email notifications
* Create the page to add conferences
* Commands (via Flask-Script) to update support table (`Keywords`, `MagicNumbers`)
* Proof read (as most of us are not native English speakers)
* What else?

## Contributors

The idea emerged within a group of PhD students in Sociology from the [University of Essex](http://essex.ac.uk): [Ale](http://www.essex.ac.uk/sociology/staff/profile.aspx?ID=3787), [Can](http://www.essex.ac.uk/sociology/staff/profile.aspx?ID=3471) and [Cuducos](http://cuducos.me).

[Mabel](http://about.me/mabel_lazzarin) and [Cuducos](http://cuducos.me) designed the UI. 

The source code is being written by [Cuducos](http://cuducos.me), [Gabriel](http://about.me/gabrielvicente) and [John](http://github.com/jbaham2).

## License

Copyright (c) 2015 Eduardo Cuducos and Gabriel Vicente

Licensed under the [MIT LICENSE](LICENSE).
