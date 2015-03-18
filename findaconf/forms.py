from findaconf.helpers.providers import OAuthProvider
from flask.ext.wtf import Form
from wtforms import BooleanField, HiddenField
from wtforms.validators import AnyOf

providers = OAuthProvider()


class LoginForm(Form):
    remember_me = BooleanField('Remember me')
    provider = HiddenField(default='google-plus',
                           validators=[AnyOf(providers.get_slugs())])
