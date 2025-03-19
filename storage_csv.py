from istorage import IStorage
import json

class StorageCsv(IStorage):

    def __init__(self, file_path):
        self._file_path = file_path

    def list_movies(self):
        """
        prints a list of all the movies in the JSON file,
        with year and rating
        """
        try:
            with open(self._file_path, "r") as handle:
                cvs_data = handle.readlines()
        except FileNotFoundError:
            with open(self._file_path, "w") as handle:
                handle.write("title,year,rating,poster\n")
            return {}
        if len(cvs_data) == 1:
            return {}
        data = {}
        for line in cvs_data[1:]:
            data_elements = line.split(",")
            data[data_elements[0]] = {
                                        "year" : int(data_elements[1]),
                                        "rating" : float(data_elements[2]),
                                        "poster" : data_elements[3][:-1]
                                        }
        return data


    def add_movie(self, title, year, rating, poster):
        """
        takes user input for a new movie, year and rating,
        calls for saving the input to the JSON File
        """
        with open(self._file_path, "r") as handle:
            movies = handle.read()

        movies += f"{title},{year},{rating},{poster}\n"

        with open(self._file_path, "w") as handle:
            handle.write(movies)

    def delete_movie(self, title):
        """
        takes user input for an existing movie,
        calls for saving the changes in the JSON File
        """
        with open(self._file_path, "r") as handle:
            movies = handle.readlines()
        new_movies = ""
        for line in movies:
            movie_elements = line.split(",")
            if title.lower() != movie_elements[0].lower():
                new_movies += line
        with open(self._file_path, "w") as handle:
            handle.write(new_movies)


    def update_movie(self, title, rating):
        """
        takes user input for an existing movie and new rating,
        calls for saving the input to the JSON File
        """
        with open(self._file_path, "r") as handle:
            movies = handle.readlines()
        new_movies = ""
        for line in movies:
            movie_elements = line.split(",")
            if title.lower() == movie_elements[0].lower():
                line = line.replace(movie_elements[2], str(rating)+"\n")
            new_movies += line
        with open(self._file_path, "w") as handle:
            handle.write(new_movies)
