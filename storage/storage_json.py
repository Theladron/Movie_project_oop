from json import JSONDecodeError

from storage.istorage import IStorage
import json


class StorageJson(IStorage):
    """Represents a json data storage"""

    def __init__(self, file_path):
        """
        Initializes the StorageJson class instance with its filepath
        :param file_path: name of the filepath the data is saved in as string
        """
        self._file_path = file_path

    def list_movies(self):
        """
        reads it's json database
        :return: json file as dictionary
        """
        try:
            with open(self._file_path, "r", encoding="utf-8") as handle:
                return json.loads(handle.read())
        except FileNotFoundError:
            return {}
        except JSONDecodeError:
            self.save_file("{}")
            with open(self._file_path, "r", encoding="utf-8") as handle:
                return json.loads(handle.read())

    def add_movie(self, title, year, rating, poster, url, flag):
        """
        Writes a new movie entry with the different attributes, calls for saving it to
        the database
        :param title: movie name as string
        :param year: year of release as integer
        :param rating: movie rating as float
        :param poster: movie cover link as string
        :param url: link-ending to access the entry on the imdb website as string
        :param flag: link to the countries of origins flags or backup flag file path as string
        """
        movies = self.list_movies()
        movies[title] = {
            "year": year,
            "rating": rating,
            "poster": poster,
            "imdb-url": url,
            "flag": flag,
            "comment": ""
        }
        self.save_file(movies)

    def delete_movie(self, title):
        """
        Gets the dictionary of movies, deletes an entry and calls for saving the change to the
        database
        :param title: movie name as string
        """
        movies = self.list_movies()
        del movies[title]
        self.save_file(movies)

    def update_movie(self, title, comment):
        """
        Adds a comment to a movie, calls for saving the change to the database
        :param title: movie name as string
        :param comment: comment to add to the movie as string
        """
        movies = self.list_movies()
        movies[title]["comment"] = comment
        self.save_file(movies)

    def save_file(self, movies):
        """Writes the movie dictionary in the database"""
        with open(self._file_path, "w") as handle:
            handle.write(json.dumps(movies, indent=4))
