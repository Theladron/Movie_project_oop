import movie_storage
import user_input
import random


def exit_program():
    """exits the program"""
    print("\nBye!")
    exit()


def list_movies():
    """
    prints a list of all the movies in the JSON file,
    with year and rating
    """
    movies = movie_storage.list_movies()
    for movie in movies:
        print(f"{movie} ({movies[movie]["year"]}): {movies[movie]["rating"]}")
    input("\nPress enter to continue...")


def add_movie():
    """
    takes user input for a new movie, year and rating,
    calls for saving the input to the JSON File
    """
    movies = movie_storage.list_movies()
    print("Enter the name of the movie: ", end="")
    title = user_input.u_input("str")
    for movie in movies:
        if title.lower() == movie.lower():
            print(f"The movie {title} already exists.")
            input("\nPress enter to continue...")
            return False
    print("Enter the year the movie was created: ", end="")
    year = user_input.u_input("int")
    print("Enter the movie rating: ", end="")
    rating = user_input.add_exception("rating")
    movie_storage.add_movie(title, year, rating)
    print(f"The movie '{title}' was added to the list.")
    input("\nPress enter to continue...")


def delete_movie():
    """
    takes user input for an existing movie,
    calls for saving the changes in the JSON File
    """
    movies = movie_storage.list_movies()
    print("Enter the name of the movie: ", end="")
    title = user_input.u_input("str")
    for movie in movies:
        if title.lower() == movie.lower():
            movie_storage.delete_movie(movie)
            print(f"The movie '{title}' was deleted.")
            input("\nPress enter to continue...")
            return
    print(f"The movie {title} does not exist.")
    input("\nPress enter to continue...")


def update_movie():
    """
    takes user input for an existing movie and new rating,
    calls for saving the input to the JSON File
    """
    movies = movie_storage.list_movies()
    print("Enter the name of the movie: ", end="")
    title = user_input.u_input("str")
    for movie in movies:
        if title.lower() == movie.lower():
            print("Enter the movie rating: ", end="")
            rating = user_input.add_exception("rating")
            movie_storage.update_movie(movie, rating)
            print(f"The movie '{title}' was updated")
            input("\nPress enter to continue...")
            return
    print(f"The movie {title} does not exist.")
    input("\nPress enter to continue...")


def movie_stats():
    """calls for average rating, median rating, best and worst movie """
    movies = movie_storage.list_movies()
    rating_list = []
    for movie in movies:
        rating_list.append(movies[movie]["rating"])
    print("Movie statistics\n")
    avg_rating(rating_list)
    median_rating(rating_list)
    best_movie(movies)
    worst_movie(movies)
    input("\nPress enter to continue...")


def avg_rating(rating_list):
    """prints average rating for the movie ratings in the JSON file"""
    avg = 0
    for rating in rating_list:
        avg += rating
    print(f"Average movie rating: "
          f"{round(avg / len(rating_list), 1)}")


def median_rating(rating_list):
    """prints median rating for the movie ratings in the JSON file"""
    rating_list.sort()
    if len(rating_list) % 2 != 0:
        print(f"Median movie rating: "
              f"{rating_list[round(len(rating_list) / 2)]}")
    else:
        print(f"Median movie rating: "
            f"{((rating_list[round(len(rating_list) / 2)]
            + rating_list[round(len(rating_list) / 2 + 1)]) / 2)}")


def best_movie(movies):
    """prints best movie by rating for the movie ratings in the JSON file"""
    sort_movies = sorted(movies, key=lambda x: movies[x]["rating"], reverse=True)
    check_val = 0
    print("\nBest movie(s):")
    for movie in sort_movies:
        if movies[movie]["rating"] >= check_val:
            print(f"{movie} ({movies[movie]["year"]}):"
                f" {movies[movie]["rating"]}")
            check_val = movies[movie]["rating"]
        else:
            break


def worst_movie(movies):
    """prints worst movie by rating for the movie ratings in the JSON file"""
    sort_movies = sorted(movies, key=lambda x: movies[x]["rating"])
    check_val = 10
    print("\nWorst movie(s):")
    for movie in sort_movies:
        if movies[movie]["rating"] <= check_val:
            print(f"{movie} ({movies[movie]["year"]}):"
                f" {movies[movie]["rating"]}")
            check_val = movies[movie]["rating"]
        else:
            break


def random_movie():
    """prints a random movie with year and rating from the JSON file"""
    movies = movie_storage.list_movies()
    r_number = random.randint(0, len(movies))
    counter = 0
    print("Your movie of choice is:")
    for movie in movies:
        if counter == r_number:
            print(f"{movie} ({movies[movie]["year"]}): {movies[movie]["rating"]}")
            input("\nPress enter to continue...")
            break
        counter += 1


def search_movie():
    """
    takes user input, searches for movies that contain the user input in
    the JSON file, prints out these movies with year and rating
    """
    print("Enter part of the movie you want to search for: ", end="")
    movies = movie_storage.list_movies()
    user_search = user_input.u_input("str").lower()
    movie_found = False
    for movie in movies:
        if user_search in movie.lower():
            print(f"{movie} ({movies[movie]["year"]}): {movies[movie]["rating"]}")
            movie_found = True
    if not movie_found:
        print(f"No movie was found for {user_search}")
    input("\nPress enter to continue...")


def sorted_by_rating():
    """
    sorts the movies in the JSON file by rating,
    prints out movies, year and rating in descending order
    """
    movies = movie_storage.list_movies()
    sort_movies = sorted(movies, key=lambda x: movies[x]["rating"], reverse=True)
    print("Movies sorted by rating:")
    for movie in sort_movies:
        print(f"{movie} ({movies[movie]["year"]}): {movies[movie]["rating"]}")
    input("\nPress enter to continue...")


def sorted_by_year():
    """
    sorts the movies in the JSON file by year,
    prints out movies, year and rating in descending order
    """
    movies = movie_storage.list_movies()
    sort_movies = sorted(movies, key=lambda x: movies[x]["year"], reverse=True)
    print("Movies sorted by year:")
    for movie in sort_movies:
        print(f"{movie} ({movies[movie]["year"]}): {movies[movie]["rating"]}")
    input("\nPress enter to continue...")


def filter_movies():
    """
    Takes user input for minimum rating, start and end year,
    prints the movies from the JSON file matching the users criteria
    """
    movies = movie_storage.list_movies()
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
            if (movies[movie]["rating"] >= min_rat
            and movies[movie]["year"] >= start):
                print(f"{movie} ({movies[movie]["year"]}): {movies[movie]["rating"]}")
    else:
        for movie in movies:
            if (movies[movie]["rating"] >= min_rat
            and start <= movies[movie]["year"] <= end):
                print(f"{movie} ({movies[movie]["year"]}): {movies[movie]["rating"]}")
    input("\nPress enter to continue...")
