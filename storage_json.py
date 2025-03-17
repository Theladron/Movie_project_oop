from istorage import IStorage
import json

class StorageJson(IStorage):

    def __init__(self, file_path):
        self._file_path = file_path

    def list_movies(self):
        """
        prints a list of all the movies in the JSON file,
        with year and rating
        """
        with open(self._file_path, "r") as handle:
            return json.loads(handle.read())


    def add_movie(self, title, year, rating):
        """
        takes user input for a new movie, year and rating,
        calls for saving the input to the JSON File
        """
        with open(self._file_path, "r") as handle:
            movies = json.loads(handle.read())
        movies[title] = {"year": year, "rating": rating}
        with open(self._file_path, "w") as handle:
            handle.write(json.dumps(movies, indent=4))

    def delete_movie(self, title):
        """
        takes user input for an existing movie,
        calls for saving the changes in the JSON File
        """
        movies = self.list_movies()
        del movies[title]
        with open (self._file_path, "w") as handle:
            handle.write(json.dumps(movies, indent=4))


    def update_movie(self, title, rating):
        """
        takes user input for an existing movie and new rating,
        calls for saving the input to the JSON File
        """
        movies = self.list_movies()
        movies[title]["rating"] = rating
        with open(self._file_path, "w") as handle:
            handle.write(json.dumps(movies, indent=4))


storage = StorageJson('data.json')
print(storage.list_movies())