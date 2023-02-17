from os import path
import input_manager
from database import ParkingDatabase, DatabaseCorruptionError, DatabaseNotFoundError

PARKING_SIZE = 1000
PROJECT_ABS_PATH = path.dirname(path.abspath(__file__))
DB_FILE_PATH = PROJECT_ABS_PATH + "spot_data.dat"

parking_database = None

def fill_parking_spot():
    spot = None
    if input_manager.yes_or_no("Do you want to manually select the parking spot?"):
        spot = input_manager.get_valid_spot(PARKING_SIZE)

    license_plate = input_manager.get_licence_plate()
    
    result = parking_database.insert_vehicle(license_plate, spot)

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

def leave_parking_spot():
    license_plate = input_manager.get_licence_plate()
    
    result = parking_database.remove_vehicle(license_plate)

    if result == 0: #Success
        print("Vehicle left the parking successfully!")
    elif result == 1: #Vehicle not found
        print("Failed leave parking: Vehicle not found in parking.")
    else:
        print("Failed leave parking: Unknown error.")

def check_parking_spot():
    spot = input_manager.get_valid_spot(PARKING_SIZE)

    result = parking_database.check_spot(spot)

    if result == None:
        print("Parking spot empty.")
    else:
        print(f"Found vehicle with license plate {result} is in this spot.")

def list_empty_spots():
    spots = parking_database.empty_spots()

    # To ensure user really wants a spamming input in their CLI
    if len(spots) < 30 or input_manager.yes_or_no(f"Display all {len(spots)} spots?"):
        print(f"Empty parking spots ({len(spots)}): {', '.join(spots)}.")

def find_vehicle():
    license_plate = input_manager.get_licence_plate()
    
    result = parking_database.find_vehicle(license_plate)

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
    for i in range(MENU_OPTIONS_TEXT):
        print(f" {i}: {MENU_OPTIONS_TEXT[i]}")
    print()

if __name__=="__main__":
    try:
        parking_database = ParkingDatabase(DB_FILE_PATH)
    except DatabaseCorruptionError:
        print("Database file is corrupt! Please check the format and try again.")
    except DatabaseNotFoundError:
        print("Database file not found! Run this program with `-c` to create it if it doesn't exist.")
    else:

        while True:
            print_menu()
            option = input_manager.get_menu_option(len(MENU_OPTIONS_TEXT))

            if option == len(MENU_OPTIONS_CALLBACKS): # User wants to exit
                print("Thanks for using this application!")
                break

            print()
            MENU_OPTIONS_CALLBACKS[option]()
            print()
