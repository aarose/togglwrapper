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

    def __init__(self, toggl):
        self.toggl = toggl


class Get(object):

    def _compile_uri(self, id=None):
        uri = self.uri
        if id is not None:
            uri += '/%s' % id
        return uri

    def get_child_objects(self, parent_id, child_uri, params=None):
        """
        Get the Objects that belong to the parent Object with the given ID.

        Args:
            parent_id (int): The ID of the parent Object.
            child_uri (str): The uri of the child Object. e.g. If we wanted
              the Clients of a Workspace, where the Workspace is the parent
              object, the child-uri is '/clients'.
        """
        uri = self._compile_uri(parent_id) + child_uri
        return self.toggl.get(uri, params=params)

    def get(self, id=None, params=None):
        """ Get the array of objects, or a specific instance by ID. """
        return self.toggl.get(self._compile_uri(id), params=params)


class Create(object):
    def create(self, data):
        """ Create a new instance of the object type. """
        return self.toggl.post(self.uri, data)


class Update(object):
    def update(self, id=None, ids=None, data=None):
        """ Update a specific instance by ID, or update multiple instances. """
        if not any(id, ids) or (id and ids):
            raise Exception('Must provide either an ID or an iterable of IDs.')
        if id is not None:
            uri = '{uri}/{id}'.format(self.uri, id)
        else:
            uri = '{uri}/{ids}'.format(uri=self.uri, ids=','.join(ids))
        return self.toggl.put(uri, data)


class Delete(object):
    def delete(self, id):
        """ Delete a specific instance by ID. """
        uri = '{uri}/{id}'.format(self.uri, id)
        return self.toggl.delete(uri)


class Clients(TogglObject, Get, Create, Update, Delete):
    uri = '/clients'

    def get_projects(self, client_id, active=True):
        """
        Get the projects associated with the Client with the given ID.

        Args:
            client_id (int): The ID of the client.
            active (bool or string, optional): Must be either True, False, or
                the string 'both'. Defaults to True.
        """
        cond1 = (active is True)
        cond2 = (active is False)
        cond3 = (active is 'both')
        if not any(cond1, cond2, cond3):
            raise Exception("The 'active' param must be either True, False,",
                            "or 'both'.")
        params = {'active': active}
        return self.get_child_objects(client_id, '/projects', params=params)

    def get(self, workspace_id):
        """ Get the Dashboard for the Workspace with the given ID. """
        return super(Dashboard, self).get(id=workspace_id)


class Projects(TogglObject, Get, Create, Update, Delete):
    uri = '/projects'


class ProjectUsers(TogglObject, Create, Update, Delete):
    uri = '/project_users'



class Tags(TogglObject, Create, Update, Delete):
    uri = '/tags'


class Tasks(TogglObject, Get, Create, Update, Delete):
    uri = '/tasks'


class TimeEntries(TogglObject):
    uri = '/time_entires'


class TimeEntries(TogglObject, Get, Create, Update, Delete):
    uri = '/time_entries'

    def get(self, id=None, start_date=None, end_date=None):
        """ Get the time entry. """
        params = {'start_date': start_date, 'end_date': end_date}
        return super(TimeEntries, self).get(id=id, params=params)

    def start(self, data):
        """ Start a new time entry. """
        uri = self.uri + '/start'
        return self.toggl.post(uri, data)

    def stop(self, time_entry_id):
        """ Stop the time entry with the given ID. """
        uri = self.uri + '/{time_entry_id}'
        return self.toggl.post(uri.format(time_entry_id=time_entry_id))



    def get(self, related_data=False, since=None):
        """ Get the user associated with the current API token. """
        query = self._compile_query(related_data=related_data, since=since)
        uri = '{uri}{query}'.format(uri=self.full_uri, query=query)
        return requests.get(uri, auth=self.client.auth)

    def update(self, data):
        """ Update the user associated with the api token. """
        return self.toggl.put(self.uri, data)


class Workspaces(TogglObject, Get, Update):
    uri = '/workspaces'


class WorkspaceUsers(TogglObject, Update, Delete):
    uri = '/workspace_users'


class Toggl(object):
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
    def get(self, uri, params=None):
        """ GET to the given uri. """
        full_uri = '{base}{uri}'.format(base=self.api_url, uri=uri)
        return requests.get(full_uri, params=params, auth=self.auth)

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
