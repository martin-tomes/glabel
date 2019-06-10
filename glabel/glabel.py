import requests
import base64
import time


class Glabel:
    ''' Class for running the github labeler logic '''

    def __init__(self, token, session=None):
        ''' Class constructor initializes a session and last ID'''
        self.page = requests.get('https://api.github.com/repos/tomesm/labely-test/pulls/1/files', headers = self.headers(token))

    def headers(self, token):
        """ Gets headers
        :param token: GitHub personal access token
        :return: HTTP headers for github request
        """
        return {'Authorization': 'token' + token}

    def read(self):
        self.page.raise_for_status()
        print(self.page.text)

