import json

import requests
from requests.auth import HTTPBasicAuth

from errors import AuthError


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
            if response.status_code == 403:
                raise AuthError('Incorrect API token.')
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
        uri = '{uri}/{object_id}'.format(self.full_uri, object_id)
        return requests.delete(uri, auth=self.client.auth)


class Clients(TogglObject):
    uri = '/clients'


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


class User(TogglObject):
    uri = '/me'

    def _compile_query(self, related_data=False, since=None):
        """ Returns the querystring. """
        query = '?with_related_data=true' if related_data else ''
        if related_data and since is not None:
            query += '&'
        if since is not None:
            query += '?since={}'.format(since)
        return query

    @return_json_or_raise_error
    def get(self, related_data=False, since=None):
        """ Get the user associated with the current API token. """
        query = self._compile_query(related_data=related_data, since=since)
        uri = '{uri}{query}'.format(uri=self.full_uri, query=query)
        return requests.get(uri, auth=self.client.auth)

    def update(self, data):
        """ Update the fields. """
        return requests.put(self.full_uri, data=data, auth=self.client.auth)


class Workspaces(TogglObject):
    uri = '/workspaces'


class WorkspaceUsers(TogglObject):
    uri = '/workspace_users'


class Client(object):
    def __init__(self, api_token, base_url=BASE_URL, version=API_VERSION):
        self.api_url = '{base}/{version}'.format(base=base_url,
                                                 version=version)
        self.auth = HTTPBasicAuth(api_token, 'api_token')
        self.Clients = Clients(self)
        self.User = User(self)
        self.Projects = Projects(self)
        self.ProjectUsers = ProjectUsers(self)
        self.Tags = Tags(self)
        self.Tasks = Tasks(self)
        self.TimeEntries = TimeEntries(self)
        self.User = User(self)
        self.Workspaces = Workspaces(self)
        self.WorkspaceUsers = WorkspaceUsers(self)

    def signups(self, user_info):
        """
        Create a new user.

        Args:
          user_info (dict): Values for all the required and optional fields.
        """
        return self.post('/signups', {'user': user_info})

    def reset_token(self):
        """ Delete the current API Token and use a new token. """
        return self.post('/reset_token')

    @return_json_or_raise_error
    def get(self, uri):
        """ GET to the given uri. """
        full_uri = '{base}{uri}'.format(base=self.api_url, uri=uri)
        return requests.get(full_uri, auth=self.auth)

    @return_json_or_raise_error
    def post(self, uri, data=None):
        """ POST to the given uri with a data dict. """
        full_uri = '{base}{uri}'.format(base=self.api_url, uri=uri)
        payload = json.dumps(data) if data is not None else None
        return requests.post(full_uri, data=payload, auth=self.auth)

    @return_json_or_raise_error
    def put(self, uri, data):
        """ PUT to the given uri with a data dict. """
        full_uri = '{base}{uri}'.format(base=self.api_url, uri=uri)
        payload = json.dumps(data)
        return requests.put(full_uri, data=payload, auth=self.auth)

    @return_json_or_raise_error
    def delete(self, uri):
        """ DELETE to the given uri. """
        full_uri = '{base}{uri}'.format(self.api_url, uri)
        return requests.delete(full_uri, auth=self.auth)
