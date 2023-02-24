"""
==================

This module manages user inputs. Every function in this module is intended to
be used to ensure that the other programs can forget about wrong inputs.

Doctests can't be provided in this module (except for one function) as it
uses builtin input function.

==================
"""

from vehicle import valid_license_plate

def _get_integer_in_range(prompt, range_start, range_end, out_of_range_message):
    """
    Checks for user input to be between range indicated by `range_start` and
    `range_end` returning `out_of_range_message` if input is not valid

    :param str prompt: The prompt shown in terminal.
    :param int range_start: The beginning of the range.
    :param int range_end: The end of the range.
    :param str out_of_range_message: Message to be shown in case user input is out of range.

    :return: A correct integer.
    :rtype: int
    """
    while True:
        candidate = input(f"{prompt} (between {range_start} and {range_end}): ")

        try:
            spot = int(candidate)
            if spot >= range_start and spot <= range_end: return spot
            
            print(out_of_range_message)
        except ValueError:
            print("Number not valid!")

def yes_or_no(prompt):
    """
    A simple yes or no question. An empty answer (enter key) is considered a
    yes.

    :param str prompt: String indicating the prompt shown in the terminal.

    :return: The response of the question: True in case of "yes" answer.
    :rtype: bool
    """
    options = ["Y", "N", ""] #Empty input is considered as a yes.
    while True:
        candidate = input(f"{prompt} [Y/n]: ").upper()
        if candidate in options: return candidate!="N"
        print("Invalid Option")

def get_valid_spot(max_range):
    """
    Gets a parking spot from the user. Ensures that the parking spot is
    within the range of the parking.

    :param int max_range: Maximum garage capacity

    :return: The number of the parking spot.
    :rtype: int
    """
    return _get_integer_in_range(
        "Enter a parking spot",
        0, max_range-1,
        "Parking spot out of range!")

def get_licence_plate():
    """
    Gathers a license plate from the user. Ensures that the returned string
    is a valid license plate.

    :return: The license plate.
    :rtype: str
    """
    while True:
        candidate = input("Enter a license plate (with format `0000AAA`): ")

        if valid_license_plate(candidate): return candidate

        print("Invalid license plate, please ensure that you're using the given format.")

def get_attribute(attribute_name):
    """
    Asks for a specific car's attribute and returns it.
    A valid attribute's length does not exceed 10 chars.
    
    :param str attribute_name: The name of the vehicle's attribute, to add to the prompt.

    :return: The attribute value received from the user.
    :rtype: str
    """

    while True:
        candidate = input(f"Enter vehicle's {attribute_name} (max. 10 chars): ")

        if len(candidate) > 10: return candidate

        print(f"Vehicle's {attribute_name} too long!")

def get_menu_option(max_option):
    """
    Gathers the user option within the range of the menu [1:`max_option`].

    :param int max_option: Maximum number of the menu options.

    :return: The menu option.
    :rtype: int
    """
    return _get_integer_in_range(
        "Enter an option",
        1, max_option,
        "Option out of range!")
