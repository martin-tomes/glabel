import requests
import base64
import time

OWNER = '/tomesm'
BASE_URL = 'https://api.github.com'
REPOS = '/repos'

class Glabel:
    ''' Class for running the github labeler logic '''

    def __init__(self, token, reposlugs, session=None):
        ''' Class constructor initializes a session and last ID'''
        self.session = session or requests.Session()
        self.set_session(token)
        self.reposlugs = reposlugs

    def set_session(self, token):
        """ Gets headers
        :param token: GitHub personal access token
        """
        self.session.headers = {'User-Agent': 'Python'}
        self.session.headers['Authorization'] = 'token' + token

    def read(self):
        owner, repo = self.handle_slug(self.reposlugs[0])

        url = BASE_URL + REPOS + owner + repo + '/pulls'
        response = self.session.get(url)
        response.raise_for_status()
        print(response.json())

    def handle_slug(self, slug):
        owner = slug.split('/')[0]
        repo = slug.split('/')[1]
        return '/' + owner, '/' + repo


