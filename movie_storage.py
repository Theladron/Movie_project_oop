import json

def list_movies():
    """
    Returns a dictionary of dictionaries that
    contains the movies information in the database.
    The function loads the information from the JSON
    file and returns the data.
    """
    with open("data.json", "r") as handle:
        return json.loads(handle.read())


def add_movie(title, year, rating):
    """
    Adds a movie to the movies database.
    Loads the information from the JSON file, add the movie,
    and saves it.
    """
    data = list_movies()
    data[title] = {"year" : year, "rating" : rating}
    json_str = json.dumps(data, indent=4)
    with open("data.json", "w") as handle:
        handle.write(json_str)


def delete_movie(title):
    """
    Deletes a movie from the movies database.
    Loads the information from the JSON file, deletes the movie,
    and saves it.
    """
    data = list_movies()
    del data[title]
    json_str = json.dumps(data, indent=4)
    with open("data.json", "w") as handle:
        handle.write(json_str)


def update_movie(title, rating):
    """
    Updates a movie from the movies database.
    Loads the information from the JSON file, updates the movie,
    and saves it.
    """
    data = list_movies()
    data[title]["rating"] = rating
    json_str = json.dumps(data, indent=4)
    with open("data.json", "w") as handle:
        handle.write(json_str)
