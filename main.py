import json

import requests
import requests_cache

requests_cache.install_cache()


class Network:
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'Connection': 'close'}
    BASE_PATH = 'https://api.themoviedb.org//3'
    URLS = {
        'movie': '/movie',
        'collection': '/collection',
        'tv': '/tv',
        'person': '/person',
        'company': '/company',
        'keyword': '/keyword',
        'multi': '/multi'
    }

    def __init__(self):
        self.API_KEY = '695405dd49c500e659c471af7f59c9b5'
        # self.USER_AGENT = 'Dataquest'

        self.base_uri = 'https://api.themoviedb.org//3'

        # self.headers = {
        #     'user-agent': self.USER_AGENT
        # }
        self.url = "https://api.themoviedb.org/3/search/movie?query="

    def search_movie(self, name):
        self.BASE_PATH += 'search//movie'

        payload = {
            'api_key': self.API_KEY,
            'language': ' en - US',
            'page': '1',
            'include_adult': 'false',
            'query': name
        }

        response = requests.get(self.url, headers=self.headers, params=payload)
        print(response.status_code)
        print(json.dumps(response.json(), indent=4))


a = Network()
a.search_movie('The matrix')
