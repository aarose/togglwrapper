import json

import requests
from requests.auth import HTTPBasicAuth

from .decorators import error_checking, return_json
from .mixins import GetMixin, CreateMixin, UpdateMixin, DeleteMixin


BASE_URL = 'https://www.toggl.com/api'
API_VERSION = 'v8'
API_URL = '{base}/{version}'.format(base=BASE_URL, version=API_VERSION)


class TogglObject(object):
    """ Base class for Toggl representations to inherit from. """
    uri = None

    def __init__(self, toggl):
        self.toggl = toggl
        if self.uri is None:
            # Helper error for subclasses that forget to specify their own URI
            raise NotImplementedError('Must define a URI.')

    @classmethod
    def _compile_uri(cls, id=None, ids=None, child_uri=None):
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
        if not any((cond1, cond2, cond3)):
            raise Exception("The 'active' param must be either True, False,",
                            "or 'both'.")
        params = {'active': active}
        return super(Clients, self).get(client_id, '/projects', params=params)


class Dashboard(TogglObject, GetMixin):
    uri = 'dashboard'

    def get(self, workspace_id):
        """ Get the Dashboard for the Workspace with the given ID. """
        return super(Dashboard, self).get(id=workspace_id)


class Projects(TogglObject, GetMixin, CreateMixin, UpdateMixin, DeleteMixin):
    uri = '/projects'

    def get(self, project_id):
        """ Get the Project with the given ID. """
        return super(Projects, self).get(id=project_id)

    def get_project_users(self, project_id):
        """ Get the ProjectUsers for the Project with the given ID. """
        return super(Projects, self).get(project_id, '/project_users')

    def get_tasks(self, project_id):
        """ Get the Tasks for the Project with the given ID. """
        return super(Projects, self).get(project_id, '/tasks')


class ProjectUsers(TogglObject, CreateMixin, UpdateMixin, DeleteMixin):
    uri = '/project_users'

    def get_for_project(self, project_id):
        """ Get the ProjectUsers for the Project with the given ID. """
        return self.toggl.Projects.get_project_users(project_id)


class Tags(TogglObject, CreateMixin, UpdateMixin, DeleteMixin):
    uri = '/tags'


class Tasks(TogglObject, GetMixin, CreateMixin, UpdateMixin, DeleteMixin):
    uri = '/tasks'

    def get(self, tag_id):
        return super(Tasks, self).get(id=tag_id)

    def get_for_project(self, project_id):
        """ Get the Tasks for the Project with the given ID. """
        return self.toggl.Projects.get_tasks(project_id)


class TimeEntries(TogglObject, GetMixin, CreateMixin, UpdateMixin,
                  DeleteMixin):
    uri = '/time_entries'

    def get(self, id=None, start_date=None, end_date=None):
        """ Get the time entry. """
        params = {'start_date': start_date, 'end_date': end_date}
        return super(TimeEntries, self).get(id=id, params=params)

    def start(self, data):
        """ Start a new time entry. """
        return super(TimeEntries, self).update(child_uri='/start', data=data)

    def stop(self, time_entry_id):
        """ Stop the time entry with the given ID. """
        return super(TimeEntries, self).update(id=time_entry_id,
                                               child_uri='/stop')

    def get_current(self):
        """ Get the current running time entry. """
        return super(TimeEntries, self).get(child_uri='/current')


class User(TogglObject, GetMixin, UpdateMixin):
    uri = '/me'

    def get(self, related_data=False, since=None):
        """ Get the user associated with the current API token. """
        params = {'since': since}
        if related_data:
            params['with_related_data'] = related_data
        return super(User, self).get(params=params)

    def update(self, data):
        """ Update the user associated with the api token. """
        return super(User, self).update(data=data)


class Workspaces(TogglObject, GetMixin, UpdateMixin):
    uri = '/workspaces'

    def get_users(self, workspace_id):
        """ Get the Users for the Workspace with the given ID. """
        return super(Workspaces, self).get(workspace_id, '/users')

    def get_clients(self, workspace_id):
        """ Get the Clients for the Workspace with the given ID. """
        return super(Workspaces, self).get(workspace_id, '/clients')

    def get_projects(self, workspace_id):
        """ Get the Projects for the Workspace with the given ID. """
        return super(Workspaces, self).get(workspace_id, '/projects')

    def get_tasks(self, workspace_id):
        """ Get the Tasks for the Workspace with the given ID. """
        return super(Workspaces, self).get(workspace_id, '/tasks')

    def get_tags(self, workspace_id):
        """ Get the Tags for the Workspace with the given ID. """
        return super(Workspaces, self).get(workspace_id, '/tags')

    def get_workspace_users(self, workspace_id):
        """ Get the WorkspaceUsers for the Workspace with the given ID. """
        return super(Workspaces, self).get(workspace_id, '/workspace_users')

    def invite(self, workspace_id, data):
        """ Add users to the workspace. Sends an email invite to the users. """
        uri = '/workspaces/{wid}/invite'.format(wid=workspace_id)
        return self.toggl.post(uri, data)


class WorkspaceUsers(TogglObject, UpdateMixin, DeleteMixin):
    uri = '/workspace_users'


class Toggl(object):
    def __init__(self, api_token, base_url=BASE_URL, version=API_VERSION):
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
        Create a new user.

        Args:
          data (dict): Contains required and optional fields and values.
        """
        return self.post('/signups', data)

    def reset_token(self):
        """ Delete the current API Token and use a new token. """
        return self.post('/reset_token')

    @return_json
    @error_checking
    def get(self, uri, params=None):
        """ GET to the given uri. """
        full_uri = '{base}{uri}'.format(base=self.api_url, uri=uri)
        return requests.get(full_uri, params=params, auth=self.auth)

    @return_json
    @error_checking
    def post(self, uri, data=None):
        """ POST to the given uri with a data dict. """
        full_uri = '{base}{uri}'.format(base=self.api_url, uri=uri)
        payload = json.dumps(data) if data is not None else None
        return requests.post(full_uri, data=payload, auth=self.auth)

    @return_json
    @error_checking
    def put(self, uri, data):
        """ PUT to the given uri with a data dict. """
        full_uri = '{base}{uri}'.format(base=self.api_url, uri=uri)
        payload = json.dumps(data)
        return requests.put(full_uri, data=payload, auth=self.auth)

    @error_checking
    def delete(self, uri):
        """ DELETE to the given uri. """
        full_uri = '{base}{uri}'.format(base=self.api_url, uri=uri)
        return requests.delete(full_uri, auth=self.auth)
