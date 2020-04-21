import fnmatch
import configparser

from .api import Api


def parse_config(file, section):
    # TODO: create one config parser. do not instantiate it again!!
    parser = configparser.ConfigParser()
    parser.read(file)
    parsed = {}

    for key in list(parser[section].keys()):
        strings = parser[section][key]
        parsed[key] = strings.split('\n')
    return parsed


class Glabel:
    ''' Class for running the github labeler logic '''

    def __init__(self, token, config, reposlugs):
        ''' Class constructor initializes a session and last ID'''
        self.owner = reposlugs[0]
        self.api = Api(token, self.owner)
        self.repos = reposlugs[1:]
        self.configs = parse_config(config, 'labels')
        self.issue_number = ""


    def get_repos(self):
        return self.api.execute('get', '/user' + '/repos')


    def get_pull_requests(self, repo):
        ''' GET /repos/:owner/:repo/pulls '''
        endpoints = '/repos/{}/{}/pulls'.format(self.owner, repo)
        return self.api.execute('get', endpoints)


    def set_issue_number(self, repo):
        pulls = self.get_pull_requests(repo)
        # TODO enable handling of multiple pull requests
        self.issue_number = str(pulls[0]['number'])


    def get_pull_files(self, repo, pull_number):
        ''' GET /repos/:owner/:repo/pulls/:pull_number/files '''
        endpoints = '/repos/{}/{}/pulls/{}/files'.format(self.owner, repo, pull_number)
        return self.api.execute('get', endpoints)


    def read_repo(self):
        self.set_issue_number(self.repos[0])
        files = self.get_pull_files(self.repos[0], self.issue_number)
        return self.check_files(files)


    def check_files(self, files):
        labels = []
        for section in files:
            if any(status in section['status'] for status in ('added', 'modified')):
                filename = section['filename']
                label = self.find_label(filename)
                if label not in labels:
                    labels.append(label)
        return labels


    def find_label(self, filename):
        for key, value in self.configs.items():
            if self.is_match(value, filename):
                return key


    def is_match(self, value, label):
        for item in value:
            if fnmatch.fnmatch(label, item):
                return True
        return False


    def post_labels(self):
        ''' POST /repos/:owner/:repo/issues/:issue_number/labels '''
        # We need to create a string object so that we can replace quotation marks to desired format
        labels = str(self.read_repo())
        labels = labels.replace('\'', '"')
        body = '{"labels": ' + labels + '}'
        endpoints= '/repos' + self.owner + '/' + self.repos[0] + '/issues' + self.issue_number
        self.api.execute('post', endpoints, body)
        print("Labels added")


    def get_labels():
        ''' GET /repos/:owner/:repo/issues/:issue_number/labels '''
        # Check if the repo has already some labels


