import json

import requests
import requests_cache

requests_cache.install_cache()


class Network:
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'Connection': 'close'}

    BASE_PATH = 'https://api.themoviedb.org/3/'

    details = []

    # URLS = {
    #     'movie': '/movie',
    #     'collection': '/collection',
    #     'tv': '/tv',
    #     'person': '/person',
    #     'company': '/company',
    #     'keyword': '/keyword',
    #     'multi': '/multi'
    # }

    def __init__(self):
        self.API_KEY = '695405dd49c500e659c471af7f59c9b5'
        self.results = dict()

    def search_movie(self, name):
        base_path = self.BASE_PATH + "search/movie?"

        payload = {
            'api_key': self.API_KEY,
            'language': ' en-US',
            'page': '1',
            'include_adult': 'false',
            'query': name
        }

        movie = self.request(base_path, payload)
        movie = movie['results'][0]
        # print(json.dumps(movie, indent=4))
        print("----------Movie Search-----------")
        print(movie['id'], movie['title'])

        # Get movie details
        info = self.movie_details(movie['id'])
        return info


    def request(self, base_path, payload):
        response = requests.get(base_path, headers=self.headers, params=payload)
        print(response.status_code)
        return response.json()

    def credits(self, credits):
        cast = dict()
        for actor in credits['cast']:
            cast[actor['name']] = [actor['name'], actor['id']]

        director = []
        for crew in credits['crew']:
            if crew['job'] == 'Director':
                director.append(crew['name'])

        temp = dict()
        temp['cast'] = cast
        temp['director'] = director
        # print(json.dumps(temp, indent=4))
        return temp

    def movie_details(self, id):
        base_path = self.BASE_PATH + "movie/" + str(id) + "?"

        payload = {
            'api_key': self.API_KEY,
            'language': 'en-US',
            'append_to_response': 'credits'
        }

        print("\n------Movie Details-------------")
        data = self.request(base_path, payload)

        # print(json.dumps(data, indent=4))

        #   Remove the attributes from the json
        lst = ["backdrop_path", "budget", "genres", "id", "imdb_id", "overview", "popularity", "poster_path",
               "production_companies", "production_countries", "release_date", "revenue", "runtime", "tagline", "title",
               "vote_average", "credits"]

        # Get ony essential info
        info = dict()
        for item in lst:
            info[item] = data[item]
        credits = self.credits(info['credits'])

        return info

class


a = Network()
# a.search_movie('The matrix')
info = a.movie_details(603)
