"""
==================

This module manages user inputs. Every function in this module is intended to
be used to ensure that the other programs can forget about wrong inputs.

Doctests can't be provided in this module (except for one function) as it
uses builtin input function.

==================
"""

import re

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

def get_attribute(table, attribute_name):
    """
    Asks for a specific table's attribute and returns it.
    A valid attribute's length does not exceed 10 chars.
    
    :param str table: The name of a specific table.
    :param str attribute_name: The name of the table's attribute, to add to the prompt.

    :return: The attribute value received from the user.
    :rtype: str
    """

    attribute_pattern = r"^(id(_\w{1,8})?)|\bsalary$"

    while True:
        candidate = input(f"Enter {table}'s {attribute_name}: ")

        if re.match(attribute_pattern, attribute_name):
            if candidate.isdigit(): return int(candidate)
        else:
            if len(candidate) > 10: print(f"{table}'s {attribute_name} is too long!")
            else: return candidate

def get_new_city():
    """
    Function used to check how many employees work in a specific city.

    :return: The specified city's name
    :rtype: str
    """
    while True:
        candidate = input("What city would you like to check? ")
        
        if not(candidate.isalpha()): print("Invalid city parameter. Use letters only") 
        else: return (candidate)

def get_new_salary():
    """
    Function used to get the percentage value from the user.

    :return: The percentage value
    :rtype: int
    """
    while True:
        candidate = input("By what factor (%) would you like to increase Managers' salary? ")
        
        if not(candidate.isdigit()): print("Invalid salary parameter. Use numbers only") 
        else: return int(candidate)/100

def asc_or_desc():
    """
    Function to ensure user only inputs two options "asc" or "desc". 
    This function is particularly important considering how the query 
    where the result of this function will be used as it could potentially lead to SQLi.
    
    :return: The specified order "ASC" or "DESC"
    :rtype: str
    """
    
    while True:
        candidate = input("What order would you like to order by the employees salary? [ASC/DESC] ")
        
        if candidate.lower() != "asc" and candidate.lower() != "desc": print("Invalid order parameter. Select ASC or DESC only") 
        else: return candidate

def get_attributes(table):
    """
    Shows the user all the columns from a specific table, lets the user choose one and returns it.

    :param str table: String indicating a table's name.

    :return: The chosen column.
    :rtype: str
    """

    cols = columns.get(table)
    print("Available Attributes:")
    for i, col in enumerate(cols, 1):
        print(f"{i}. {col}")
    print(f"{i+1}. EXIT")
    while True:
        candidate = input("Choose a column from the options above: ")
        if candidate.isdigit():
            idx = int(candidate)
            if idx >= 1 and idx <= len(cols):
                return cols[idx-1]
            elif idx == (i+1):
                return
        elif candidate in cols:
            return candidate
        elif candidate == i or candidate == "EXIT":
            return 
        print("Invalid Option")

def get_tables():
    """
    Shows the user all the tables, lets the user choose one and returns it.

    :return: The chosen table.
    :rtype: str
    """
        
    print("Available Tables:")
    for i, table in enumerate(tables, 1):
        print(f"{i}. {table}")
    print(f"{i+1}. EXIT")
    while True:
        candidate = input("Choose a table from the options above: ")
        if candidate.isdigit():
            idx = int(candidate)
            if idx >= 1 and idx <= len(tables):
                return tables[idx-1]
            elif idx == (i+1):
                return
        elif candidate in tables:
            return candidate
        elif candidate == "EXIT":
            return 
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
