import fnmatch

class Glabel:
    ''' Class for running the github labeler logic '''

    def __init__(self, api, reposlugs):
        ''' Class constructor initializes a session and last ID'''
        self.reposlugs = reposlugs
        self.api = api

    def handle_slug(self, slug):
        owner = slug.split('/')[0]
        repo = slug.split('/')[1]
        return '/' + owner, '/' + repo


    def read(self):
        owner, repo = self.handle_slug(self.reposlugs[0])
        pull_number = self.api.get_pull_number(owner, repo)
        files = self.api.get_pull_files(owner, repo, pull_number)
        print(files[0]['status'])

        if files[0]['status'] == 'modified':
            filename = files[0]['filename']
            label = filename.split('/')[0]
            if fnmatch.fnmatch(label, '*/templates/*'):
                print(label)

