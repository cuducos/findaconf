# Find a Conference – Development TODO

This is a list of ideas we had to improve our platform and to learn. Feel free to jump in and contribute to get the list longer  (adding ideas)or shorter (coding some of these ideas).

## New Features

| Title | Description | References | Depends on | Branch | 
|-------|-------------|------------|------------|--------|
| **Add conferences** | Create the page to add conferences | [Flask-API](http://www.flaskapi.org/) | | |
| **Redirect after login** | When accessing restricted pages, login should be asked and user should be redirected there after the login | [Flask-Login `next` variable](https://flask-login.readthedocs.org/en/latest/#how-it-works) and [`next_page` within our `login()`](https://github.com/cuducos/findaconf/blob/master/findaconf/blueprints/site/views.py#L82) | _Add conference_ |
| **Full text search** | Add full text search to Conference mapped class | [Whoosh](https://pypi.python.org/pypi/Whoosh) and [Miguel's tutorial](http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-x-full-text-search) | _Add conference_ | |
| **Update support tables** | Run scripts to update support tables (`Keywords`, `MagicNumbers`) asynchronous | [Celery](https://pypi.python.org/pypi/celery/3.1.17) (preferable) or via [Flask-Script](http://flask-script.readthedocs.org/) and [Heroku's Scheduler](https://devcenter.heroku.com/articles/scheduler) | _Add conference_ | |
| **Threading emails** | Create the feature to queue and send emails | | | |

## Refactors

| Title | Description | References | Depends on | Branch | 
|-------|-------------|------------|------------|--------|
| **Fixtures** | We are seeding our database through migration scripts – we might need a better way to input “static” data (countries and continents names), avoiding 2-step `bulk_insert` for example | | | |
| **login()** | This method ended up too long (more than 100 lines) – we might need to study and refactor it | [Our `login()`](https://github.com/cuducos/findaconf/blob/master/findaconf/blueprints/site/views.py#L78)| | |
| **Users API** | Implement a RESTful architecture for our `User` model | [Flask-API](http://www.flaskapi.org/) | | |

## Contents

| Title | Description | References | Depends on | Branch | 
|-------|-------------|------------|------------|--------|
| **Financial support page** | `/support` page explaining the business model, the costs and the  donations through Unlock, PayPal and Bitcoin | | | |
| **Terms of use** | We might need it someday | | | |
| **Proofread** | Proofread everything, as most of us are not native English speakers | | | |