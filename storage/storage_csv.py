from storage.istorage import IStorage

class StorageCsv(IStorage):

    def __init__(self, file_path):
        self._file_path = file_path

    def list_movies(self):
        """
        prints a list of all the movies in the JSON file,
        with year and rating
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
                                        "year"      : int(data_elements[1]),
                                        "rating"    : float(data_elements[2]),
                                        "poster"    : data_elements[3],
                                        "imdb-url"  : data_elements[4],
                                        "flag"      : data_elements[5].split("|"),
                                        "comment"   : data_elements[-1][:-1]
                                        }
        return data


    def add_movie(self, title, year, rating, poster, url, flag):
        """
        takes user input for a new movie, year and rating,
        calls for saving the input to the JSON File
        """
        with open(self._file_path, "r", encoding="utf-8") as handle:
            movies = handle.read()

        movies += f"{title},{year},{rating},{poster},{url},{"|".join(flag)},\n"

        self.save_file(movies)

    def delete_movie(self, title):
        """
        takes user input for an existing movie,
        calls for saving the changes in the JSON File
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
        takes user input for an existing movie and new rating,
        calls for saving the input to the JSON File
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
        with open(self._file_path, "w") as handle:
            handle.write(movies)
