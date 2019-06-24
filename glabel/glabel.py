import requests
import base64
import time

OWNER = '/tomesm'
BASE_URL = 'https://api.github.com'
REPOS = '/repos'
REPO = '/labely-test'


class Glabel:
    ''' Class for running the github labeler logic '''

    def __init__(self, token, session=None):
        ''' Class constructor initializes a session and last ID'''
        # self.page = requests.get('https://api.github.com/repos/tomesm/labely-test/pulls/1/files', headers = self.headers(token))
        self.session = session or requests.Session()
        self.set_session(token)

    def set_session(self, token):
        """ Gets headers
        :param token: GitHub personal access token
        """
        self.session.headers = {'User-Agent': 'Python'}
        self.session.headers['Authorization'] = 'token' + token

    def read(self):
        url = BASE_URL + REPOS + OWNER + REPO + '/pulls'
        response = self.session.get(url)
        response.raise_for_status()
        print(response.json())

