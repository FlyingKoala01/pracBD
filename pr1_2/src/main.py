"""
==================

This is the main module. It will interact with all of the other modules and
with the user. 

The functions are just an analogy of the options in the menu. This means
that executing any function is like clicking on that menu option.

==================
"""

from os import path
from sys import argv
from time import sleep

import input_manager
from database import ParkingDatabase, DatabaseCorruptionError
from vehicle import Vehicle

PARKING_SIZE = 1000
PROJECT_ABS_PATH = path.dirname(path.abspath(__file__))
DB_FILE_PATH = f"{PROJECT_ABS_PATH}/spot_data.dat"

def fill_parking_spot(db):
    """
    Used to fill a specific, if required, parking slot with a given
    license plate, brand and color.

    The spot can be introduced or the user can choose to park on the first
    available spot.

    This function gets the user's input, and returns a nice output depending
    on the output (or error) code.

    :param `database.ParkingDatabase` db: The opened database instance.
    """
    spot = None
    if input_manager.yes_or_no("Do you want to manually select the parking spot?"):
        spot = input_manager.get_valid_spot(PARKING_SIZE)

    license_plate = input_manager.get_licence_plate()
    color = input_manager.get_attribute("color")
    brand = input_manager.get_attribute("brand")

    vehicle = Vehicle(license_plate, color, brand)
    result = db.insert_vehicle(vehicle, spot)

    print()

    if result == 0: #Success
        print("Parking spot occupied successfully!")
    elif result == 1: #Spot occupied
        print("Failed to occupy parking spot: Parking spot occupied.")
    elif result == 2: #Parking full
        print("Failed to occupy parking spot: Parking full!")
    elif result == 3: #Vehicle already inside
        print("Failed to occupy parking spot: Vehicle is already in the parking!")
    else:
        print("Failed to occupy parking spot: Unknown error.")

def leave_parking_spot(db):
    """
    Used to delete a car from a parking slot given a license plate. This
    function handles user's input and outputs a nice message depending on the
    database's return code.

    :param `database.ParkingDatabase` db: The opened database instance.
    """
    license_plate = input_manager.get_licence_plate()
    result = db.remove_vehicle(license_plate)

    print()

    if result == 0: #Success
        print("Vehicle left the parking successfully!")
    elif result == 1: #Vehicle not found
        print("Failed leave parking: Vehicle not found in parking.")
    else:
        print("Failed leave parking: Unknown error.")

def check_parking_spot(db):
    """
    Checks the parking slot for a specific vehicle in database.

    The function gets user's input and outputs a different message wether
    the spot is empty or occupied.

    :param `database.ParkingDatabase` db: The opened database instance.
    """
    spot = input_manager.get_valid_spot(PARKING_SIZE)
    result = db.check_spot(spot)

    print()

    if result == None:
        print("Parking spot empty.")
    else:
        print(f"Vehicle found in spot {spot}: {result}")

def list_empty_spots(db):
    """
    Returns a list indicating all the free spaces in the database.

    If the length of the list exceeds 30 elements, an extra prompt is required
    in order to ensure a spamming output.

    :param `database.ParkingDatabase` db: The opened database instance.
    """
    spots = db.empty_spots()

    if len(spots) == 0:
        print("Parking full! There aren't any empty spots.")
        return

    # To ensure user really wants a spamming input in their CLI
    if len(spots) < 30 or input_manager.yes_or_no(f"Display all {len(spots)} spots?"):
        spots_str = [str(spot.number) for spot in spots]
        print(f"Empty parking spots ({len(spots)}): {', '.join(spots_str)}.")

def find_vehicle(db):
    """
    Find the parking slot for a specific license plate in the database.

    There are different output messages wether the vehicle is found or not.

    :param `database.ParkingDatabase` db: The opened database instance.
    """
    license_plate = input_manager.get_licence_plate()
    spot = db.find_vehicle(license_plate)

    print()

    if spot == None:
        print("This vehicle is not in the parking.")
    else:
        print(f"Found at {spot}.")

def find_vehicle_color(db):
    """
    Returns a list with all the vehicles of a specific color.

    If the length of the list exceeds 10 elements, an extra prompt is required
    in order to ensure a spamming output.

    :param `database.ParkingDatabase` db: The opened database instance.
    """
    color = input_manager.get_attribute("color")
    spots = db.find_vehicles_with_brand(color)

    print()

    if len(spots) == 0:
        print(f'No {color} vehicles found in the parking.')
    elif len(spots) < 10 or input_manager.yes_or_no(f"Display all {len(spots)} vehicles?"):
        print(f"Vehicles with [color == '{color}']:")
        for spot in spots:
            print(f'- {spot}.')

def find_vehicle_brand(db):
    """
    Returns a list with all the vehicles of a specific brand.

    If the length of the list exceeds 10 elements, an extra prompt is required
    in order to ensure a spamming output.

    :param `database.ParkingDatabase` db: The opened database instance.
    """
    brand = input_manager.get_attribute("brand")
    spots = db.find_vehicles_with_brand(brand)

    print()

    if len(spots) == 0:
        print(f'No {brand} vehicles found in the parking.')
    elif len(spots) < 10 or input_manager.yes_or_no(f"Display all {len(spots)} vehicles?"):
        print(f"Vehicles with [brand == '{brand}']:")
        for spot in spots:
            print(f'- {spot}.')


MENU_OPTIONS_TEXT = [
    "Occupy a parking spot",
    "Leave parking",
    "Check parking spot availability",
    "List empty parking spots",
    "Find vehicle in the parking",
    "Find vehicle with a specific color in the parking",
    "Find vehicle of specific brand in the parking",
    "Exit application"
]

MENU_OPTIONS_CALLBACKS = [
    fill_parking_spot,
    leave_parking_spot,
    check_parking_spot,
    list_empty_spots,
    find_vehicle,
    find_vehicle_color,
    find_vehicle_brand
]

def print_menu():
    """
    Prints the user menu. In order to make this program easy-to-scale,
    the options are defined in a list in this module.

    This is the only function of this module that doesn't gather user input,
    so we can introduce a doctest.

    >>> print_menu()
    ====================
    PARKING MANAGER MENU
    ====================
    <BLANKLINE>
    Options:
     1: Occupy a parking spot
     2: Leave parking
     3: Check parking spot availability
     4: List empty parking spots
     5: Find vehicle in the parking
     6: Find vehicle with a specific color in the parking
     7: Find vehicle of specific brand in the parking
     8: Exit application
    <BLANKLINE>
    """
    print("="*20)
    print("PARKING MANAGER MENU")
    print("="*20 + "\n")
    print("Options:")
    for i in range(len(MENU_OPTIONS_TEXT)):
        print(f" {i+1}: {MENU_OPTIONS_TEXT[i]}")
    print()

if __name__=="__main__":
    init_if_not_exist = len(argv) == 2 and argv[1] == '-c'
    try:
        parking_database = ParkingDatabase(DB_FILE_PATH, PARKING_SIZE, init_if_not_exist=init_if_not_exist)
    except DatabaseCorruptionError:
        print("Database file is corrupt! Please check the format and try again.")
    except FileNotFoundError:
        print("Database file not found! Run this program with `-c` to create it if it doesn't exist.")
    else:

        while True:
            print_menu()
            option = input_manager.get_menu_option(len(MENU_OPTIONS_TEXT))

            if option == len(MENU_OPTIONS_TEXT): # User wants to exit
                print("Thanks for using this application!")
                break

            print()
            MENU_OPTIONS_CALLBACKS[option-1](parking_database)
            # We wait 1 sec in order to let the user read the result.
            sleep(1)
            print()

        parking_database.end()
