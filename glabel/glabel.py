import fnmatch
import configparser

def get_keys(file, section):
    parser = configparser.ConfigParser()
    parser.read(file)
    return list(parser[section].keys())


def set_parser(file, section):
    parser = configparser.ConfigParser()
    parser.read(file)

    d = {}

    for key in list(parser[section].keys()):
        confs = []

        for str in parser[section][key]:
            confs.append(str)

        d[key] = confs

    return d


class Glabel:
    ''' Class for running the github labeler logic '''

    def __init__(self, api, config, reposlugs):
        ''' Class constructor initializes a session and last ID'''
        self.reposlugs = reposlugs
        self.api = api
        self.keys = get_keys(config, 'labels')
        self.values = set_parser(config, 'labels')

        print(self.values)

    def handle_slugs(self, slugs):
        owner = slugs[0]
        repo = slugs[1]
        return '/' + owner, '/' + repo


    def read(self):
        owner, repo = self.handle_slugs(self.reposlugs)
        pull_number = self.api.get_pull_number(owner, repo)
        files = self.api.get_pull_files(owner, repo, pull_number)
        # print(files[0]['status'])

        if files[0]['status'] == 'modified':
            filename = files[0]['filename']

            label = filename.split('/')[0]

            if fnmatch.fnmatch(label, '*templates*'):
                print(label)

