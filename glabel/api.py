import asyncio
import aiohttp
import json


def setup_session(token):
    """ Sets up auiohttp session
        :param token: GitHub personal access token
    """
    connector = aiohttp.TCPConnector(verify_ssl=False)
    headers = {'Authorization': F'token {token}'}
    return aiohttp.ClientSession(headers=headers, connector=connector)

class Api:
    ''' This class executes all REST API calls to the githb'''

    def __init__(self, token):
        self.token = token

    async def execute_request(self, method, endpoints, params=None, data=None):
        ''' Executes HTTP requests to the API '''
        async with setup_session(self.token) as s:
            url = 'https://api.github.com' + endpoints
            async with s.request(method, url, params=params, json=data) as r:
                data = await r.text()
                r.raise_for_status()
                if r.status == 200:
                    return json.loads(data)
                else:
                    return r.status

    async def get_pull_requests(self, owner, repo, state):
        ''' GET /repos/:owner/:repo/pulls '''
        endpoints = F'/repos/{owner}/{repo}/pulls'
        return await self.execute_request('get', endpoints, params={'state': state})

    async def get_pull_files(self, owner, repo, pull_number):
        ''' GET /repos/:owner/:repo/pulls/:pull_number/files '''
        endpoints = F'/repos/{owner}/{repo}/pulls/{pull_number}/files'
        return await self.execute_request('get', endpoints)

    async def update_labels(self, owner, repo, pull_number, labels):
        ''' POST /repos/:owner/:repo/issues/:issue_number/labels '''
        endpoints = F'/repos/{owner}/{repo}/issues/{pull_number}'
        return await self.execute_request('patch', endpoints, data={'labels': labels})
        # return response

    async def delete_all_labels(self, owner, repo, pull_number):
        '''DELETE /repos/:owner/:repo/issues/:issue_number/labels
            Deletes all labels in a given repository
        '''
        endpoints = F'/repos/{owner}/{repo}/issues/{pull_number}/labels'
        response = await self.execute_request('delete', endpoints)
        print(response)