import fnmatch
import configparser


def parse_config(file, section):
    parser = configparser.ConfigParser()
    parser.read(file)
    parsed = {}

    for key in list(parser[section].keys()):
        strings = parser[section][key]
        parsed[key] = strings.split('\n')

    # print(parsed)
    return parsed


class Glabel:
    ''' Class for running the github labeler logic '''

    def __init__(self, api, config, reposlugs):
        ''' Class constructor initializes a session and last ID'''
        self.reposlugs = reposlugs
        self.api = api
        self.configs = parse_config(config, 'labels')

        # for section in self.configs.values():
            # print(section)
            # match = [v for v in section if fnmatch.fnmatch('templates', v)]
            # print(match)


    def handle_slugs(self, slugs):
        owner = slugs[0]
        repo = slugs[1]

        return '/' + owner, '/' + repo


    def read(self):
        owner, repo = self.handle_slugs(self.reposlugs)
        pull_number = self.api.get_pull_number(owner, repo)
        response = self.api.get_pull_files(owner, repo, pull_number)
        self.handle_response(response)


    def handle_response(self, response):
        print(response)
        for section in response:
            if section['status'] == 'modified':
                filename = section['filename']
                label = filename.split('/')[0]

                for key, value in self.configs.items():
                    if self.is_match(value, label):
                        print(key)


    def is_match(self, value, label):
        for item in value:
            if fnmatch.fnmatch(label, item):
                return True
        return False


