import json

import requests
from requests.auth import HTTPBasicAuth


BASE_URL = 'https://www.toggl.com/api/'
API_VERSION = 'v8'
API_URL = BASE_URL + API_VERSION
API_TOKEN = ''

auth = HTTPBasicAuth(API_TOKEN, 'api_token')


class User(object):
    pass
