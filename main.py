import json
import os
import re

import requests
import requests_cache

requests_cache.install_cache()


class Network:
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'Connection': 'close'}
    BASE_PATH = 'https://api.themoviedb.org/3/'
    database = dict()

    def __init__(self, dir):
        self.API_KEY = '695405dd49c500e659c471af7f59c9b5'
        self.dir = dir

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
        i = 0
        for actor in credits['cast']:
            i += 1
            if (i == 5): break
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
        del info['credits']
        info.update(credits)


        return info

    def get_image(self, path, name):
        base_url = 'https://image.tmdb.org/t/p/w92'+path
        r = requests.get(base_url)
        with open('./media/poster/'+path, 'wb') as f:
            f.write(r.content)

    def files(self):
        file_types = [".avi", ".mp4", ".mkv", ".mpeg", ".m4v"]
        lst = []

        for root, dirs, files in os.walk(self.dir):
            for file in files:
                name, ext = os.path.splitext(file)
                if ext in file_types:
                    path = os.path.join(root, file)
                    if os.path.getsize(path) / (1024 * 1024) > 300:
                        lst.append(path)
        return lst

    def start(self):
        files_list = self.files()

        try:
            with open('database.json') as fp:
                db = json.load(fp)

            for filename, values in db.copy().items():
                if values['location'] not in files_list:
                    del db[filename]
                else:
                    files_list.remove(values['location'])

            print(json.dumps(db, indent=2))
            print(files_list)
            self.database = db

        except:
            pass

        for filename in files_list:
            name = re.match(r'^.*\\(.*?)\s+\(.*?$', filename).group(1)
            print(name)
            info = self.search_movie(name)

            # Get poster for the movie
            self.get_image(info["poster_path"], name)
            info['location'] = filename

            self.database[name] = info

        with open('database.json', 'w') as fp:
            json.dump(self.database, fp, indent=2)


a = Network("A:\!Movie")
a.start()
# a.search_movie('The matrix')
# info = a.movie_details(603)
