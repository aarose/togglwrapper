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

    @property
    def full_url(self):
        return self.toggl.api_url + self.focus_class.uri


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
        responses.add(
            responses.POST,
            self.full_url,
            body=self.get_json('client_create'),
            status=200,
            content_type='application/json'
        )

        new_client_data = {"client": {"name": "Very Big Company", "wid": 777}}
        response = self.toggl.Clients.create(new_client_data)
        self.assertTrue(response)
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_get_by_id(self):
        """ Should get a specific Client by ID. """
        inst_id = 1239455
        full_url = '{url}/{id}'.format(url=self.full_url, id=inst_id)
        responses.add(
            responses.GET,
            full_url,
            body=self.get_json('client_get'),
            status=200,
            content_type='application/json'
        )

        response = self.toggl.Clients.get(id=inst_id)
        self.assertTrue(response)
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_get(self):
        """ Should get all Clients. """
        responses.add(
            responses.GET,
            self.full_url,
            body=self.get_json('clients_get'),
            status=200,
            content_type='application/json'
        )

        response = self.toggl.Clients.get()
        self.assertTrue(response)
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_update(self):
        """ Should update a Client. """
        inst_id = 1239455
        full_url = '{url}/{id}'.format(url=self.full_url, id=inst_id)
        responses.add(
            responses.PUT,
            full_url,
            body=self.get_json('client_update'),
            status=200,
            content_type='application/json'
        )

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
        full_url = '{url}/{id}'.format(url=self.full_url, id=inst_id)
        responses.add(responses.DELETE, full_url, status=200)

        response = self.toggl.Clients.delete(inst_id)
        self.assertTrue(response)
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_projects_get(self):
        """ Should get all active projects under the Client. """
        inst_id = 1239455
        url = '{url}/{id}/projects'.format(url=self.full_url, id=inst_id)
        responses.add(
            responses.GET,
            url,
            body=self.get_json('client_projects_get'),
            status=200,
            content_type='application/json'
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
        full_url = '{url}/{id}'.format(url=self.full_url, id=inst_id)
        responses.add(
            responses.GET,
            full_url,
            body=self.get_json('dashboard'),
            status=200,
            content_type='application/json'
        )

        response = self.toggl.Dashboard.get(inst_id)
        self.assertTrue(response)
        self.assertEqual(len(responses.calls), 1)


class TestProjects(TestTogglBase):
    focus_class = api.Projects

    @responses.activate
    def test_create(self):
        """ Should create a new Project. """
        responses.add(
            responses.POST,
            self.full_url,
            body=self.get_json('project_create'),
            status=200,
            content_type='application/json'
        )

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
        full_url = '{url}/{id}'.format(url=self.full_url, id=inst_id)
        responses.add(
            responses.GET,
            full_url,
            body=self.get_json('project_get'),
            status=200,
            content_type='application/json'
        )

        response = self.toggl.Projects.get(inst_id)
        self.assertTrue(response)
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_update(self):
        """ Should update a Project. """
        inst_id = 193838628
        full_url = '{url}/{id}'.format(url=self.full_url, id=inst_id)
        responses.add(
            responses.PUT,
            full_url,
            body=self.get_json('project_update'),
            status=200,
            content_type='application/json'
        )

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
        full_url = '{url}/{id}'.format(url=self.full_url, id=inst_id)
        responses.add(responses.DELETE, full_url, status=200)

        response = self.toggl.Projects.delete(inst_id)
        self.assertTrue(response)
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_project_users_get(self):
        """ Should get Project Users under the Project. """
        inst_id = 193838628
        url = '{url}/{id}/project_users'.format(url=self.full_url, id=inst_id)
        responses.add(
            responses.GET,
            url,
            body=self.get_json('project_projectusers_get'),
            status=200,
            content_type='application/json'
        )

        response = self.toggl.Projects.get_project_users(inst_id)
        self.assertTrue(response)
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_tasks_get(self):
        """ Should get Tasks under the Project. """
        inst_id = 777
        url = '{url}/{id}/tasks'.format(url=self.full_url, id=inst_id)
        responses.add(
            responses.GET,
            url,
            body=self.get_json('project_tasks_get'),
            status=200,
            content_type='application/json'
        )

        response = self.toggl.Projects.get_tasks(inst_id)
        self.assertTrue(response)
        self.assertEqual(len(responses.calls), 1)


class TestUser(TestTogglBase):
    focus_class = api.User

    @responses.activate
    def test_get(self):
        """ Should successfully get the User associated with the token. """
        responses.add(
            responses.GET,
            self.full_url,
            body=self.get_json('user_get'),
            status=200,
            content_type='application/json'
        )

        response = self.toggl.User.get()

        self.assertTrue(response)
        self.assertEqual(len(responses.calls), 1)


if __name__ == '__main__' and __package__ is None:
    __package__ = "toggl"
    unittest.main()
