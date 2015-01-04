# Find a Conference's Google Places Proxy

If deploying to servers such as [Heroku](http://heroku.com) by default IP will 
not be a fixed one, causing Google Public API to fail as it requires a list of
incoming IP addressess.

This is the case, for example, of *Google Places API* (but not of *OAuth2*).

This directory contains the proxy server we use to solve this problem. We
store this script somewhere else (a server with fixed IP), and set our
application to access Google Places API using this script as a proxy.
Performance still an issue, but the use of proxy is meant to be temporary.

## Server requirements

* Python 2.7
* `pip` command line tool
* Access through SSH (or some other way to run `pip`)  
* WSGI enabled

## Installing

1. Upload the `google_places_proxy.fcgi` and `requirements.txt` file to your
fixed IP server.
1. Install the requirements: `pip install -r requirements.txt`.
1. If using Python through [virtualenv](https://virtualenv.pypa.io/), add its
path as a shebang at the first line of `google_places_proxy.fcgi`:
`#!/path/to/your/virtualenv/bin/python`

For [Apache](https://httpd.apache.org/) servers a `.htaccess` might be helpful to simplify the URL:

```
Options +ExecCGI
AddHandler fcgid-script .fcgi
RewriteEngine On
RewriteCond %{REQUEST_FILENAME} !=/path/to/google_places_proxy.fcgi
RewriteRule ^(.*)$ google_places_proxy.fcgi/$1 [QSA,L]
```

## Activating the proxy within *Find a Conference*

1. In your *Find a Conference* fork set the `GOOGLE_PLACES_PROXY` environment
variable to the URL of `google_places_proxy.fcgi`.
1. Make sure both servers (the proxy server and the one running your fork of
*Find a Conference*) have exactly the `SECRET_KEY` environment variable.

## License

Copyright (c) 2015 Eduardo Cuducos

Licensed under the [MIT LICENSE](LICENSE).
