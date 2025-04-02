from app.movie_app import MovieApp
from storage.storage_csv import StorageCsv
from storage.storage_json import StorageJson
from utils.colors import Colors
from utils.file_manager import get_database_name, parse_argument


def main():
    """Handles program start parameters and initializes the movie app."""
    # parsing the start parameter
    args = parse_argument()

    # creating the name for the database from start parameter
    database_name = get_database_name(args.user)

    # deciding what file type is created as the database
    if database_name.endswith(".csv"):
        storage = StorageCsv("data/" + database_name)
    else:
        storage = StorageJson("data/" + database_name)

    print(f"{Colors.orange}You can access your database in the future by typing in "
          f"{Colors.blue}{database_name}{Colors.orange} as the start parameter.{Colors.reset}")
    input(f"{Colors.orange}\nPress enter to continue...{Colors.reset}")
    movie_app = MovieApp(storage)
    movie_app.run()


if __name__ == "__main__":
    main()
