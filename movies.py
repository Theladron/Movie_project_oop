import movie_storage
import user_input
import movie_functions

funct_dict = {
            0   :   movie_functions.exit_program,
            1   :   movie_functions.list_movies,
            2   :   movie_functions.add_movie,
            3   :   movie_functions.delete_movie,
            4   :   movie_functions.update_movie,
            5   :   movie_functions.movie_stats,
            6   :   movie_functions.random_movie,
            7   :   movie_functions.search_movie,
            8   :   movie_functions.sorted_by_rating,
            9   :   movie_functions.sorted_by_year,
            10  :   movie_functions.filter_movies
}


def main():
    """prints menu options, calls for the functions and handles empty dict"""
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

    Enter choice (1-10): """, end="")
        u_input = user_input.add_exception("menu")
        movies = movie_storage.list_movies()
        if not movies:
            if not (u_input == 2 or u_input == 0):
                print("Error. The movie list is empty. Please"
                " enter '2' and add a movie to the list.")
                input("Press enter to continue...")
                continue
        funct_dict[u_input]()



if __name__ == "__main__":
    main()
