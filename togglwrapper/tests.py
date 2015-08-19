import json
import unittest

from mock import patch

import api
from errors import AuthError


class TestAPIMethods(unittest.TestCase):

    def setUp(self):
        self.api_token = 'fake_token_1'
        self.toggl = api.Toggl(self.api_token)

    def _get_json(self, filename):
        """ Return the JSON data contained in the given filename. """
        with open('json/{}.json'.format(filename)) as json_file:
            json_data = json.load(json_file)
            json_file.close()
        return json_data

    def test_client(self):
        """ Should successfully establish the client. """
        # TODO: patch futher upstream - in requests, probably.
        with patch.object(self.toggl, 'User') as MockedUser:
            MockedUser.get.return_value = self._get_json('user_get')
            response = self.toggl.User.get()
        self.assertTrue(response)
        self.assertEqual(response['data']['api_token'], self.api_token)

    def test_client_wrong_token(self):
        """ Should raise exception when wrong API token is provided. """
        self.assertRaises(AuthError, self.toggl.User.get)

    def test_client_create(self):
        """ Should create a new Client. """
        with patch.object(self.toggl, 'Clients') as MockedClients:
            MockedClients.create.return_value = self._get_json('client_create')
            response = self.toggl.Clients.create()
        self.assertTrue(response)

    def test_client_get(self):
        """ Should get a specific Client by ID. """
        with patch.object(self.toggl, 'Clients') as MockedClients:
            MockedClients.get.return_value = self._get_json('client_get')
            response = self.toggl.Clients.get()
        self.assertTrue(response)


if __name__ == '__main__':
    unittest.main()
