import unittest

import api


class TestAPIMethods(unittest.TestCase):
    def test_client(self):
        """ Should successfully establish the client. """
        api_token = 'correct_token'
        self.assertTrue(api.Client(api_token))

    def test_client_wrong_token(self):
        """ Should raise exception when wrong API token is provided. """
        wrong_api_token = 'wrong token'
        self.assertRaises(Exception, api.Client, wrong_api_token)


if __name__ == '__main__':
    unittest.main()
