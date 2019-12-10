import requests

class API:
    """ Class for handling github API calls  """

    def __init__(self, token):
        self.token = token
        self.set_session(token)
        self.base_url = 'https://api.github.com/repos'

    def set_session(self, token):
        """ Gets headers
        :param token: GitHub personal access token
        """
        self.session = requests.Session()
        self.session.headers = {'User-Agent': 'Python'}
        self.session.headers['Authorization'] = 'token' + token

    def get_pull_number(self, owner, repo):
        url = self.base_url + owner + repo + '/pulls'
        response = self.session.get(url)
        response.raise_for_status()
        return str(response.json()[0]['number'])

    def get_pull_files(self, owner, repo, pull_number):
        url = self.base_url + owner + repo + '/pulls/' + pull_number + '/files'
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def post_labels(self, owner, repo, number, labels):
        ''' POST /repos/:owner/:repo/issues/:issue_number/labels '''
        url = self.base_url + owner + repo + '/issues/' + number + '/' + labels
