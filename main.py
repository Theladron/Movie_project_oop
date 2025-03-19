from app.movie_app import MovieApp
from storage.storage_json import StorageJson
from storage.storage_csv import StorageCsv
import argparse
import os


def main():

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
    if "csv" in args.user:
        storage = StorageCsv("data/" + args.user)
    else:
        storage = StorageJson("data/" + args.user)
    movie_app = MovieApp(storage)
    movie_app.run()


if __name__ == "__main__":
    main()
