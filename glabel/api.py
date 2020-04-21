import requests
import json
import logging

from . import errors

class Api:
    """ Class for handling github API calls  """

    def __init__(self, token, owner):
        self.token = token
        self.set_session(token, owner)
        self.base_url = 'https://api.github.com'
        self.logger = logging.getLogger("Glabel")

    def set_session(self, token, owner):
        """ Gets headers
        :param token: GitHub personal access token
        """
        self.session = requests.Session()
        self.session.auth = (owner, token)
        self.session.headers = {'User-Agent': 'Python'}
        self.session.headers['Content-Type'] = 'application/vnd.github.v3+json'

    def execute(self, method, endpoints, data=None):
        resonse = requests.Response()
        if method == 'get':
            response = self.session.get(self.base_url + endpoints)
        elif method == 'post':
            if data is not None:
                response = self.session.post(self.base_url + endpoints, data)
        else:
            self.logger.exception("Glabel api call internal exception")

        response.raise_for_status()
        return json.loads(response.text)



