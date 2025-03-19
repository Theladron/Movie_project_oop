from app.movie_app import MovieApp
from storage.storage_json import StorageJson
from storage.storage_csv import StorageCsv


def main():
    storage = StorageCsv('data/data.cvs')
    movie_app = MovieApp(storage)
    movie_app.run()

if __name__ == "__main__":
    main()