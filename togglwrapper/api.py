import requests
from requests.auth import HTTPBasicAuth


BASE_URL = 'https://www.toggl.com/api'
API_VERSION = 'v8'
API_URL = '{base}/{version}'.format(base=BASE_URL, version=API_VERSION)
API_TOKEN = ''

auth = HTTPBasicAuth(API_TOKEN, 'api_token')


class TogglObject(object):
    @property
    def full_uri(self):
        return '{api}{uri}'.format(api=self.client.api_url, uri=self.uri)

    def __init__(self, client):
        self.client = client


class User(TogglObject):
    uri = '/me'

    def get(self, related_data=False, since=None):
        """ Get the user associated with the current API token. """
        response = requests.get(self.full_uri, auth=auth)
        return response.json()

    def update(self, data):
        """ Update the fields. """
        pass


class Client(object):
    def __init__(self, api_token, base_url=BASE_URL, version=API_VERSION):
        # self.api_token = api_token
        self.api_url = '{base}/{version}'.format(base=base_url,
                                                 version=version)
        self.auth = HTTPBasicAuth(self.api_token, 'api_token')
        self.user = User(self)
