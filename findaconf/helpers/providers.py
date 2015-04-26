# coding: utf-8

from findaconf import app


class OAuthProvider(object):

    """
    Loads oauth/oauth2 credentials from app.config['OAUTH_CREDENTIALS'] and
    sets the following attributes:

    * original: (dictionary) the same credentials as loaded

    * credentials: (list generator) tuples (slug, credentials) for a filtered
    version of the loaded credentials keeping only `valid` oauth/oauth2
    providers, i.e. the ones  with client key and secret properly set

    * ordered: (list generator) OAuthProvider object for each valid
    provider (sorted alphabetically)
    """

    def __init__(self):
        self.original = app.config['OAUTH_CREDENTIALS']

    @property
    def credentials(self):
        """
        Test each oauth/oauth2 provider to check if it has client and secret
        keys set, and deleteing the ones with no settings. Returns a list
        generator with tuples (provider name, provider settings).
        """
        for provider in self.original.iterkeys():
            credentials = self.original.get(provider)
            if credentials:
                key = credentials.get('consumer_key')
                secret = credentials.get('consumer_secret')
                if key and secret:
                    ui = ProviderUI(name=provider)
                    self.original[provider]['ui'] = ui
                    yield ui.slug, self.original[provider]

    @property
    def ordered(self):
        """ List generator with OAuthProvider objects ordered by slug """
        credentials = dict(self.credentials)
        slugs = sorted([slug for slug in credentials.iterkeys()])
        for slug in slugs:
            yield credentials[slug]['ui'] 

    def name(self, slug):
        """Returns a provider name given its slug"""
        for provider in self.ordered:
            if provider.slug == slug:
                return provider.name
        return None

        
class ProviderUI(object):

    """ Creates a  object with name & slug for oauth/oauth2 providers"""
    
    def __init__(self, name=None):
        self.name = name

    @property
    def slug(self):
        return self.name.lower().replace(' ', '-')
