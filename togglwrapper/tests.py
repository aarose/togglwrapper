import json
import unittest

from mock import patch
from requests.exceptions import HTTPError

import api


class TestAPIMethods(unittest.TestCase):

    def setUp(self):
        self.api_token = 'fake_token_1'

    def test_client(self):
        """ Should successfully establish the client. """
        # Grab the JSON response to return
        with open('json/user_get.json') as json_data:
            data = json.load(json_data)
            json_data.close()
        toggl = api.Client(self.api_token)
        with patch.object(toggl, 'User') as MockedUser:
            MockedUser.get.return_value = data
            response = toggl.User.get()
            self.assertTrue(response)
            self.assertEqual(response['data']['api_token'], self.api_token)

    def test_client_wrong_token(self):
        """ Should raise exception when wrong API token is provided. """
        toggl = api.Client(self.api_token)
        self.assertRaises(HTTPError, toggl.User.get)
        # Check that the error is a 403 error

    def test_update_user(self):
        """ Should change a property of the User. """

    def test_update_user_incorrect(self):
        """ Should raise a 404 error. """


if __name__ == '__main__':
    unittest.main()
