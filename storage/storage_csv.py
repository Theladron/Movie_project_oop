from storage.istorage import IStorage


class StorageCsv(IStorage):
    """Represents a csv data storage"""

    def __init__(self, file_path):
        """
        Initializes the StorageCsv class instance with its filepath
        :param file_path: name of the filepath the data is saved in as string
        """
        self._file_path = file_path

    def list_movies(self):
        """
        Reads the movie storage file and creates a dictionary
        :return: movie database as dictionary
        """
        try:
            with open(self._file_path, "r", encoding="utf-8") as handle:
                cvs_data = handle.readlines()
        except FileNotFoundError:
            self.save_file("title,year,rating,poster,imdb-url,flag,comment\n")
            return {}
        if not cvs_data:
            with open(self._file_path, "w") as handle:
                handle.write("title,year,rating,poster,imdb-url,flag,comment\n")
        if len(cvs_data) == 1:
            return {}
        data = {}
        for line in cvs_data[1:]:
            data_elements = line.split(",")
            data[data_elements[0]] = {
                "year": int(data_elements[1]),
                "rating": float(data_elements[2]),
                "poster": data_elements[3],
                "imdb-url": data_elements[4],
                "flag": data_elements[5].split("|"),
                "comment": data_elements[-1][:-1]
            }
        return data

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
        with open(self._file_path, "r", encoding="utf-8") as handle:
            movies = handle.read()

        movies += f"{title},{year},{rating},{poster},{url},{"|".join(flag)},\n"

        self.save_file(movies)

    def delete_movie(self, title):
        """
        Gets the movies with their entries, deletes a movie and calls for saving the change to the
        database
        :param title: movie name as string
        """
        with open(self._file_path, "r", encoding="utf-8") as handle:
            movies = handle.readlines()
        new_movies = ""
        for line in movies:
            movie_elements = line.split(",")
            if title.lower() != movie_elements[0].lower():
                new_movies += line
        self.save_file(new_movies)

    def update_movie(self, title, comment):
        """
        Adds a comment to a movie, calls for saving the change to the database
        :param title: movie name as string
        :param comment: comment to add to the movie as string
        """
        with open(self._file_path, "r", encoding="utf-8") as handle:
            movies = handle.readlines()
        movie_string = ""
        for line in movies:
            movie_elements = line.split(",")
            if title in movie_elements[0]:
                line = line.replace(movie_elements[-1], comment + "\n")
            movie_string += line
        self.save_file(movie_string)

    def save_file(self, movies):
        """Writes the movie dictionary in the database"""
        with open(self._file_path, "w") as handle:
            handle.write(movies)
