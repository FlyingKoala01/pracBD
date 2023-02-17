"""
==================

This module contains the class :class:`Garage`. It will be used to interact with the `places.dat` file.

==================
"""


GARAGE_SIZE = 10
FILENAME = "places.dat"

def occupy_spot(car_id, spot_number=None):
    """
    Fills a a parking spot with `car_id`. If `spot_number` is not given, it will fill the first empty spot found in `FILENAME`

    :param str car_id: String to indicate a car's license plate
    :param int spot_number: integer to indicate a specific parking position

    >>> initialize_file("places.dat", 10)
    >>> car_status("2310AMN")
    2310AMN NOT FOUND
    >>> occupy_spot("2310AMN", 2)
    >>> car_status("2310AMN")
    2 FULL 2310AMN

    """
    f = open(f'{FILENAME}', 'r+')
    f.seek(0)

    if spot_number != None:
        f.seek((7 * spot_number))
        f.write(car_id)

    else:    
        for i in range(GARAGE_SIZE):
            f.seek(7 * i)
            if f.read(7) == "XXXXXXX":
                f.seek(7 * i)
                f.write(car_id) 
                break
    
    f.close()


def car_status(car_id):
    """
    Returns the number of `car_id` parking slot

    :param str car_id: String to indicate the car's license plate

    >>> initialize_file("places.dat", 10)
    >>> car_status("2310AMN")
    2310AMN NOT FOUND
    >>> occupy_spot("2310AMN", 2)
    >>> car_status("2310AMN")
    2 FULL 2310AMN
    >>> car_status("2367ABC")
    2367ABC NOT FOUND

    """
    f = open(f'{FILENAME}', 'r+')
    f.seek(0)

    for i in range(GARAGE_SIZE):
        f.seek(7 * i)
        if  f.read(7) == (car_id):
            print(f'{i} FULL {car_id}')
            f.close()
            return (i)
    
    print(f'{car_id} NOT FOUND')
    f.close()
    return None

def leave_spot(car_id):
    """
    Deletes `car_id` from `FILENAME` and fills it with "XXXXXXX"

    :param str car_id: String indicating the car's license plate.

    >>> initialize_file("places.dat", 10)
    >>> occupy_spot("2310AMN", 2)
    >>> leave_spot("2310AMN")
    2 FULL 2310AMN
    >>> car_status("2310AMN")
    2310AMN NOT FOUND
    """
    spot_number = car_status(car_id)
    if  spot_number != None:
        occupy_spot("XXXXXXX", spot_number)
    return

def spot_status(spot_number):
    """
    Returns the spot status for a given spot number. If a car is parked, it will print the spot number with the car's license plate.
    If the spot is empty it will return the spot number and "XXXXXXX".

    :param int spot_number: Integer indicating a spot in the parking lot

    >>> initialize_file("places.dat", 10)
    >>> occupy_spot("2310AMN", 2)
    >>> car_status("2310AMN")
    2 FULL 2310AMN
    >>> spot_status(2)
    2 2310AMN
    """
    f = open(f'{FILENAME}', 'r')
    f.seek(7 * spot_number)
    spot_car = f.read(7) 
    if spot_car == "XXXXXXX":
        f.close()
        print(f'{spot_number} EMPTY')
    else:
        f.close()
        print(f'{spot_number} {spot_car}')

def list_spots():
    """
    Returns a list of the free spot numbers

    >>> initialize_file("places.dat", 10)
    >>> list_spots("placed.dat")
    0 EMPTY 
    1 EMPTY 
    2 EMPTY 
    3 EMPTY 
    4 EMPTY 
    5 EMPTY 
    6 EMPTY 
    7 EMPTY 
    8 EMPTY 
    9 EMPTY
    """
    f = open(f'{FILENAME}', 'r')
    free_list = []

    for i in range(GARAGE_SIZE):
        f.seek(7 * i)
        if  f.read(7) == ("XXXXXXX"):
            print(f'{i} EMPTY')
            free_list.append(i)
    f.close()
    return free_list



if __name__ == "__main__":
    print("STARTING")
    initialize_file("places.dat", 10)
    #list_spots()

    car_status("2310AMN")
    occupy_spot("2310AMN", 2)
    car_status("2310AMN")
    spot_status(2)

    # car_status("1234ABC")
    # occupy_spot("1234ABC")
    # car_status("1234ABC")

    # leave_spot("2310AMN")
    # leave_spot("1234ABC")
    # car_status("2310AMN")
    # car_status("1234ABC")
    