from dotenv import load_dotenv
import os
import random
import requests
from app import user_input
from jinja2 import Environment, FileSystemLoader

load_dotenv()
API_KEY = os.getenv("API_KEY")

class MovieApp:
    def __init__(self, storage):
        self._storage = storage

    def _command_exit_program(self):
        """exits the program"""
        print("bye!")
        exit()

    def _command_list_movies(self):
        """
        prints a list of all the movies with year and rating
        """
        movies = self._storage.list_movies()
        movie_list = [f"{movie} ({movies[movie]["year"]})"
                      f": {movies[movie]["rating"]}" for movie in movies]
        print("\n".join(movie_list))

    def _command_add_movie(self):
        """
        takes user input for a new movie, year and rating,
        calls for saving the input
         """
        movies = self._storage.list_movies()
        print("Enter the name of the movie: ", end="")
        title = user_input.u_input("str")
        for movie in movies:
            if title.lower() == movie.lower():
                print(f"The movie {title} already exists.")
                return
        try:
            response = requests.get("http://www.omdbapi.com/?apikey="+API_KEY+"&t="+title)
        except requests.exceptions.ConnectionError:
            print("Error fetching data. Please check your internet connection.")
            return
        if not response.status_code == 200:
            print("Error fetching data. Database might be busy, please try again later.")
            return
        movie_data = response.json()
        if movie_data.get("Response") == "False":
            print("Error. The movie does not exist.")
            return

        # testing "Year" entry for integer, using 0 as fallback
        try:
            int(movie_data["Year"])
        except ValueError:
            try:
                int(movie_data["Year"][:4])
                movie_data["Year"] = movie_data["Year"][:4]
            except ValueError:
                movie_data["Year"] = 0

        # testing "Rating" entry for integer, using 0 as fallback
        try:
            float(movie_data["imdbRating"])
        except ValueError:
            movie_data["imdbRating"] = 0.0

        self._storage.add_movie(movie_data["Title"],
                                movie_data["Year"],
                                movie_data["imdbRating"],
                                movie_data["Poster"])
        print(f"The movie '{movie_data["Title"]}' was added to the list.")

    def _command_delete_movie(self):
        """
        takes user input for an existing movie,
        calls for saving the changes
        """
        movies = self._storage.list_movies()
        print("Enter the name of the movie: ", end="")
        title = user_input.u_input("str")

        for movie in movies:
            if title.lower() == movie.lower():
                self._storage.delete_movie(movie)
                print(f"The movie '{movie}' was deleted.")
                return
        print(f"The movie {title} does not exist.")

    def _command_update_movie(self):
        """
        takes user input for an existing movie and new rating,
        calls for saving the input
        """
        movies = self._storage.list_movies()
        print("Enter the name of the movie: ", end="")
        title = user_input.u_input("str")
        for movie in movies:
            if title.lower() == movie.lower():
                print("Enter the movie rating: ", end="")
                rating = user_input.add_exception("rating")
                self._storage.update_movie(movie, rating)
                print(f"The movie '{title}' was updated")
                return
        print(f"The movie {title} does not exist.")

    def _command_movie_stats(self):
        """calls for average rating, median rating, best and worst movie """
        movies = self._storage.list_movies()
        rating_list = [float(movies[movie]["rating"]) for movie in movies]
        print("Movie statistics\n")
        self._avg_rating(rating_list)
        self._median_rating(rating_list)
        self._best_movie(movies)
        self._worst_movie(movies)

    @staticmethod
    def _avg_rating(self, rating_list):
        """prints average rating for the movie ratings"""
        avg = sum(rating_list)
        print(f"Average movie rating: "
              f"{round(avg / len(rating_list), 1)}")

    @staticmethod
    def _median_rating(self, rating_list):
        """prints median rating for the movie ratings"""
        rating_list.sort()
        if len(rating_list) % 2 != 0:
            print(f"Median movie rating: "
                  f"{rating_list[round(len(rating_list) / 2)]}")
        else:
            print(f"Median movie rating: "
                  f"{((rating_list[round(len(rating_list) / 2)]
                       + rating_list[round(len(rating_list) / 2 + 1)]) / 2)}")

    @staticmethod
    def _best_movie(self, movies):
        """prints best movie by rating for the movie ratings"""
        sort_movies = sorted(movies, key=lambda x: (-float(movies[x]["rating"]), x))
        check_val = 0
        print("\nBest movie(s):")
        for movie in sort_movies:
            if float(movies[movie]["rating"]) >= check_val:
                print(f"{movie} ({movies[movie]['year']}):"
                      f" {movies[movie]['rating']}")
                check_val = float(movies[movie]["rating"])
            else:
                break

    @staticmethod
    def _worst_movie(self, movies):
        """prints worst movie by rating for the movie ratings"""
        sort_movies = sorted(movies, key=lambda x: (float(movies[x]["rating"]), x))
        check_val = 10
        print("\nWorst movie(s):")
        for movie in sort_movies:
            if float(movies[movie]["rating"]) <= check_val:
                print(f"{movie} ({movies[movie]["year"]}):"
                      f" {movies[movie]["rating"]}")
                check_val = float(movies[movie]["rating"])
            else:
                break

    def _command_random_movie(self):
        """prints a random movie with year and rating"""
        movies = self._storage.list_movies()
        r_number = random.randint(0, len(movies))
        counter = 0
        print("Your movie of choice is:")
        for movie in movies:
            if counter == r_number:
                print(f"{movie} ({movies[movie]["year"]}): {movies[movie]["rating"]}")
                break
            counter += 1

    def _command_search_movie(self):
        """
        takes user input, searches for movies that contain the user input,
        prints out these movies with year and rating
        """
        print("Enter part of the movie you want to search for: ", end="")
        movies = self._storage.list_movies()
        user_search = user_input.u_input("str").lower()
        movie_found = False
        for movie in movies:
            if user_search in movie.lower():
                print(f"{movie} ({movies[movie]["year"]}): {movies[movie]["rating"]}")
                movie_found = True
        if not movie_found:
            print(f"No movie was found for {user_search}")

    def _command_sorted_by_rating(self):
        """
        sorts the movies by rating,
        prints out movies, year and rating in descending order
         """
        movies = self._storage.list_movies()
        sort_movies = sorted(movies, key=lambda x: (-float(movies[x]["rating"]), x))
        print("Movies sorted by rating:")
        for movie in sort_movies:
            print(f"{movie} ({movies[movie]["year"]}): {movies[movie]["rating"]}")

    def _command_sorted_by_year(self):
        """
        sorts the movies by year,
        prints out movies, year and rating in descending order
        """
        movies = self._storage.list_movies()
        sort_movies = sorted(movies, key=lambda x: (-float(movies[x]["year"]), x))
        print("Movies sorted by year:")
        for movie in sort_movies:
            print(f"{movie} ({movies[movie]["year"]}): {movies[movie]["rating"]}")

    def _command_filter_movies(self):
        """
        Takes user input for minimum rating, start and end year,
        prints the movies matching the users criteria
        """
        movies = self._storage.list_movies()
        print(f"Enter minimum rating (leave "
              f"blank for no minimum rating): ", end="")
        min_rat = user_input.add_exception("floatrange")
        print(f"Enter start year "
              f"(leave blank for no start year): ", end="")
        start = user_input.add_exception("range")
        print("Enter end year "
              "(leave blank for no end year): ", end="")
        end = user_input.add_exception("range")
        print("Movies that match your criteria:")
        if not min_rat:
            min_rat = 0
        if not start:
            start = 0
        if not end:
            for movie in movies:
                if (float(movies[movie]["rating"]) >= min_rat
                        and int(movies[movie]["year"]) >= start):
                    print(f"{movie} ({movies[movie]["year"]}): {movies[movie]["rating"]}")
        else:
            for movie in movies:
                if (float(movies[movie]["rating"]) >= min_rat
                        and start <= int(movies[movie]["year"]) <= end):
                    print(f"{movie} ({movies[movie]["year"]}): {movies[movie]["rating"]}")

    def _generate_website(self):
        movies = self._storage.list_movies()
        env = Environment(loader=FileSystemLoader('../_static'))
        with open("../data/index.html", "w") as handle:
            handle.write(env.get_template("index_template.html").render(movies=movies))


    def run(self):
        funct_dict = {
            0: self._command_exit_program,
            1: self._command_list_movies,
            2: self._command_add_movie,
            3: self._command_delete_movie,
            4: self._command_update_movie,
            5: self._command_movie_stats,
            6: self._command_random_movie,
            7: self._command_search_movie,
            8: self._command_sorted_by_rating,
            9: self._command_sorted_by_year,
            10: self._command_filter_movies,
            11: self._generate_website
        }
        while True:
            print("""********** My Movies Database **********

            Menu:
            0. Exit
            1. List movies
            2. Add movie
            3. Delete movie
            4. Update movie
            5. Stats
            6. Random movie
            7. Search movie
            8. Movies sorted by rating
            9. Movies sorted by year
            10. Filter movies
            11. Generate Website

                Enter choice (1-10): """, end="")
            u_input = user_input.add_exception("menu")
            if not self._storage.list_movies():
                if not (u_input == 2 or u_input == 0):
                    print("Error. The movie list is empty. Please"
                          " enter '2' and add a movie to the list.")
                    input("Press enter to continue...")
                    continue
            funct_dict[u_input]()
            input("\nPress enter to continue...")
