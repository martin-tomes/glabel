import json
import logging
import requests
import asyncio
import aiohttp
import configparser
import fnmatch
# from .api import Api


def parse_config(file, section):
    # TODO: create one config parser. do not instantiate it again!!
    parser = configparser.ConfigParser()
    parser.read(file)
    parsed = {}

    for key in list(parser[section].keys()):
        strings = parser[section][key]
        parsed[key] = strings.split('\n')
    return parsed


def setup_session(token):
    """ Gets headers
        :param token: GitHub personal access token
    """
    connector = aiohttp.TCPConnector(verify_ssl=False)
    headers = {'Authorization': F'token {token}'}
    return aiohttp.ClientSession(headers=headers, connector=connector)


class Glabel:
    def __init__(self, token, config, reposlugs, delete_all):
        connector = aiohttp.TCPConnector(ssl=False)
        headers = {'Authorization': F'token {token}'}
        self.session = aiohttp.ClientSession(
            headers=headers, connector=connector)
        self.base_url = 'https://api.github.com'
        self.reposlugs = reposlugs
        self.token = token
        self.configs = parse_config(config, 'labels')
        self.delete_all = delete_all

    async def execute_request(self, method, endpoints, params=None):
        ''' Perform HTTP requests to the API '''
        async with setup_session(self.token) as s:
            async with s.request(method, self.base_url + endpoints, json=params) as response:
                data = await response.text()
                response.raise_for_status()
                if response.status == 200:
                    return json.loads(data)

    async def run(self):
        tasks = []
        for slug in self.reposlugs:
            owner = slug.split('/')[0]
            repo = slug.split('/')[1]
            tasks.append(self.scan_repo(owner, repo))
        await asyncio.wait(tasks)

    async def scan_repo(self, owner, repo):
        print("Scanning {}".format(repo))
        pr_numbers = await self.get_pr_numbers(owner, repo)
        print(pr_numbers)

        for pull_number in pr_numbers:

            if self.delete_all:
                await self.delete_all_labels(owner, repo, pull_number)
            else:

                files = await self.get_pull_files(owner, repo, pull_number)
                labels = self.find_labels(files)
                await self.update_labels(owner, repo, pull_number, labels)

                print("Labels added: {}".format(labels))
                print("Finished {}".format(repo))

    async def get_pr_numbers(self, owner, repo):
        pulls = await self.get_pull_requests(owner, repo)
        return [pull['number'] for pull in pulls]

    async def get_pull_requests(self, owner, repo):
        ''' GET /repos/:owner/:repo/pulls '''
        endpoints = '/repos/{}/{}/pulls'.format(owner, repo)
        return await self.execute_request('get', endpoints)

    async def get_pull_files(self, owner, repo, pull_number):
        ''' GET /repos/:owner/:repo/pulls/:pull_number/files '''
        endpoints = '/repos/{}/{}/pulls/{}/files'.format(
            owner, repo, pull_number)
        return await self.execute_request('get', endpoints)

    def find_labels(self, files):
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

    async def update_labels(self, owner, repo, pull_number, labels):
        ''' POST /repos/:owner/:repo/issues/:issue_number/labels '''
        endpoints = '/repos/{}/{}/issues/{}'.format(owner, repo, pull_number)
        await self.execute_request('patch', endpoints, {'labels': labels})

    async def delete_all_labels(self, owner, repo, pull_number):
        '''DELETE /repos/:owner/:repo/issues/:issue_number/labels
            Deletes all labels in a given repository
        '''
        endpoints = '/repos/{}/{}/issues/{}/labels'.format(
            owner, repo, pull_number)
        response = await self.execute_request('delete', endpoints)
        print(response)

    def create_labels(self, labels):
        ''' We need to create a string object
            so that we can replace quotation marks to desired format
        '''
        labels = str(labels)
        labels = labels.replace('\'', '"')
        return '{"labels": ' + labels + '}'

    async def close(self):
        await self.session.close()

