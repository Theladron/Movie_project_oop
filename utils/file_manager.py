import argparse
import os


def parse_argument():
    """
    Parses the command line arguments for the movie database.
    :return: start parameter as string
    """
    parser = argparse.ArgumentParser(description="Database Name")
    parser.add_argument(
        'user',
        type=str,
        nargs="?",
        default="",
        help="Your movie storage file"
    )
    return parser.parse_args()


def get_database_name(user_input, default_prefix="data"):
    """
    Generates the database name based on the given user input.
    :param user_input: start parameter as string
    :param default_prefix: prefix in case no start parameter was given
    :return: filename as string
    """
    # getting the current unique number for default filename creation
    storage_files = os.listdir("./data")
    data_number = 0
    for file in storage_files:
        if default_prefix in file:
            data_number += 1

    # generating a standard-name out of the unique number if program was started without parameter
    if not user_input:
        return f"{default_prefix}{data_number}.json"

    # checking the validity of the start parameter, creating a valid file name
    check_arg = user_input.split(".")
    if len(check_arg) == 2 and check_arg[1] in ["csv", "json"]:
        return f"{check_arg[0]}.{check_arg[1]}"
    else:
        return f"{user_input.replace('.', '')}.json"