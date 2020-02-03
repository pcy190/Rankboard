import requests
import json

from util.config import *


class Gist:
    def __init__(self):
        self.user = USERNAME
        self.token = API_TOKEN
        self.gist_id = GIST_ID

    def auth(self):
        # login = requests.get('https://api.github.com/search/repositories?q=github+api', auth=(self.user, self.token))
        self.headers = {'Authorization': 'token ' + self.token}
        # print(login.json())
        # print("login success")

    def listgist(self):
        file_name = []
        print("list gist")
        r = self.gist = requests.get('https://api.github.com/gists', headers=self.headers)
        print(self.gist.json())
        r_text = json.loads(r.text)
        limit = len(r.json())
        if (r.status_code == 200):
            for g, no in zip(r_text, range(0, limit)):
                for key, value in r.json()[no]['files'].items():
                    file_name.append(value['filename'])
            print("200: gistall")
            print(file_name)
            return file_name

        raise Exception('Username not found')

    def list(self, offset):
        '''
        will display only the required no. of filenames but in order.
        Result can be stored in an array for easy fetching of gistNames
        for future purposes.
        eg. a = Gist().mygists().listall()
            print a[0] #to fetch first gistName
        '''
        file_name = []
        r = requests.get(
            '%s' % BASE_URL + '/gists',
            headers=self.headers
        )
        if (r.status_code == 200):
            r_text = json.loads(r.text)
            limit = offset if (offset <= len(r.json())) else len(r.json())

            for g, no in zip(r_text, range(0, limit)):
                for key, value in r.json()[no]['files'].items():
                    file_name.append(value['filename'])
            print("200:gist offset")
            print(file_name)
            return file_name

        raise Exception('Username not found')

    def getMyID(self, gist_name):
        '''
        Getting gistID of a gist in order to make the workflow
        easy and uninterrupted.
        '''
        r = requests.get(
            '%s' % BASE_URL + '/gists',
            headers=self.headers
        )
        if (r.status_code == 200):
            r_text = json.loads(r.text)
            limit = len(r.json())

            for g, no in zip(r_text, range(0, limit)):
                for ka, va in r.json()[no]['files'].items():
                    if str(va['filename']) == str(gist_name):
                        print("My id is ", r.json()[no]['id'])
                        return r.json()[no]['id']
        return 0

    def create(self, **args):
        if 'description' in args:
            self.description = args['description']
        else:
            self.description = ''

        if 'name' in args:
            self.gist_name = args['name']
        else:
            self.gist_name = ''

        if 'public' in args:
            self.public = args['public']
        else:
            self.public = 1

        if 'content' in args:
            self.content = args['content']
        else:
            raise Exception('Gist content can\'t be empty')

        url = '/gists'

        data = {"description": self.description,
                "public": self.public,
                "files": {
                    self.gist_name: {
                        "content": self.content
                    }
                }
                }

        r = requests.post(
            '%s%s' % (BASE_URL, url),
            data=json.dumps(data),
            headers=self.headers
        )
        if (r.status_code == 201):
            response = {
                'Gist-Link': '%s/%s/%s' % (GIST_URL, self.user, r.json()['id']),
                'Clone-Link': '%s/%s.git' % (GIST_URL, r.json()['id']),
                'Embed-Script': '<script src="%s/%s/%s.js"</script>' % (GIST_URL, self.user, r.json()['id']),
                'id': r.json()['id'],
                'created_at': r.json()['created_at'],

            }
            self.gist_id = r.json()['id']
            print("Create Gist successful!: ", r)
            return response

        raise Exception('Gist not created: server response was [%s] %s' % (r.status_code, r.text))

    def read_all(self) -> [str, str, str]:
        """
        Get gist filename, content, description
        :return: filename, content, description
        """
        d = self.read_json()
        json_content = list(d['files'].values())[0]
        description = d['description']
        return json_content['filename'], json_content['content'], description

    def read(self) -> str:
        """
        Get gist Content only
        :return: content
        """
        _, content, __ = self.read_all()
        return content

    def read_json(self) -> dict:
        r = requests.get(
            '%s' % BASE_URL + '/gists/' + '%s' % self.gist_id,
            headers=self.headers
        )
        if (r.status_code == 200):
            # print("Read Gist Successful!: ", r.content)
            return json.loads(r.content)
        else:
            raise Exception('gist id not found')

    def update(self, content, description=None, filename=None):
        """
        edit gist file. Note: if filename is None, won't change filename, so do description
        :param content:
        :param description:
        :param filename:
        :return:
        """
        _filename, _, _description = self.read_all()
        if description is None:
            description = _description
        if filename is None:
            filename = _filename
        assert filename is not None  # Keep safe. if filename is null, the api will delete the file. Not necessary

        updated_data = {
            "description": description,
            "files": {
                str(filename): {
                    "content": str(content),
                    "filename": str(filename)
                }
            }
        }

        r = requests.patch(
            '%s' % BASE_URL + '/gists/' + '%s' % self.gist_id,
            headers=self.headers,
            data=json.dumps(updated_data)
        )
        if (r.status_code == 200):
            print("Update Gist Successful!: ", r)

        else:
            raise Exception('gist id not found')

    def delete(self):

        r = requests.delete(
            '%s' % BASE_URL + '/gists/' + '%s' % self.gist_id,
            headers=self.headers
        )
        if (r.status_code == 204):
            print("Delete Gist Successful!: ", r)

        else:
            raise Exception('gist id not found')
