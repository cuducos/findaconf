# coding: utf-8

from findaconf import app


class OAuthProvider(object):

    def __init__(self, oauth_credentials=None):
        """
        Loads oauth/oauth2 credentials from app.config['OAUTH_CREDENTIALS'] or
        from oauth_credentials.

        Sets the following instance attributes:

        * original_credetials: (dictionary) the same credentials as loaded

        * credetnials: (dictionary) filtered version of the loaded credentials
        keeping only `valid` oauth/oauth2 providers, i.e. the ones  with client
        key and secret properly set

        * names: (list) humanized names for valid oauth/oauth2 providers (e.g.
        Google Plus instead of google-plus)

        * slugs: (list) slugs for valid oauth/oauth2 providers (e.g. google-plus
        instead of Google Plus)

        * providers: (dictionary) valid oauth/oauth2 providers having the slug
        as key and the humanized name as value
        """

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

    def __valid_provider(self, provider_name):
        """
        Test if a oauth/oauth2 provider is valid by asserting it has the client
        key and secret set.
        :param provider_name: (string) humanized name (e.g. Google Plus instead
        of google-plus) of a oauth/oauth2 provider
        :return: (boolean) True if valid, False otherwise
        """
        credentials = self.original_credentials.get(provider_name, None)
        if credentials:
            key = credentials.get('consumer_key', None)
            secret = credentials.get('consumer_secret', None)
            if key and secret:
                return True
        return False

    def get_name(self, provider_slug):
        """
        Returns the humanized name for a valid oauth/oauth2 provider.
        :param provide_slug: (string) slug for a valid oauth/oauth2 provider
        :return: (string|None) humanized name of a valid oauth/oauth2 provider
        """
        name = self.providers.get(provider_slug, None)
        if name:
            return str(name)
        return None

    def get_slugs(self):
        return [str(slug) for slug in self.slugs]
