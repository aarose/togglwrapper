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

    @return_json_or_raise_error
    def get(self, object_id=None):
        """ Get the array of objects, or a specific instance by ID. """
        uri = self.full_uri
        if object_id is not None:
            uri = '{uri}/{object_id}'.format(uri=uri, object_id=object_id)
        return requests.get(uri, auth=self.client.auth)

    @return_json_or_raise_error
    def create(self, data):
        """ Create a new instance of the object type. """
        return requests.post(self.full_uri, data=data, auth=self.client.auth)

    @return_json_or_raise_error
    def update(self, object_id, data):
        uri = '{uri}/{object_id}'.format(self.full_uri, object_id)
        return requests.put(uri, auth=self.client.auth)

    @return_json_or_raise_error
    def delete(self, object_id):
        return requests.delete(uri, auth=self.client.auth)


class User(TogglObject):
    uri = '/me'

    @return_json_or_raise_error
    def get(self, related_data=False, since=None):
        """ Get the user associated with the current API token. """
        return requests.get(self.full_uri, auth=self.client.auth)

    def update(self, data):
        """ Update the fields. """
        pass


class Clients(TogglObject):
    uri = '/clients'


class Workspaces(TogglObject):
    uri = '/workspaces'


class Projects(TogglObject):
    uri = '/projects'


class ProjectUsers(TogglObject):
    uri = '/project_users'


class Tags(TogglObject):
    uri = '/tags'


class Tasks(TogglObject):
    uri = '/tasks'


class TimeEntries(TogglObject):
    uri = '/time_entires'


class WorkspaceUsers(TogglObject):
    uri = '/workspace_users'


class Client(object):
    def __init__(self, api_token, base_url=BASE_URL, version=API_VERSION):
        self.api_url = '{base}/{version}'.format(base=base_url,
                                                 version=version)
        self.auth = HTTPBasicAuth(api_token, 'api_token')
        self.User = User(self)

    def signup(self):
        """ Signup a new user. """
        uri = '{}/signups'.format(self.api_url)
        requests.post(uri, auth=self.auth)

    def reset_token(self):
        """ Delete the current API Token and use a new token. """
        uri = '{}/reset_token'.format(self.api_url)
        requests.post(uri, auth=self.auth)
