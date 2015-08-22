import json
import os
import unittest

import responses

from togglwrapper import api
from togglwrapper.exceptions import AuthError


FAKE_TOKEN = 'fake_token_1'
FIXTURES_PATH = '%s/fixtures' % os.path.dirname(os.path.abspath(__file__))


class TestTogglBase(unittest.TestCase):
    """ Class to establish utility methods for Test classes. """

    api_token = FAKE_TOKEN
    focus_class = None

    def compile_full_url(self, id=None, ids=None, sub_uri=None):
        """ Compile a full URL from the base url. """
        uri = self.focus_class._compile_uri(id=id, ids=ids, sub_uri=sub_uri)
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
                      sub_uri=None, status_code=200, content_type=''):
        """ Adds a mock response for requests to a certain url. """
        body = None
        if filename is not None:
            body = self.get_json(filename)
            content_type = 'application/json'

        responses.add(
            getattr(responses, method),
            self.compile_full_url(id=id, ids=ids, sub_uri=sub_uri),
            body=body,
            status=status_code,
            content_type=content_type
        )


class TestToggl(TestTogglBase):

    @responses.activate
    def test_wrong_token(self):
        """ Should raise exception when wrong API token is provided. """
        full_url = self.toggl.api_url + self.toggl.User.uri
        responses.add(responses.GET, full_url, status=403)
        self.assertRaises(AuthError, self.toggl.User.get)
        self.assertEqual(len(responses.calls), 1)


class TestClients(TestTogglBase):
    focus_class = api.Clients

    @responses.activate
    def test_create(self):
        """ Should create a new Client. """
        self.responses_add('POST', filename='client_create')
        new_client_data = {"client": {"name": "Very Big Company", "wid": 777}}
        response = self.toggl.Clients.create(new_client_data)
        self.assertEqual(type(response), dict)
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_get_by_id(self):
        """ Should get a specific Client by ID. """
        inst_id = 1239455
        self.responses_add('GET', filename='client_get', id=inst_id)
        response = self.toggl.Clients.get(id=inst_id)
        self.assertTrue(response)
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_get(self):
        """ Should get all Clients. """
        self.responses_add('GET', filename='clients_get')
        response = self.toggl.Clients.get()
        self.assertTrue(response)
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
        self.assertTrue(response)
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_delete(self):
        """ Should delete a Client. """
        inst_id = 1239455
        self.responses_add('DELETE', id=inst_id)

        response = self.toggl.Clients.delete(inst_id)
        self.assertTrue(response)
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_projects_get(self):
        """ Should get all active projects under the Client. """
        inst_id = 1239455
        self.responses_add(
            'GET',
            filename='client_projects_get',
            id=inst_id,
            sub_uri='/projects'
        )
        response = self.toggl.Clients.get_projects(inst_id)
        self.assertTrue(response)
        self.assertEqual(len(responses.calls), 1)


class TestDashboard(TestTogglBase):
    focus_class = api.Dashboard

    @responses.activate
    def test_get(self):
        """ Should get the dashboard info for a given Workspace. """
        inst_id = 3134975
        self.responses_add('GET', filename='dashboard', id=inst_id)
        response = self.toggl.Dashboard.get(inst_id)
        self.assertTrue(response)
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
        self.assertTrue(response)
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_get(self):
        """ Should get a specific Project by ID. """
        inst_id = 193838628
        self.responses_add('GET', filename='project_get', id=inst_id)
        response = self.toggl.Projects.get(inst_id)
        self.assertTrue(response)
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
        self.assertTrue(response)
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_delete(self):
        """ Should delete a Project. """
        inst_id = 4692190
        self.responses_add('DELETE', id=inst_id)
        response = self.toggl.Projects.delete(inst_id)
        self.assertTrue(response)
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
            sub_uri='/project_users'
        )
        response = self.toggl.Projects.get_project_users(inst_id)
        self.assertTrue(response)
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_tasks_get(self):
        """ Should get Tasks under the Project. """
        inst_id = 777
        self.responses_add(
            'GET',
            filename='project_tasks_get',
            id=inst_id,
            sub_uri='/tasks'
        )
        response = self.toggl.Projects.get_tasks(inst_id)
        self.assertTrue(response)
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
        self.assertTrue(response)
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
        self.assertTrue(response)
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_delete(self):
        """ Should delete a ProjectUser. """
        inst_id = 4692190
        self.responses_add('DELETE', id=inst_id)
        response = self.toggl.ProjectUsers.delete(inst_id)
        self.assertTrue(response)
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


class TestUser(TestTogglBase):
    focus_class = api.User

    @responses.activate
    def test_get(self):
        """ Should successfully get the User associated with the token. """
        self.responses_add('GET', filename='user_get')
        response = self.toggl.User.get()
        self.assertTrue(response)
        self.assertEqual(len(responses.calls), 1)


if __name__ == '__main__' and __package__ is None:
    __package__ = "toggl"
    unittest.main()
