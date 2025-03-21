from utils.colors import Colors


def user_string_input(prompt):
    """
    Gets the user input, handles exceptions
    :param prompt: Input description as str
    :return: User input as string, float or integer, depending on exceptions
    """
    while True:
        user_input = input(prompt)

        if not user_input:
            break

        # exceptions for start and end year filter
        elif f"year{Colors.green} (leave blank for no" in prompt:
            if user_input.isnumeric():
                return int(user_input)
            print(f"{Colors.bold}{Colors.red}Error{Colors.reset}{Colors.red}. "
                  f"Please leave blank or enter a positive, whole number.{Colors.reset}")

        # exceptions for minimum rating
        elif f"Enter {Colors.blue}minimum rating" in prompt:
            if user_input.isnumeric():
                return float(user_input)
            else:
                test_input = user_input.split(".")
                if (len(test_input) == 2
                        and test_input[0].isnumeric()
                        and test_input[1].isnumeric()):
                    return float(user_input)
            print(f"{Colors.bold}{Colors.red}Error{Colors.reset}{Colors.red}. "
                  f"Please leave blank or enter a positive number.{Colors.reset}")
        else:
            return user_input


def user_int_input(prompt):
    """
    gets int user input, handles exceptions
    :param prompt: Input description as str
    :return: user input as int
    """
    while True:
        try:
            user_input = int(input(prompt))
        except ValueError:
            print(f"{Colors.bold}{Colors.red}Error{Colors.reset}{Colors.red}. "
                  f"Please enter a whole number.{Colors.reset}")
        else:
            # general exception, no input should be negative
            if user_input < 0:
                print(f"{Colors.bold}{Colors.red}Error{Colors.reset}{Colors.red}. "
                      f"Please enter a positive, whole number.{Colors.reset}")
            # exception for menu choice
            elif "Enter Choice (1-11): " in prompt and user_input > 11:
                print(f"{Colors.bold}{Colors.red}Error{Colors.reset}{Colors.red}. "
                      f"Please enter a whole number between 0-101.{Colors.reset}")
            else:
                return user_input
