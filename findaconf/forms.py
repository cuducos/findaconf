from findaconf.helpers.providers import OAuthProvider
from flask.ext.wtf import Form
from wtforms import BooleanField, HiddenField
from wtforms.validators import AnyOf

providers = OAuthProvider()
credentials = dict(providers.credentials)


class LoginForm(Form):
    remember_me = BooleanField('Remember me (for a month)')
    provider = HiddenField(default='google-plus',
                           validators=[AnyOf(credentials.keys())])
