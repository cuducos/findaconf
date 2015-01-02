# coding: utf-8

from findaconf import app


class OAuthProvider(object):

    def __init__(self, oauth_credentials=None):

        # load credentials
        if oauth_credentials:
            self.original_credentials = oauth_credentials
        else:
            self.original_credentials = app.config['OAUTH_CREDENTIALS']

        # check if consumer key an secret are set
        self.credentials = dict()
        for provider in self.original_credentials.keys():
            if self.__valid_provider(provider):
                self.credentials[provider] = self.original_credentials[provider]

        # set support vars
        self.names = sorted([p for p in self.credentials])
        self.slugs = [p.lower().replace(' ', '-') for p in self.names]
        self.providers = dict(zip(self.slugs, self.names))

    def get_name(self, provider_slug):
        name = self.providers.get(provider_slug, None)
        if name:
            return str(name)
        return None

    def get_slugs(self):
        return [str(slug) for slug in self.slugs]

    def __valid_provider(self, provider_name):
        credentials = self.original_credentials.get(provider_name, None)
        if credentials:
            key = credentials.get('consumer_key', None)
            secret = credentials.get('consumer_secret', None)
            if key and secret:
                return True
        return False
