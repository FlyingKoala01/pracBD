"""
==================

This module manages user inputs. Every function in this module is intended to
be used to ensure that the other programs can forget about wrong inputs.

Doctests can't be provided in this module (except for one function) as it
uses builtin input function.

==================
"""

tables = ["EMPLOYEE", "JOB", "COMPANY", "MANAGER"]
columns = {
    "EMPLOYEE"  : ["id_employee", "street", "city"],
    "JOB"       : ["id_employee", "id_company", "salary"],
    "COMPANY"   : ["id_company", "city"],
    "MANAGER"   : ["id_employee", "id_employee_coordinatator"],
}

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

def get_attribute(table, attribute_name):
    """
    Asks for a specific table's attribute and returns it.
    A valid attribute's length does not exceed 10 chars.
    
    :param str table: The name of a specific table.
    :param str attribute_name: The name of the table's attribute, to add to the prompt.

    :return: The attribute value received from the user.
    :rtype: str
    """

    while True:
        candidate = input(f"Enter {table}'s {attribute_name} value (max. 10 chars): ")

        if len(candidate) <= 10: return candidate

        print(f"{table}'s {attribute_name} value is too long!")

def get_attributes(table):
    """
    Shows the user all the columns from a specific table, lets the user choose one and returns it.

    :param str table: String indicating a table's name.

    :return: The chosen column.
    :rtype: str
    """

    cols = (columns.get(table))
    print("Available Attributes:")
    print(*cols, sep="\n")
    while True:
        candidate = input("Choose a column from the options above: ")
        if candidate in cols: return candidate
        print("Invalid Option")

def get_tables():
    """
    Shows the user all the tables, lets the user choose one and returns it.

    :return: The chosen table.
    :rtype: str
    """
        
    print("Available Tables:")
    print(*tables, sep="\n")
    while True:
        candidate = input("Choose a table from the options above: ").upper()
        if candidate in tables: return candidate
        print("Invalid Option")

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
