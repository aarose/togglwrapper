import requests
from requests.auth import HTTPBasicAuth


BASE_URL = 'https://www.toggl.com/api'
API_VERSION = 'v8'
API_URL = '{base}/{version}'.format(base=BASE_URL, version=API_VERSION)


def return_json_or_raise_error(func):
    def inner(*args, **kwargs):
        response = func(*args, **kwargs)
        try:
            return response.json()
        except ValueError:
            # JSON couldn't be decoded, raise status error
            response.raise_for_status()
    return inner


class TogglObject(object):
    @property
    def full_uri(self):
        return '{api}{uri}'.format(api=self.client.api_url, uri=self.uri)

    def __init__(self, client):
        self.client = client


class User(TogglObject):
    uri = '/me'

    @return_json_or_raise_error
    def get(self, related_data=False, since=None):
        """ Get the user associated with the current API token. """
        return requests.get(self.full_uri, auth=self.client.auth)

    def update(self, data):
        """ Update the fields. """
        pass


class Client(object):
    def __init__(self, api_token, base_url=BASE_URL, version=API_VERSION):
        self.api_url = '{base}/{version}'.format(base=base_url,
                                                 version=version)
        self.auth = HTTPBasicAuth(api_token, 'api_token')
        self.User = User(self)
