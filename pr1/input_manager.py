"""
==================

This module is used to check whether the input given by
the user follows the right format indicated by the documentation

==================
"""

from string import digits, ascii_uppercase

def _get_integer_in_range(prompt, range_start, range_end, out_of_range_message):
    """
    Checks for user input to be between range indicated by `range_start` and `range_end` returning `out_of_range_message` if input is not valid


    :param str prompt: String indicating the prompt shown in terminal
    :param int range_start: Integer indicating the beginning of the range 
    :param int range_end: Integer indicating the end of the range
    :param str out_of_range_message: Message to be shown in case user input is out of range
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
    Checks for user input to be "Y", "N", or ""


    :param str prompt: Character indicating the prompt shown in terminal
    """
    options = ["Y", "N", ""] #Empty input is considered as a yes.
    while True:
        candidate = input(f"{prompt} [Y/n]: ").upper()
        if candidate in options: return candidate!="N"
        print("Invalid Option")

def get_valid_spot(max_range):
    """
    Checks if `user_input` is between 1 and maximum garage capacity.

    :param int max_range: Maximum garage capacity
    """
    return _get_integer_in_range(
        "Enter a parking spot",
        1, max_range,
        "Parking spot out of range!")

def _valid_license_plate(license):
    """
    Checks if `license` follows the right format indicated by the documentation.

    :param str license: String indicating the license to be checked
    """
    if len(license) != 7: return False

    for i in range(0, 4):
        if license[i] not in digits: return False
    
    for i in range(4, 7):
        if license[i] not in ascii_uppercase: return False

    return True


def get_licence_plate():
    """
    Checks if the license given by the user input follows the right format indicated by the documentation.

    """
    while True:
        candidate = input("Enter a license plate (with format `0000AAA`): ")

        if _valid_license_plate(candidate): return candidate

        print("Invalid license plate, please ensure that you're using the given format.")

def get_menu_option(max_option):
    """
    Checks if option given by user is within the range [1:`max_option`]

    :param int max_option: Integer indicating maximum of range
    """
    return _get_integer_in_range(
        "Enter an option",
        1, max_option,
        "Option out of range!")
