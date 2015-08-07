import json
import unittest

from mock import patch
from requests.exceptions import HTTPError

import api


class TestAPIMethods(unittest.TestCase):
    def setUp(self):
        with open('json/user_get.json') as json_data:
            self.data = json.load(json_data)
            json_data.close()

    def test_client(self):
        """ Should successfully establish the client. """
        api_token = 'fake_token_1'
        toggl = api.Client(api_token)
        with patch.object(toggl, 'User') as MockedUser:
            MockedUser.get.return_value = self.data
            response = toggl.User.get()
            self.assertTrue(response)

    def test_client_wrong_token(self):
        """ Should raise exception when wrong API token is provided. """
        wrong_api_token = 'wrong token'
        toggl = api.Client(wrong_api_token)
        self.assertRaises(HTTPError, toggl.User.get)


if __name__ == '__main__':
    unittest.main()
