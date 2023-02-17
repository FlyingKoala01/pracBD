"""
==================

This module contains the class :class:`Garage`. It will be used to interact with the `places.dat` file.

==================
"""


GARAGE_SIZE = 10
FILENAME = "places.dat"

def initialize_file(filename, garage_size=None):
    """
    Initializes a `filename` file and fill it with `GARAGE_SIZE` lines of "XXXXXXX".

    :param str filename: Filename indicating the file with the garage information.
    :param int garage_size: Integer to indicat how many gars are present in the parking lot 

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

    if garage_size != None: GARAGE_SIZE = garage_size
    FILENAME = filename

    f = open(f'{FILENAME}', "w")
    for i in range(GARAGE_SIZE):
        f.write("XXXXXXX")
    f.close()

def occupy_spot(car_id, spot_number=None):
    """
    Fills a line with a car_id
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
    Returns the number of the car_id's parking slot
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
    Deletes car_id from filename and fills it with "XXXXXXX"
    """
    spot_number = car_status(FILENAME, car_id)
    if  spot_number != None:
        occupy_spot(FILENAME, "XXXXXXX", spot_number)
    return

def spot_status(spot_number):
    """
    Returns the spot status for a given spot number
    """
    f = open(f'{FILENAME}', 'r')
    spot_car = f.read(7 * spot_number) 
    if spot_car == "XXXXXXX":
        f.close()
        return f'{spot_number} EMPTY'
    else:
        f.close()
        return f'{spot_number} {spot_car}'

def list_spots():
    """
    Returns a list of the free spot numbers
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
    list_spots("places.dat")

    #car_status("places.dat", "2310AMN")
    #occupy_spot("places.dat", "2310AMN", 2)
    #list_spots("places.dat")
    #car_status("places.dat", "2310AMN")

    #car_status("places.dat", "1234ABC")
    #occupy_spot("places.dat", "1234ABC")
    #car_status("places.dat", "1234ABC")

    #leave_spot("places.dat", "2310AMN")
    #leave_spot("places.dat", "1234ABC")
    #car_status("places.dat", "2310AMN")
    #car_status("places.dat", "1234ABC")
    