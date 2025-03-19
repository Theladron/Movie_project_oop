def user_string_input(prompt):
    while True:
        user_input = input(prompt)

        if not user_input:
            break

        elif "year (leave blank for no" in prompt:
            if user_input.isnumeric():
                return int(user_input)
            print("Error. Please leave blank or enter a positive, "
                  "whole number.")

        elif "Enter minimum rating" in prompt:
            if user_input.isnumeric():
                return float(user_input)
            else:
                test_input = user_input.split(".")
                if (len(test_input) == 2
                        and test_input[0].isnumeric()
                        and test_input[1].isnumeric()):
                    return float(user_input)
            print("Error. Please leave blank or enter a positive "
                  "number.")
        else:
            return user_input


def user_float_input(prompt):
    while True:
        try:
            user_input = float(input(prompt))
        except ValueError:
            print("Error. Please enter a number.")
        else:
            return user_input


def user_int_input(prompt):
    while True:
        try:
            user_input = int(input(prompt))
        except ValueError:
            print("Error. Please enter a whole number.")
        else:

            if user_input < 0:
                print("Error. Please enter a positive, "
                      "whole number.")

            elif "Enter Choice (1-10): " in prompt and user_input > 11:
                print("Error. Please enter a whole number "
                      "between 0-10.")
            else:
                return user_input
