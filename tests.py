# -*- coding: utf-8 -*-

"""
tests
-----

Ensures that certain actions in the togglwrapper library result in certain
behaviours.

Uses the responses library to mock out the requests library, and loads fixtures
from ``fixtures/`` for the mock JSON response output.
"""

import json
import os
import unittest

import responses
from requests.exceptions import HTTPError


from togglwrapper import api
from togglwrapper.exceptions import AuthError


FAKE_TOKEN = 'fake_token_1'
FIXTURES_PATH = '%s/fixtures' % os.path.dirname(os.path.abspath(__file__))


class TestTogglBase(unittest.TestCase):
    """ Class to establish utility methods for Test classes. """

    api_token = FAKE_TOKEN
    focus_class = None

    def compile_full_url(self, id=None, ids=None, child_uri=None):
        """ Compile a full URL from the base url. """
        focus_class = self.focus_class
        uri = focus_class._compile_uri(id=id, ids=ids, child_uri=child_uri)
        return self.toggl.api_url + uri

    def setUp(self):
        self.toggl = api.Toggl(self.api_token)

    def get_json(self, filename):
        """ Return the JSON data in the .json file with the given filename. """
        file_path = '{path}/{filename}.json'.format(path=FIXTURES_PATH,
                                                    filename=filename)
        with open(file_path) as json_file:
            json_dict = json.load(json_file)
            json_file.close()
        raw_json = json.dumps(json_dict)
        return raw_json

    def responses_add(self, method, filename=None, id=None, ids=None,
                      child_uri=None, status_code=200, content_type=''):
        """ Adds a mock response for requests to a certain url. """
        body = None
        if filename is not None:
            body = self.get_json(filename)
            content_type = 'application/json'

        responses.add(
            getattr(responses, method),
            self.compile_full_url(id=id, ids=ids, child_uri=child_uri),
            body=body,
            status=status_code,
            content_type=content_type
        )


class TestToggl(TestTogglBase):
    """ Tests the main Toggl client Class. """

    @responses.activate
    def test_wrong_token(self):
        """ Should raise exception when wrong API token is provided. """
        full_url = self.toggl.api_url + self.toggl.User.uri
        responses.add(responses.GET, full_url, status=403)
        self.assertRaises(AuthError, self.toggl.User.get)
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_failed_request(self):
        """ Should raise an HTTPError with status code 404. """
        full_url = self.toggl.api_url + self.toggl.TimeEntries.uri
        responses.add(
            responses.POST,
            full_url,
            body=self.get_json('failed_request'),
            status=404,
        )
        wrong_data = {"time_entry": {
            "description": "New time entry",
            "created_with": "API example code"
        }}
        self.assertRaises(HTTPError, self.toggl.TimeEntries.create,
                          data=wrong_data)
        # Ensure that the error message in the response is the exception reason
        reason = json.loads(self.get_json('failed_request'))
        try:
            self.toggl.TimeEntries.create(data=wrong_data)
        except HTTPError as e:
            self.assertEqual(e.response.reason, reason)
        else:
            raise Exception('Reason was not correct.')

        # Ensure that the mocked response was triggered twice
        self.assertEqual(len(responses.calls), 2)


class TestClients(TestTogglBase):
    focus_class = api.Clients

    @responses.activate
    def test_create(self):
        """ Should create a new Client. """
        self.responses_add('POST', filename='client_create')
        create_data = {"client": {"name": "Very Big Company", "wid": 777}}
        response = self.toggl.Clients.create(create_data)
        self.assertEqual(type(response), dict)
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_get_by_id(self):
        """ Should get a specific Client by ID. """
        inst_id = 1239455
        self.responses_add('GET', filename='client_get', id=inst_id)
        response = self.toggl.Clients.get(id=inst_id)
        self.assertEqual(type(response), dict)
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_get(self):
        """ Should get all Clients. """
        self.responses_add('GET', filename='clients_get')
        response = self.toggl.Clients.get()
        self.assertEqual(type(response), list)
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_update(self):
        """ Should update a Client. """
        inst_id = 1239455
        self.responses_add('PUT', filename='client_update', id=inst_id)
        update_data = {
            "client": {
                "name": "Very Big Company",
                "notes": "something about the client"
            }
        }
        response = self.toggl.Clients.update(id=inst_id, data=update_data)
        self.assertEqual(type(response), dict)
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_delete(self):
        """ Should delete a Client. """
        inst_id = 1239455
        self.responses_add('DELETE', id=inst_id)

        response = self.toggl.Clients.delete(inst_id)
        self.assertTrue(response.ok)
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_projects_get(self):
        """ Should get all active projects under the Client. """
        inst_id = 1239455
        self.responses_add(
            'GET',
            filename='client_projects_get',
            id=inst_id,
            child_uri='/projects'
        )
        response = self.toggl.Clients.get_projects(inst_id)
        self.assertEqual(type(response), list)
        self.assertEqual(len(responses.calls), 1)


class TestDashboard(TestTogglBase):
    focus_class = api.Dashboard

    @responses.activate
    def test_get(self):
        """ Should get the dashboard info for a given Workspace. """
        inst_id = 3134975
        self.responses_add('GET', filename='dashboard', id=inst_id)
        response = self.toggl.Dashboard.get(inst_id)
        self.assertEqual(type(response), dict)
        self.assertEqual(len(responses.calls), 1)


class TestProjects(TestTogglBase):
    focus_class = api.Projects

    @responses.activate
    def test_create(self):
        """ Should create a new Project. """
        self.responses_add('POST', filename='project_create')
        project_data = {"project": {
            "name": "An awesome project",
            "wid": 777,
            "template_id": 10237,
            "is_private": True,
            "cid": 123397
        }}
        response = self.toggl.Projects.create(project_data)
        self.assertEqual(type(response), dict)
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_get_by_id(self):
        """ Should get a specific Project by ID. """
        inst_id = 193838628
        self.responses_add('GET', filename='project_get', id=inst_id)
        response = self.toggl.Projects.get(inst_id)
        self.assertEqual(type(response), dict)
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_update(self):
        """ Should update a Project. """
        inst_id = 193838628
        self.responses_add('PUT', filename='project_update', id=inst_id)
        update_data = {"project": {
            "name": "Changed the name",
            "is_private": False,
            "cid": 123398,
            "color": "6"
        }}
        response = self.toggl.Projects.update(id=inst_id, data=update_data)
        self.assertEqual(type(response), dict)
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_delete(self):
        """ Should delete a Project. """
        inst_id = 4692190
        self.responses_add('DELETE', id=inst_id)
        response = self.toggl.Projects.delete(inst_id)
        self.assertTrue(response.ok)
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_mass_delete(self):
        """ Should delete multiple Projects. """
        ids = [4692190, 4692192, 4692193]
        self.responses_add('DELETE', ids=ids)
        response = self.toggl.Projects.delete(ids=ids)
        self.assertTrue(response.ok)
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_project_users_get(self):
        """ Should get Project Users under the Project. """
        inst_id = 193838628
        fixture_name = 'project_projectusers_get'
        self.responses_add(
            'GET',
            filename=fixture_name,
            id=inst_id,
            child_uri='/project_users'
        )
        response = self.toggl.Projects.get_project_users(inst_id)
        self.assertEqual(type(response), list)
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_tasks_get(self):
        """ Should get Tasks under the Project. """
        inst_id = 777
        self.responses_add(
            'GET',
            filename='project_tasks_get',
            id=inst_id,
            child_uri='/tasks'
        )
        response = self.toggl.Projects.get_tasks(inst_id)
        self.assertEqual(type(response), list)
        self.assertEqual(len(responses.calls), 1)


class TestProjectUsers(TestTogglBase):
    focus_class = api.ProjectUsers

    @responses.activate
    def test_create(self):
        """ Should create a new ProjectUser. """
        self.responses_add('POST', filename='projectuser_create')
        create_data = {
            "project_user": {
                "pid": 777,
                "uid": 123,
                "rate": 4.0,
                "manager": True
            }
        }
        response = self.toggl.ProjectUsers.create(create_data)
        self.assertEqual(type(response), dict)
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_update(self):
        """ Should update a ProjectUser. """
        inst_id = 4692190
        self.responses_add('PUT', filename='projectuser_update', id=inst_id)
        update_data = {
            "project_user": {
                "manager": False,
                "rate": 15,
                "fields": "fullname"
            }
        }
        response = self.toggl.ProjectUsers.update(id=inst_id, data=update_data)
        self.assertEqual(type(response), dict)
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_delete(self):
        """ Should delete a ProjectUser. """
        inst_id = 4692190
        self.responses_add('DELETE', id=inst_id)
        response = self.toggl.ProjectUsers.delete(inst_id)
        self.assertTrue(response.ok)
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_mass_create(self):
        """ Should create multiple new ProjectUsers. """
        self.responses_add('POST', 'projectusers_create_multiple')
        create_data = {"project_user": {
            "pid": 777,
            "uid": "1267998,29624,112047",
            "rate": 4.0,
            "manager": True,
            "fields": "fullname"
        }}
        response = self.toggl.ProjectUsers.create(create_data)
        self.assertEqual(type(response), dict)
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_mass_update(self):
        """ Should update multiple ProjectUsers. """
        ids = (4692190, 4692192, 4692191)
        self.responses_add('PUT', 'projectusers_update_multiple', ids=ids)
        update_data = {
            "project_user": {
                "manager": False,
                "rate": 15,
                "fields": "fullname"
            }
        }
        response = self.toggl.ProjectUsers.update(ids=ids, data=update_data)
        self.assertEqual(type(response), dict)
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_mass_delete(self):
        """ Should delete multiple ProjectUsers. """
        ids = (4692190, 4692192, 4692193)
        self.responses_add('DELETE', ids=ids)
        response = self.toggl.ProjectUsers.delete(ids=ids)
        self.assertTrue(response.ok)
        self.assertEqual(len(responses.calls), 1)


class TestTags(TestTogglBase):
    focus_class = api.Tags

    @responses.activate
    def test_create(self):
        """ Should create a new Tag. """
        self.responses_add('POST', filename='tag_create')
        create_data = {"tag": {"name": "billed", "wid": 777}}
        response = self.toggl.Tags.create(create_data)
        self.assertEqual(type(response), dict)
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_update(self):
        """ Should update a Tag. """
        inst_id = 1239455
        self.responses_add('PUT', filename='tag_update', id=inst_id)
        update_data = {"tag": {"name": "not billed"}}
        response = self.toggl.Tags.update(id=inst_id, data=update_data)
        self.assertEqual(type(response), dict)
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_delete(self):
        """ Should delete a Tag. """
        inst_id = 1239455
        self.responses_add('DELETE', id=inst_id)
        response = self.toggl.Tags.delete(inst_id)
        self.assertTrue(response.ok)
        self.assertEqual(len(responses.calls), 1)


class TestTasks(TestTogglBase):
    focus_class = api.Tasks

    @responses.activate
    def test_create(self):
        """ Should create a new Task. """
        self.responses_add('POST', filename='task_create')
        create_data = {"task": {"name": "A new task", "pid": 777}}
        response = self.toggl.Tasks.create(create_data)
        self.assertEqual(type(response), dict)
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_get_by_id(self):
        """ Should get a Task. """
        inst_id = 1335076912
        self.responses_add('GET', filename='task_get', id=inst_id)
        response = self.toggl.Tasks.get(inst_id)
        self.assertEqual(type(response), dict)
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_update(self):
        """ Should update a Task. """
        inst_id = 1335076912
        self.responses_add('PUT', filename='task_update', id=inst_id)
        update_data = {
            "task": {
                "active": False,
                "estimated_seconds": 3600,
                "fields": "done_seconds,uname"
            }
        }
        response = self.toggl.Tasks.update(id=inst_id, data=update_data)
        self.assertEqual(type(response), dict)
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_delete(self):
        """ Should delete a Task. """
        inst_id = 1335076912
        self.responses_add('DELETE', id=inst_id)
        response = self.toggl.Tasks.delete(inst_id)
        self.assertTrue(response.ok)
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_mass_update(self):
        """ Should update multiple Tasks. """
        ids = (1335076912, 1335076911)
        self.responses_add('PUT', 'projectusers_update_multiple', ids=ids)
        update_data = {"task": {
            "active": False,
            "fields": "done_seconds,uname"
        }}
        response = self.toggl.Tasks.update(ids=ids, data=update_data)
        self.assertEqual(type(response), dict)
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_mass_delete(self):
        """ Should delete multiple Tasks. """
        ids = (1335076912, 1335076911, 1335076910)
        self.responses_add('DELETE', ids=ids)
        response = self.toggl.Tasks.delete(ids=ids)
        self.assertTrue(response.ok)
        self.assertEqual(len(responses.calls), 1)


class TestTimeEntries(TestTogglBase):
    focus_class = api.TimeEntries

    @responses.activate
    def test_create(self):
        """ Should create a new TimeEntry. """
        self.responses_add('POST', filename='time_entry_create')
        create_data = {"time_entry": {
            "description": "Meeting with possible clients",
            "tags": ["billed"],
            "duration": 1200,
            "start": "2013-03-05T07:58:58.000Z",
            "pid": 123,
            "created_with": "togglwrapper"
        }}
        response = self.toggl.TimeEntries.create(create_data)
        self.assertEqual(type(response), dict)
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_start(self):
        """ Should start a TimeEntry. """
        self.responses_add('POST', 'time_entry_start', child_uri='/start')
        start_data = {"time_entry": {
            "description": "Meeting with possible clients",
            "tags": ["billed"],
            "pid": 123,
            "created_with": "togglwrapper"
        }}
        response = self.toggl.TimeEntries.start(start_data)
        self.assertEqual(type(response), dict)
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_stop(self):
        """ Should stop a TimeEntry. """
        inst_id = 436694100
        self.responses_add(
            'PUT',
            filename='time_entry_stop',
            id=inst_id,
            child_uri='/stop'
        )
        response = self.toggl.TimeEntries.stop(inst_id)
        self.assertEqual(type(response), dict)
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_get_by_id(self):
        """ Should get a TimeEntry. """
        inst_id = 436694100
        self.responses_add('GET', filename='time_entry_get', id=inst_id)
        response = self.toggl.TimeEntries.get(id=inst_id)
        self.assertEqual(type(response), dict)
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_get_current(self):
        """ Should get the current running TimeEntry. """
        self.responses_add('GET', 'time_entry_current', child_uri='/current')
        response = self.toggl.TimeEntries.get_current()
        self.assertEqual(type(response), dict)
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_get_in_time_range(self):
        """ Should get the TimeEntries started in a specific time range. """
        self.responses_add('GET', filename='time_entries_get_in_range')
        response = self.toggl.TimeEntries.get(
            start_date='2013-03-10T15:42:46+02:00',
            end_date='2013-03-12T15:42:46+02:00'
        )
        self.assertEqual(type(response), list)
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_update(self):
        """ Should update a TimeEntry. """
        inst_id = 436694100
        self.responses_add('PUT', filename='time_entry_update', id=inst_id)
        update_data = {"time_entry": {
            "description": "Meeting with possible clients",
            "tags": [""],
            "duration": 1240,
            "start": "2013-03-05T07:58:58.000Z",
            "stop": "2013-03-05T08:58:58.000Z",
            "duronly": True,
            "pid": 123,
            "billable": True
        }}
        response = self.toggl.TimeEntries.update(id=inst_id, data=update_data)
        self.assertEqual(type(response), dict)
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_delete(self):
        """ Should delete a TimeEntry. """
        inst_id = 1239455
        self.responses_add('DELETE', id=inst_id)
        response = self.toggl.TimeEntries.delete(inst_id)
        self.assertTrue(response.ok)
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_mass_update(self):
        """ Should update multiple TimeEntries. """
        ids = (436694100, 436694101)
        self.responses_add('PUT', 'projectusers_update_multiple', ids=ids)
        update_data = {"time_entry": {
            "tags": ["billed", "productive"],
            "tag_action": "add"
        }}
        response = self.toggl.TimeEntries.update(ids=ids, data=update_data)
        self.assertEqual(type(response), dict)
        self.assertEqual(len(responses.calls), 1)


class TestUser(TestTogglBase):
    focus_class = api.User

    @responses.activate
    def test_get(self):
        """ Should successfully get the User associated with the token. """
        self.responses_add('GET', filename='user_get')
        response = self.toggl.User.get()
        self.assertEqual(type(response), dict)
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_get_with_related_data(self):
        """ Should get the User associated with the token and related data. """
        self.responses_add('GET', filename='user_get_with_related_data')
        response = self.toggl.User.get(related_data=True)
        self.assertEqual(type(response), dict)
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_update(self):
        """ Should update the User associated with the api token. """
        self.responses_add('PUT', filename='user_update')
        update_data = {"user": {"fullname": "John Smith"}}
        response = self.toggl.User.update(update_data)
        self.assertEqual(type(response), dict)
        self.assertEqual(len(responses.calls), 1)


class TestWorkspaces(TestTogglBase):
    focus_class = api.Workspaces

    @responses.activate
    def test_get(self):
        """ Should successfully get an iterable of Workspaces. """
        self.responses_add('GET', filename='workspaces_get')
        response = self.toggl.Workspaces.get()
        self.assertEqual(type(response), list)
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_get_by_id(self):
        """ Should successfully get a specific Workspace. """
        inst_id = 3134975
        self.responses_add('GET', filename='workspace_get', id=inst_id)
        response = self.toggl.Workspaces.get(id=inst_id)
        self.assertEqual(type(response), dict)
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_update(self):
        """ Should update a specific Workspace. """
        inst_id = 3134975
        self.responses_add('PUT', filename='workspace_update', id=inst_id)
        update_data = {"workspace": {
            "default_currency": "EUR",
            "default_hourly_rate": 50,
            "name": "John's ws",
            "only_admins_may_create_projects": False,
            "only_admins_see_billable_rates": True,
            "rounding": 1,
            "rounding_minutes": 60
        }}
        response = self.toggl.Workspaces.update(id=inst_id, data=update_data)
        self.assertEqual(type(response), dict)
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_users_get(self):
        """ Should get Users under the Workspace. """
        inst_id = 777
        self.responses_add('GET', filename='workspace_users', id=inst_id,
                           child_uri='/users')
        response = self.toggl.Workspaces.get_users(inst_id)
        self.assertEqual(type(response), list)
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_clients_get(self):
        """ Should get Clients under the Workspace. """
        inst_id = 777
        self.responses_add('GET', filename='workspace_clients', id=inst_id,
                           child_uri='/clients')
        response = self.toggl.Workspaces.get_clients(inst_id)
        self.assertEqual(type(response), list)
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_projects_get(self):
        """ Should get Projects under the Workspace. """
        inst_id = 777
        self.responses_add('GET', 'workspace_projects', id=inst_id,
                           child_uri='/projects')
        response = self.toggl.Workspaces.get_projects(inst_id)
        self.assertEqual(type(response), list)
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_tasks_get(self):
        """ Should get Tasks under the Workspace. """
        inst_id = 777
        self.responses_add('GET', 'workspace_tasks', id=inst_id,
                           child_uri='/tasks')
        response = self.toggl.Workspaces.get_tasks(inst_id)
        self.assertEqual(type(response), list)
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_tags_get(self):
        """ Should get Tags under the Workspace. """
        inst_id = 777
        self.responses_add('GET', 'workspace_tags', id=inst_id,
                           child_uri='/tags')
        response = self.toggl.Workspaces.get_tags(inst_id)
        self.assertEqual(type(response), list)
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_workspace_users_get(self):
        """ Should get WorkspaceUsers under the Workspace. """
        inst_id = 777
        self.responses_add('GET', 'workspace_workspaceusers', id=inst_id,
                           child_uri='/workspace_users')
        response = self.toggl.Workspaces.get_workspace_users(inst_id)
        self.assertEqual(type(response), list)
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_invite(self):
        """ Should invite users to the given Workspace. """
        inst_id = 777
        self.responses_add('POST', 'workspace_invite', id=inst_id,
                           child_uri='/invite')
        data = {"emails": ["john.doe@toggl.com", "Jane.Swift@toggl.com"]}
        response = self.toggl.Workspaces.invite(inst_id, data)
        self.assertEqual(type(response), dict)
        self.assertEqual(len(responses.calls), 1)


class TestWorkspaceUsers(TestTogglBase):
    focus_class = api.WorkspaceUsers

    @responses.activate
    def test_update(self):
        """ Should update a specific WorkspaceUser. """
        inst_id = 19012628
        self.responses_add('PUT', filename='workspaceuser_update', id=inst_id)
        update_data = {"workspace_user": {"admin": False}}
        response = self.toggl.WorkspaceUsers.update(inst_id, data=update_data)
        self.assertEqual(type(response), dict)
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_delete(self):
        """ Should delete a specific WorkspaceUser. """
        inst_id = 19012628
        self.responses_add('DELETE', id=inst_id)
        response = self.toggl.WorkspaceUsers.delete(inst_id)
        self.assertTrue(response.ok)
        self.assertEqual(len(responses.calls), 1)


if __name__ == '__main__' and __package__ is None:
    __package__ = "toggl"
    unittest.main()
