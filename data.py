import tmdbsimple as tmdb


class Data:
    def __int__(self, key):
        tmdb.API_KEY = '695405dd49c500e659c471af7f59c9b5'

    def search(self):
        m=tmdb.search(query='The matrix')
        res=m.info()