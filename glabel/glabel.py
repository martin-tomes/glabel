import requests
import base64
import time


class Glabel:
    ''' Class for running the github labeler logic '''

    def __init__(self, token, session=None):
        ''' Class constructor initializes a session and last ID'''
        page = requests.get('https://api.github.com/user', headers = headers(token))
        page.raise_for_status()
        print(page.text)

    def headers(self, token):
        """ Gets headers
        :param token: GitHub personal access token
        :return: HTTP headers for github request
        """
        return {'Authorization': 'token' + token}


