import json
import logging
import requests

from . import errors


class Api:
    """ Class for handling github API calls  """

    def __init__(self, token):
        self.token = token
        self.set_session(token)
        self.base_url = 'https://api.github.com'
        self.logger = logging.getLogger("Glabel")

    def setup_session(self, token):
        """ Gets headers
        :param token: GitHub personal access token
        """
        self.session = requests.Session()
        self.session.headers['Authorization'] = 'token ' + token
        self.session.headers = {'User-Agent': 'Python'}
        self.session.headers['Content-Type'] = 'application/vnd.github.v3+json'

    def execute(self, method, endpoints, data=None):
        response = requests.Response()
        if method == 'get':
            response = self.session.get(self.base_url + endpoints)
        elif method == 'post':
            if data is not None:
                response = self.session.post(self.base_url + endpoints, data)
        else:
            self.logger.exception("Glabel api call internal exception")

        response.raise_for_status()
        return json.loads(response.text)
