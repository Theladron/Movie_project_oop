from app.movie_app import MovieApp
from storage.storage_json import StorageJson
from storage.storage_csv import StorageCsv
from utils.colors import Colors
import argparse
import os




def main():
    """Creates the name for the storage file, handles program start parameters"""
    # checking through the data files to determine which generic number has not been used
    storage_files = os.listdir("./data")
    data_number = 0
    for file in storage_files:
        if "data" in file:
            data_number += 1
    parser = argparse.ArgumentParser(description="Database Name")

    # Making sure each time no argument is given, a new file is created
    parser.add_argument('user',
                        type=str,
                        nargs="?",
                        default="data"+str(data_number),
                        help="Your movie storage file")
    args = parser.parse_args()

    # checks start parameter to decide which filetype to save the database in, default = json
    if "csv" in args.user:
        check_arg = args.user.split(".")
        if len(check_arg) == 2 and check_arg[1] in "csv" :
            database_name = check_arg[0] + ".csv"
            storage = StorageCsv("data/" + database_name)
        else:
            database_name = args.user.replace(".", "") + ".csv"
            storage = StorageCsv("data/" + database_name)

    else:
        check_arg = args.user.split(".")
        if len(check_arg) == 2 and check_arg[1] in "json":
            database_name = check_arg[0] + ".json"
            storage = StorageJson("data/" + database_name)

        else:
            database_name = args.user.replace(".", "") + ".json"
            storage = StorageJson("data/" + database_name)

    print(f"{Colors.orange}Your can access your database in the future by typing in "
          f"{Colors.blue}{database_name}{Colors.orange} as the start parameter.{Colors.reset}")
    input(f"{Colors.orange}\nPress enter to continue...{Colors.reset}")
    movie_app = MovieApp(storage)
    movie_app.run()


if __name__ == "__main__":
    main()
