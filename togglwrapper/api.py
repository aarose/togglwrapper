# -*- coding: utf-8 -*-

"""
togglwrapper.api
"""

import json

import requests
from requests.auth import HTTPBasicAuth

from .decorators import error_checking, return_json
from .mixins import GetMixin, CreateMixin, UpdateMixin, DeleteMixin


BASE_URL = 'https://www.toggl.com/api'
API_VERSION = 'v8'
API_URL = '{base}/{version}'.format(base=BASE_URL, version=API_VERSION)


class TogglObject(object):
    """ Base class for Toggl object representations to inherit from. """
    uri = None

    def __init__(self, toggl):
        self.toggl = toggl
        if self.uri is None:
            # Helper error for subclasses that forget to specify their own URI
            raise NotImplementedError('Must define a URI.')

    @classmethod
    def _compile_uri(cls, id=None, ids=None, child_uri=None):
        """
        Returns the path to append to the base API URL.

        Args:
            id (int, optional): The ID of the object instance. Defaults to
                None.
            ids (iterable of ints, optional): An iterable of IDs of the
                multiple instances to target. Defaults to None.
            child_uri (str, optional): The sub-URI/path to access child objects
                or methods/actions.
        """
        if id and ids:
            raise Exception('Cannot use both an ID and an iterable of IDs.')
        uri = cls.uri
        if id:
            uri += '/{}'.format(id)
        if ids:
            uri += '/{}'.format(','.join([str(int_id) for int_id in ids]))
        if child_uri:
            uri += child_uri
        return uri


class Clients(TogglObject, GetMixin, CreateMixin, UpdateMixin, DeleteMixin):
    """
    The :class:`Clients <Clients>` object.

    Groups all actions relating to Clients together.
    """
    uri = '/clients'

    def get_projects(self, client_id, active=True):
        """
        Gets the projects associated with the Client with the given ID.

        Args:
            client_id (int): The ID of the client.
            active (bool or string, optional): Must be either True, False, or the string 'both'. Defaults to True.
        """
        cond1 = (active is True)
        cond2 = (active is False)
        cond3 = (active is 'both')
        if not any((cond1, cond2, cond3)):
            raise Exception("The 'active' param must be either True, False,",
                            "or 'both'.")
        params = {'active': active}
        return super(Clients, self).get(client_id, '/projects', params=params)


class Dashboard(TogglObject, GetMixin):
    uri = 'dashboard'

    def get(self, workspace_id):
        """ Gets the Dashboard for the Workspace with the given ID. """
        return super(Dashboard, self).get(id=workspace_id)


class Projects(TogglObject, GetMixin, CreateMixin, UpdateMixin, DeleteMixin):
    uri = '/projects'

    def get(self, project_id):
        """ Gets the Project with the given ID. """
        return super(Projects, self).get(id=project_id)

    def get_project_users(self, project_id):
        """ Gets the ProjectUsers for the Project with the given ID. """
        return super(Projects, self).get(project_id, '/project_users')

    def get_tasks(self, project_id):
        """ Gets the Tasks for the Project with the given ID. """
        return super(Projects, self).get(project_id, '/tasks')


class ProjectUsers(TogglObject, CreateMixin, UpdateMixin, DeleteMixin):
    uri = '/project_users'

    def get_for_project(self, project_id):
        """ Gets the ProjectUsers for the Project with the given ID. """
        return self.toggl.Projects.get_project_users(project_id)


class Tags(TogglObject, CreateMixin, UpdateMixin, DeleteMixin):
    uri = '/tags'


class Tasks(TogglObject, GetMixin, CreateMixin, UpdateMixin, DeleteMixin):
    uri = '/tasks'

    def get(self, tag_id):
        """ Gets the Task instance with the given ID. """
        return super(Tasks, self).get(id=tag_id)

    def get_for_project(self, project_id):
        """ Gets the Tasks for the Project with the given ID. """
        return self.toggl.Projects.get_tasks(project_id)


class TimeEntries(TogglObject, GetMixin, CreateMixin, UpdateMixin,
                  DeleteMixin):
    uri = '/time_entries'

    def get(self, id=None, start_date=None, end_date=None):
        """
        Gets a time entry, or time entires in a time range, or the latest ones.

        If neither an ID or time range is given, returns the time entries
        started during the last 9 days. The limit of returned time entries
        is 1000. So only the first 1000 found time entries are returned.

        Args:
            id (int, optional): The ID of the specific instance to get.
                Defaults to None.
            start_date (str, optional): Must be ISO 8601 date and time strings.
                e.g. '2013-03-10T15:42:46+02:00'. Defaults to None.
            end_date (str, optional): Must be ISO 8601 date and time strings.
                e.g. '2013-03-10T15:42:46+02:00'. Defaults to None.
        """
        params = {'start_date': start_date, 'end_date': end_date}
        return super(TimeEntries, self).get(id=id, params=params)

    def start(self, data):
        """ Starts a new time entry. """
        return super(TimeEntries, self).create(child_uri='/start', data=data)

    def stop(self, time_entry_id):
        """ Stops the time entry with the given ID. """
        return super(TimeEntries, self).update(id=time_entry_id,
                                               child_uri='/stop')

    def get_current(self):
        """ Gets the current running time entry. """
        return super(TimeEntries, self).get(child_uri='/current')


class User(TogglObject, GetMixin, UpdateMixin):
    uri = '/me'

    def get(self, related_data=False, since=None):
        """
        Gets the User associated with the current API token.

        Args:
            related_data (bool): If True, gets all the workspaces, clients,
                projects, tasks, time entries and tags which the user can see.
                Defaults to False.
            since (str or int, optional): Get objects which have changed after
                a certain time. The value should be a unix timestamp
                (e.g. 1362579886). Defaults to None.
        """
        params = {'since': since}
        if related_data:
            params['with_related_data'] = related_data
        return super(User, self).get(params=params)

    def update(self, data):
        """
        Updates the user associated with the api token.

        Args:
            data (dict): The dict of information to update for the user.
        """
        return super(User, self).update(data=data)


class Workspaces(TogglObject, GetMixin, UpdateMixin):
    uri = '/workspaces'

    def get_users(self, workspace_id):
        """ Gets the Users for the Workspace with the given ID. """
        return super(Workspaces, self).get(workspace_id, '/users')

    def get_clients(self, workspace_id):
        """ Gets the Clients for the Workspace with the given ID. """
        return super(Workspaces, self).get(workspace_id, '/clients')

    def get_projects(self, workspace_id):
        """ Gets the Projects for the Workspace with the given ID. """
        return super(Workspaces, self).get(workspace_id, '/projects')

    def get_tasks(self, workspace_id):
        """ Gets the Tasks for the Workspace with the given ID. """
        return super(Workspaces, self).get(workspace_id, '/tasks')

    def get_tags(self, workspace_id):
        """ Gets the Tags for the Workspace with the given ID. """
        return super(Workspaces, self).get(workspace_id, '/tags')

    def get_workspace_users(self, workspace_id):
        """ Gets the WorkspaceUsers for the Workspace with the given ID. """
        return super(Workspaces, self).get(workspace_id, '/workspace_users')

    def invite(self, workspace_id, data):
        """
        Adds users to the workspace. Sends an email invite to the users.

        Args:
            workspace_id (int): The ID of the workspace to invite the user to.
            data (dict): The information needed to invite the right user.
        """
        uri = '/workspaces/{wid}/invite'.format(wid=workspace_id)
        return self.toggl.post(uri, data)


class WorkspaceUsers(TogglObject, UpdateMixin, DeleteMixin):
    uri = '/workspace_users'


class Toggl(object):
    """
    Class to collect all Toggl objects in one place.

    Ensures easy authentication, since API credentials only need to be provided
    upon instantiation.
    """
    def __init__(self, api_token, base_url=BASE_URL, version=API_VERSION):
        """
        Initializes the Toggl client object.

        Args:
            api_token (str): The Toggl API token. Can be found at
                https://www.toggl.com/app/profile
            base_url (str): The base API URL. Defaults to
                `https://www.toggl.com/api`.
            version (str): The version of the API. Used to compile the full
                URL. Defaults to `v8`.
        """
        self.api_url = '{base}/{version}'.format(base=base_url,
                                                 version=version)
        self.auth = HTTPBasicAuth(api_token, 'api_token')
        self.Clients = Clients(self)
        self.Dashboard = Dashboard(self)
        self.Projects = Projects(self)
        self.ProjectUsers = ProjectUsers(self)
        self.Tags = Tags(self)
        self.Tasks = Tasks(self)
        self.TimeEntries = TimeEntries(self)
        self.User = User(self)
        self.Workspaces = Workspaces(self)
        self.WorkspaceUsers = WorkspaceUsers(self)

    def signups(self, data):
        """
        Creates a new user.

        Args:
          data (dict): Contains required and optional fields and values.
        """
        return self.post('/signups', data)

    def reset_token(self):
        """ Deletes the current API Token and returns a new token. """
        return self.post('/reset_token')

    @return_json
    @error_checking
    def get(self, uri, params=None):
        """
        GETs to the given URI.

        Args:
            uri (str): The URI/path to append to the full API URL.
            params (dict, optional): Extra parameters/querystrings to accompany the GET request.
        """
        full_uri = '{base}{uri}'.format(base=self.api_url, uri=uri)
        return requests.get(full_uri, params=params, auth=self.auth)

    @return_json
    @error_checking
    def post(self, uri, data=None):
        """
        POSTs to the given URI.

        Args:
            uri (str): The URI/path to append to the full API URL.
            data (optional): dict, bytes, or file-like object to POST.
        """
        full_uri = '{base}{uri}'.format(base=self.api_url, uri=uri)
        payload = json.dumps(data) if data is not None else None
        return requests.post(full_uri, data=payload, auth=self.auth)

    @return_json
    @error_checking
    def put(self, uri, data):
        """
        PUTs to the given URI with a data.

        Args:
            uri (str): The URI/path to append to the full API URL.
            data: dict, bytes, or file-like object to PUT.
        """
        full_uri = '{base}{uri}'.format(base=self.api_url, uri=uri)
        payload = json.dumps(data)
        return requests.put(full_uri, data=payload, auth=self.auth)

    @error_checking
    def delete(self, uri):
        """ DELETEs to the given URI. """
        full_uri = '{base}{uri}'.format(base=self.api_url, uri=uri)
        return requests.delete(full_uri, auth=self.auth)
