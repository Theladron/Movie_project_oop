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
            movies = json.loads(handle.read())
        for movie in movies:
            print(f"{movie} ({movies[movie]["year"]}): {movies[movie]["rating"]}")
        input("\nPress enter to continue...")

    def add_movie(self, title, year, rating):
        """
        takes user input for a new movie, year and rating,
        calls for saving the input to the JSON File
        """
        with open(self._file_path, "r") as handle:
            movies = json.loads(handle.read())
        for movie in movies:
            if title.lower() == movie.lower():
                print(f"The movie {title} already exists.")
                input("\nPress enter to continue...")
                return
        movies[title] = {"year": year, "rating": rating}
        with open(self._file_path, "w") as handle:
            handle.write(json.dumps(movies, indent=4))
        print(f"The movie '{title}' was added to the list.")
        input("\nPress enter to continue...")

    def delete_movie(self, title):
        """
        takes user input for an existing movie,
        calls for saving the changes in the JSON File
        """
        with open(self._file_path, "r") as handle:
            movies = json.loads(handle.read())
        for movie in movies:
            if title.lower() == movie.lower():
                del movies[movie]
                with open (self._file_path, "w") as handle:
                    handle.write(json.dumps(movies, indent=4))
                print(f"The movie '{title}' was deleted.")
                input("\nPress enter to continue...")
                return
        print(f"The movie {title} does not exist.")
        input("\nPress enter to continue...")

    def update_movie(self, title, rating):
        """
        takes user input for an existing movie and new rating,
        calls for saving the input to the JSON File
        """
        with open(self._file_path, "r") as handle:
            movies = json.loads(handle.read())
        for movie in movies:
            if title.lower() == movie.lower():
                movies[title]["rating"] = rating
                with open(self._file_path, "w") as handle:
                    handle.write(json.dumps(movies, indent=4))
                print(f"The movie '{title}' was updated")
                input("\nPress enter to continue...")
                return
        print(f"The movie {title} does not exist.")
        input("\nPress enter to continue...")

