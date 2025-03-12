def u_input(string):
    """
    gets user input, handles exceptions for input types
    :param string: the type you want the input to be as str
    :return: user input
    """
    match string:

        case "int":
            while True:
                try:
                    user_input = int(input(""))
                except ValueError:
                    print("Error. Please enter a whole number: ", end="")
                else:
                    if user_input < 0:
                        print("Error. Please enter a positive, "
                        "whole number: ", end="")
                    else:
                        break

        case "float":
            while True:
                try:
                    user_input = float(input(""))
                except ValueError:
                    print("Error. Please enter a number: ", end="")
                else:
                    break

        case "str":
            user_input = input("")

    return user_input


def add_exception(occasion):
    """
    handles additional exceptions for specific user input criteria
    :param occasion: takes the occasion as str
    :return: user input
    """
    match occasion:

        case "menu":
            while True:
                user_input = u_input("int")
                if user_input > 10:
                    print("Error. Please enter a whole number "
                    "between 0-10: ", end="")
                else:
                    break

        case "rating":
            while True:
                user_input = u_input("float")
                if user_input > 10:
                    print("Error. Please enter a number "
                    "between 0-10: ", end="")
                elif user_input < 0:
                    print("Error. Please enter a positive number "
                    "between 0-10: ", end="")
                else:
                    break

        case "range":
            while True:
                user_input = u_input("str")
                if not user_input:
                    break
                elif user_input.isnumeric():
                    user_input = int(user_input)
                    break
                print("Error. Please leave blank or enter a positive, "
                "whole number: ", end="")

        case "floatrange":
            while True:
                user_input = u_input("str")
                if not user_input:
                    break
                elif user_input.isnumeric():
                    user_input = float(user_input)
                    break
                else:
                    test_input = user_input.split(".")
                    if len(test_input) == 2:
                        if (test_input[0].isnumeric()
                            and test_input[1].isnumeric()):
                            user_input = float(user_input)
                            break
                    print("Error. Please leave blank or enter a positive "
                    "number: ", end="")

    return user_input