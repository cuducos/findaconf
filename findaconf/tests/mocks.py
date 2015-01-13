# coding: utf-8

from mock import Mock


class MockAuthomatic(object):

    def __init__(self, name='John Doe', email='johndoe@john.doe', error=False):
        self.name = name
        self.email = email
        if error:
            self.error = Mock()
            self.error.message = str(error)
        else:
            self.error = False

    def login(self, adapter, provider_name):
        del adapter, provider_name
        response = Mock()
        response.error = self.error
        if self.error:
            response.user = False
        else:
            user = Mock()
            user.name = self.name
            user.email = self.email
            response.user = user
        return response
