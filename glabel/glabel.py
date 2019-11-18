import fnmatch
import configparser

def get_keys(file, section):
    parser = configparser.ConfigParser()
    parser.read(file)
    return list(parser[section].keys())


def parse_config(file, section):
    parser = configparser.ConfigParser()
    parser.read(file)

    parsed = {}

    for key in list(parser[section].keys()):
        strings = parser[section][key]
        parsed[key] = strings.split('\n')

    return parsed


class Glabel:
    ''' Class for running the github labeler logic '''

    def __init__(self, api, config, reposlugs):
        ''' Class constructor initializes a session and last ID'''
        self.reposlugs = reposlugs
        self.api = api
        self.configs = parse_config(config, 'labels')
        # print(self.values)
        for section in self.configs.values():
            print(section)
            match = [v for v in section if fnmatch.fnmatch('templates', v)]

            print(match)




    def handle_slugs(self, slugs):
        print(slugs)
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

            for value in self.configs.values():
                print(value)
                # if fnmatch.fnmatch(label, '*templates*'):
                    # print(label)

