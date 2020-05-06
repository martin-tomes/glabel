import json
import logging
import requests
import asyncio
import aiohttp
import configparser
import fnmatch
from .api import Api


def parse_config(conf, section):
    # TODO: create one config parser. do not instantiate it again!!
    parser = configparser.ConfigParser()
    parser.read(conf)
    parsed = {}

    for key in list(parser[section].keys()):
        strings = parser[section][key]
        parsed[key] = strings.split('\n')
    return parsed


class Glabel:
    def __init__(self, token, config, reposlugs, delete_all, state, base):
        self.api = Api(token)
        self.reposlugs = reposlugs
        self.configs = parse_config(config, 'labels')
        self.delete_all = delete_all
        self.state = state 
        self.base = base

    async def run(self):
        tasks = []
        for slug in self.reposlugs:
            owner = slug.split('/')[0]
            repo = slug.split('/')[1]
            tasks.append(self.scan_repo(owner, repo))
        await asyncio.wait(tasks)

    async def scan_repo(self, owner, repo):
        print("Scanning {}".format(repo))
        pulls = await self.api.get_pull_requests(owner, repo, self.state, self.base)
        pr_numbers = [pull['number'] for pull in pulls] 
        for number in pr_numbers:
            await self.handle_pull_request(owner, repo, number)

    async def handle_pull_request(self, owner, repo, pull_number):
        if self.delete_all:
            if await self.api.delete_all_labels(owner, repo, pull_number) == 204:
                print(F"All labels removed from {repo} PR: {pull_number}")
        else:
            files = await self.api.get_pull_files(owner, repo, pull_number)
            labels = self.find_labels(files)
            response = await self.api.update_labels(owner, repo, pull_number, labels)
            updated_labels = ([label['name'] for label in response['labels']])
            print(F"Labels added: {updated_labels} for repo: {repo} pull: {pull_number}")

    # def evaluate_response(self, response):
    #     return [item['name'] for item in response]


    def find_labels(self, files):
        statuses = ('added', 'modified')
        labels = []
        for section in files:
            if any(status in section['status'] for status in statuses):
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

    def create_labels(self, labels):
        ''' We need to create a string object
            so that we can replace quotation marks to desired format
        '''
        labels = str(labels)
        labels = labels.replace('\'', '"')
        return '{"labels": ' + labels + '}'

    # async def close(self):
    #     await self.session.close()

