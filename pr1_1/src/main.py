from os import path
from sys import argv
import input_manager
from database import ParkingDatabase, DatabaseCorruptionError

PARKING_SIZE = 1000
PROJECT_ABS_PATH = path.dirname(path.abspath(__file__))
DB_FILE_PATH = f"{PROJECT_ABS_PATH}/spot_data.dat"

def fill_parking_spot(db):
    spot = None
    if input_manager.yes_or_no("Do you want to manually select the parking spot?"):
        spot = input_manager.get_valid_spot(PARKING_SIZE)

    license_plate = input_manager.get_licence_plate()
    
    result = db.insert_vehicle(license_plate, spot)

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
    license_plate = input_manager.get_licence_plate()
    
    result = db.remove_vehicle(license_plate)

    if result == 0: #Success
        print("Vehicle left the parking successfully!")
    elif result == 1: #Vehicle not found
        print("Failed leave parking: Vehicle not found in parking.")
    else:
        print("Failed leave parking: Unknown error.")

def check_parking_spot(db):
    spot = input_manager.get_valid_spot(PARKING_SIZE)

    result = db.check_spot(spot)

    if result == None:
        print("Parking spot empty.")
    else:
        print(f"Found vehicle with license plate {result} is in this spot.")

def list_empty_spots(db):
    spots = db.empty_spots()

    # To ensure user really wants a spamming input in their CLI
    if len(spots) < 30 or input_manager.yes_or_no(f"Display all {len(spots)} spots?"):
        spots_str = [str(spot) for spot in spots]
        print(f"Empty parking spots ({len(spots)}): {', '.join(spots_str)}.")

def find_vehicle(db):
    license_plate = input_manager.get_licence_plate()
    
    result = db.find_vehicle(license_plate)

    if result == None:
        print("This vehicle is not in the parking.")
    else:
        print(f"Found vehicle at parking spot {result}.")

MENU_OPTIONS_TEXT = [
    "Occupy a parking spot",
    "Leave parking",
    "Check parking spot availability",
    "List empty parking spots",
    "Find vehicle in the parking",
    "Exit application"
]

MENU_OPTIONS_CALLBACKS = [
    fill_parking_spot,
    leave_parking_spot,
    check_parking_spot,
    list_empty_spots,
    find_vehicle
]

def print_menu():
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
            print()

        parking_database.end()
