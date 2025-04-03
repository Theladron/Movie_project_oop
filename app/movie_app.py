import os
import random

import requests
from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader

from app.user_input import user_int_input, user_string_input
from utils.colors import Colors

load_dotenv()
API_KEY = os.getenv("API_KEY")


class MovieApp:
    """
    Represents a movie app to manipulate a movie database, get statistics and generate a visual
    representation in a HTML page

    Attributes:
        _storage (Storage) : Storage class Instance with the movie database savefile handling
    """

    def __init__(self, storage):
        """
        Initializes the MovieApp class instance with its storage
        :param storage: Storage class instance
        """
        self._storage = storage

    @staticmethod
    def _command_exit_program():
        """exits the program"""
        print(f"{Colors.orange}bye!{Colors.reset}")
        exit()

    def _command_list_movies(self):
        """prints a list of all the movies with year and rating"""
        movies = self._storage.list_movies()
        if not movies:
            return
        print(f"{Colors.orange}\nMovies in the database:{Colors.reset}")
        movie_list = [(f"{movie} ({movies[movie]["year"]}) {Colors.blue}{movies[movie]["rating"]}"
                       f"{Colors.reset}") for movie in movies]
        print("\n".join(movie_list))

    @staticmethod
    def get_movie_data(title):
        """
        Searches the api for information about the movie the user entered, handles exceptions
        :param title: user given movie name as string
        :return: movie data as dict, None if exception found
        """
        try:
            response = requests.get("http://www.omdbapi.com/?apikey=" + API_KEY + "&t=" + title)
        except requests.exceptions.ConnectionError:
            print(f"{Colors.bold}{Colors.red}Error{Colors.reset}{Colors.red} "
                  f"fetching data. Please check your internet connection.{Colors.reset}")
            return
        if not response.status_code == 200:
            print(f"{Colors.bold}{Colors.red}Error{Colors.reset}{Colors.red} fetching data. "
                  f"Database might be busy, please try again later.{Colors.reset}")
            return
        movie_data = response.json()
        if movie_data.get("Response") == "False":
            print(f"{Colors.bold}{Colors.red}Error{Colors.reset}{Colors.red}. "
                  f"The movie does not exist.{Colors.reset}")
            return
        return movie_data

    @staticmethod
    def validate_movie_data(movie_data):
        """
        Searches for movie year, rating, imdb-link, countries and their flags and
        adds it to the movie data, handles exceptions
        :param movie_data: the movie file as dictionary
        :return: updated movie data as dict, flag_url(s) as list
        """
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

        # Adding Fallback icon in case the movie has no poster
        if "N/A" in movie_data["Poster"]:
            movie_data["Poster"] = "/_static/fallback_poster.png"

        flag_url = []
        if "N/A" in movie_data["Country"]:
            flag_url.append("/_static/fallback_flag.png")
        else:
            countries = movie_data["Country"].split(", ")
            for country in countries:
                response = requests.get(f"https://restcountries.com/v3.1/name/{country}")
                country_data = response.json()
                # extract the flag(s) in a list
                flag_url.append(country_data[0]['flags']['png'])
        return movie_data, flag_url

    def _command_add_movie(self):
        """
        takes user input for a new movie, searches for the movie in the api database,
        gets the necessary information and calls for saving the movie in the database,
        handles exceptions
         """
        movies = self._storage.list_movies()
        title = user_string_input(f"{Colors.green}Enter the name of "
                                  f"the movie (leave blank to return"
                                  f" to menu): {Colors.reset}")
        if not title:
            return

        if any(movie for movie in movies if title.lower() == movie.lower()):
            print(f"The movie {Colors.blue}{title}{Colors.reset} already exists.")
            return
        omdb_api_data = self.get_movie_data(title)

        if not omdb_api_data:
            return

        movie_data, flag_url = self.validate_movie_data(omdb_api_data)

        self._storage.add_movie(movie_data["Title"],
                                movie_data["Year"],
                                movie_data["imdbRating"],
                                movie_data["Poster"],
                                "https://www.imdb.com/title/" + movie_data["imdbID"] + "/",
                                flag_url)
        print(f"The movie {Colors.blue}{movie_data['Title']}{Colors.reset} was added to the list.")

    def _command_delete_movie(self):
        """takes user input for an existing movie and calls for deletion"""
        movies = self._storage.list_movies()
        title = user_string_input(f"{Colors.green}Enter the name of the "
                                  f"movie: {Colors.reset}")
        if not title:
            return
        movie = next((movie for movie in movies if title.lower() == movie.lower()), None)
        if movie:
            self._storage.delete_movie(movie)
            print(f"The movie {Colors.blue}{movie}{Colors.reset} was deleted.")
            return
        print(f"The movie {Colors.blue}{title}{Colors.reset} does not exist.")

    def _command_update_movie(self):
        """Allows user to search for a movie and add a comment for it"""
        movies = self._storage.list_movies()
        title = user_string_input(f"{Colors.green}Enter the name of the "
                                  f"{Colors.blue}movie{Colors.green}: {Colors.reset}")
        if not title:
            return
        movie = next((movie for movie in movies if title.lower() == movie.lower()), None)
        if movie:
            comment = user_string_input(f"{Colors.green}Enter "
                                        f"comment: {Colors.reset}")
            self._storage.update_movie(movie, comment)
            print(f"The movie '{Colors.blue}{title}{Colors.reset}' was updated")
            return
        print(f"The movie {Colors.blue}{title}{Colors.reset} does not exist.")

    def _command_movie_stats(self):
        """calls for average rating, median rating, best and worst movie """
        movies = self._storage.list_movies()
        rating_list = [float(movies[movie]["rating"]) for movie in movies]
        print(f"{Colors.orange}Movie statistics\n{Colors.reset}")
        self._avg_rating(rating_list)
        self._median_rating(rating_list)
        self._best_movie(movies)
        self._worst_movie(movies)

    @staticmethod
    def _avg_rating(rating_list):
        """prints average rating for the movie ratings"""
        avg = sum(rating_list)
        print(f"{Colors.cyan}Average movie rating: {Colors.blue}"
              f"{round(avg / len(rating_list), 1)}{Colors.reset}")

    @staticmethod
    def _median_rating(rating_list):
        """prints median rating for the movie ratings"""
        rating_list.sort()
        if len(rating_list) % 2 != 0:
            print(f"{Colors.cyan}Median movie rating: {Colors.blue}"
                  f"{rating_list[round(len(rating_list) / 2)]}{Colors.reset}")
        else:
            print(f"Median movie rating: {Colors.blue}"
                  f"{round((rating_list[len(rating_list) // 2]
                            + rating_list[len(rating_list) // 2 - 1]) / 2, 2)}{Colors.reset}")

    @staticmethod
    def _best_movie(movies):
        """prints best movie by rating for the movie ratings"""
        sort_movies = sorted(movies, key=lambda x: (-float(movies[x]["rating"]), x))
        check_val = 0
        print(f"{Colors.cyan}\nBest movie(s):{Colors.reset}")
        for movie in sort_movies:
            if float(movies[movie]["rating"]) >= check_val:
                print(f"{movie} ({movies[movie]['year']}):"
                      f" {Colors.blue}{movies[movie]['rating']}{Colors.reset}")
                check_val = float(movies[movie]["rating"])
            else:
                break

    @staticmethod
    def _worst_movie(movies):
        """prints worst movie by rating for the movie ratings"""
        sort_movies = sorted(movies, key=lambda x: (float(movies[x]["rating"]), x))
        check_val = 10
        print(f"{Colors.cyan}\nWorst movie(s):{Colors.reset}")
        for movie in sort_movies:
            if float(movies[movie]["rating"]) <= check_val:
                print(f"{movie} ({movies[movie]["year"]}):"
                      f" {Colors.blue}{movies[movie]["rating"]}{Colors.reset}")
                check_val = float(movies[movie]["rating"])
            else:
                break

    def _command_random_movie(self):
        """prints a random movie with year and rating"""
        movies = self._storage.list_movies()
        r_number = random.randint(0, len(movies) - 1)
        counter = 0
        print(f"{Colors.cyan}Your movie of choice is:{Colors.reset}")
        for movie in movies:
            if counter == r_number:
                print(f"{movie} ({movies[movie]["year"]}): "
                      f"{Colors.blue}{movies[movie]["rating"]}{Colors.reset}")
                break
            counter += 1

    def _command_search_movie(self):
        """
        takes user input, searches for movies that contain the user input,
        prints out these movies with year and rating
        """
        movies = self._storage.list_movies()
        user_search = user_string_input(f"{Colors.green}Enter part of the "
                                        f"movie you want to search for:"
                                        f" {Colors.reset}").lower()
        movie_found = False
        for movie in movies:
            if user_search in movie.lower():
                print(f"{movie} ({movies[movie]["year"]}): "
                      f"{Colors.blue}{movies[movie]["rating"]}{Colors.reset}")
                movie_found = True
        if not movie_found:
            print(f"{Colors.red}No movie was found for {Colors.blue}{user_search}{Colors.reset}")

    def _command_sorted_by_rating(self):
        """
        sorts the movies by rating,
        prints out movies, year and rating in descending order
         """
        movies = self._storage.list_movies()
        sort_movies = sorted(movies, key=lambda x: (-float(movies[x]["rating"]), x))
        print(f"{Colors.cyan}Movies sorted by rating:{Colors.reset}")
        for movie in sort_movies:
            print(f"{movie} ({movies[movie]["year"]}): "
                  f"{Colors.blue}{movies[movie]["rating"]}{Colors.reset}")

    def _command_sorted_by_year(self):
        """
        sorts the movies by year,
        prints out movies, year and rating in descending order
        """
        movies = self._storage.list_movies()
        sort_movies = sorted(movies, key=lambda x: (-float(movies[x]["year"]), x))
        print(f"{Colors.cyan}Movies sorted by year:{Colors.reset}")
        for movie in sort_movies:
            print(f"{movie} ({movies[movie]["year"]}): "
                  f"{Colors.blue}{movies[movie]["rating"]}{Colors.reset}")

    def _command_filter_movies(self):
        """
        Takes user input for minimum rating, start and end year,
        prints the movies matching the users criteria
        """
        movies = self._storage.list_movies()
        min_rat = user_string_input(f"{Colors.green}Enter {Colors.blue}minimum rating"
                                    f"{Colors.green} (leave blank for no minimum "
                                    f"rating): {Colors.reset}")
        start = user_string_input(f"{Colors.green}Enter {Colors.blue}start year"
                                  f"{Colors.green} (leave blank for no "
                                  f"start year): {Colors.reset}")
        end = user_string_input(f"{Colors.green}Enter {Colors.blue}end year"
                                f"{Colors.green} (leave blank for no "
                                f"end year): {Colors.reset}")
        print(f"{Colors.cyan}Movies that match your criteria:{Colors.reset}")
        movie_found = False
        if not min_rat:
            min_rat = 0
        if not start:
            start = 0
        if not end:
            for movie in movies:
                if (float(movies[movie]["rating"]) >= min_rat
                        and int(movies[movie]["year"]) >= start):
                    print(f"{movie} ({movies[movie]["year"]}):"
                          f" {Colors.blue}{movies[movie]["rating"]}{Colors.reset}")
                    movie_found = True
        else:
            for movie in movies:
                if (float(movies[movie]["rating"]) >= min_rat
                        and start <= int(movies[movie]["year"]) <= end):
                    print(f"{movie} ({movies[movie]["year"]}):"
                          f" {Colors.blue}{movies[movie]["rating"]}{Colors.reset}")
                    movie_found = True
        if not movie_found:
            print(f"{Colors.red}No movies found for your filter options.{Colors.reset}")

    def _generate_website(self):
        movies = self._storage.list_movies()
        env = Environment(loader=FileSystemLoader('./_static'))
        with open("./data/index.html", "w") as handle:
            handle.write(env.get_template("index_template.html").render(movies=movies))
        print(f"{Colors.orange}Website was generated successfully.{Colors.reset}")

    def run(self):
        """prints available options and calls for user input for the different methods"""
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
            print(f"""{Colors.orange}********** My Movies Database **********{Colors.reset}

            {Colors.bold}{Colors.cyan}Menu:{Colors.reset}
            {Colors.blue}0.{Colors.reset} Exit
            {Colors.blue}1.{Colors.reset} List movies
            {Colors.blue}2.{Colors.reset} Add movie
            {Colors.blue}3.{Colors.reset} Delete movie
            {Colors.blue}4.{Colors.reset} Update movie
            {Colors.blue}5.{Colors.reset} Stats
            {Colors.blue}6.{Colors.reset} Random movie
            {Colors.blue}7.{Colors.reset} Search movie
            {Colors.blue}8.{Colors.reset} Movies sorted by rating
            {Colors.blue}9.{Colors.reset} Movies sorted by year
            {Colors.blue}10.{Colors.reset} Filter movies
            {Colors.blue}11.{Colors.reset} Generate Website
                """)
            u_input = user_int_input(f"{Colors.blue}Enter choice (1-11): {Colors.reset}")
            if not self._storage.list_movies():
                if not (u_input == 2 or u_input == 0):
                    print(f"{Colors.bold}{Colors.red}Error{Colors.reset}{Colors.red}. "
                          f"The movie list is empty. Please enter {Colors.blue}2{Colors.reset} "
                          f"and add a movie to the list.{Colors.reset}")
                    input(f"{Colors.orange}Press enter to continue...{Colors.reset}")
                    continue
            funct_dict[u_input]()
            input(f"{Colors.orange}\nPress enter to continue...{Colors.reset}")
