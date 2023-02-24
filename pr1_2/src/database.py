"""
==================

The module will be used to interact with the `spot_data.dat` file.

In contains the `class.DatabaseCorruptionError` Exception, the class to
manage database connections and an auxiliary function to sort license plates.

==================

When running doctests, we wish to start with an empty parking place. That's
why we delete the db file in this doctest.

>>> _delete_db_if_exists("./spot_data.dat")
"""

from os import path, remove
import struct
from vehicle import valid_license_plate, Vehicle
from parking_spot import ParkingSpot

DB_RECORD_LENGTH = Vehicle.COLOR_MAX_LENGTH + Vehicle.BRAND_MAX_LENGTH + Vehicle.LICENSE_PLATE_LENGTH
STRUCT_FORMAT = f"{Vehicle.LICENSE_PLATE_LENGTH}s{Vehicle.COLOR_MAX_LENGTH}s{Vehicle.BRAND_MAX_LENGTH}s"
PLACEHOLDER_LICENSE_PLATE = "XXXXXXX"
PLACEHOLDER_VEHICLE = Vehicle(PLACEHOLDER_LICENSE_PLATE, "", "")

def _delete_db_if_exists(filename):
    try:
        remove(filename)
    except OSError:
        pass

class DatabaseCorruptionError(Exception):
    """
    This Exception is raised when there's an error while reading the database
    file at startup.

    >>> raise DatabaseCorruptionError('test')
    Traceback (most recent call last):
     ...
    database.DatabaseCorruptionError: test
    """
    pass

class ParkingDatabase():
    """
    This class represents a Database storing information about a garage.
    Specifically, it will store license plates.

    :param str db_file: The database file name
    :param int parking_size: How many cars will fit in the parking
    :param bool init_if_not_exist: Create a database file if not found.

    >>> db = ParkingDatabase("./spot_data.dat", 1000, True)
    >>> car = Vehicle('7865GZH', 'pink', 'BMW')
    >>> db.insert_vehicle(car, 987)
    0
    >>> db.check_spot(987)
    Vehicle <License plate: 7865GZH, Brand: BMW, Color: pink>
    >>> db.remove_vehicle("7865GZH")
    0
    >>> db.check_spot(987)
    >>> db.remove_vehicle("7865GZH")
    1
    """

    def __init__(self, db_file, parking_size, init_if_not_exist=False):
        """
        Initialize the instance.

        :param str db_file: The database file name
        :param int parking_size: How many cars will fit in the parking
        :param bool init_if_not_exist: Create a database file if not found.
        
        >>> db = ParkingDatabase("./spot_data.dat", 1000, True)
        """
        self.parking_size = parking_size
        self.db = self.__open_db_file(db_file, init_if_not_exist)
        if not self._is_db_valid(): raise DatabaseCorruptionError

    def end(self):
        """
        Closes the database file, to prevent corruption. It must be done
        before the program finishes. Once done, the database isn't accessible.

        >>> db = ParkingDatabase("./spot_data.dat", 1000, True)
        >>> db.end()
        >>> car = Vehicle('7865GZH', 'pink', 'BMW')
        >>> db.insert_vehicle(car)
        Traceback (most recent call last):
         ...
        ValueError: seek of closed file
        """

        self.db.close()

    def __open_db_file(self, file, init_if_not_exist):
        """
        Creates or opens the `file`. In case the file does not exist,
        it is created and thus also the db is initialized.

        :param str file: The file name
        :param bool init_if_not_exist: If the `file` exists or not

        :return: The file instance of the db file.
        :rtype: file
        """

        if not init_if_not_exist or path.exists(file):
            return open(file, 'rb+')
        else:
            file = open(file, 'wb+')
            self.__init_db_file(file)
            return file

    def __init_db_file(self, file):
        """
        Initializes the database in `file`. Fills the spaces with "XXXXXXX".

        :param str file: String indicating the file name
        """
       
        # We suppose that the file has been just opened and was empty.
        placeholder_pack = struct.pack(STRUCT_FORMAT, *PLACEHOLDER_VEHICLE.encode())
        file.write(placeholder_pack * self.parking_size)

    def __load_vehicle(self, spot=None):
        """
        Used to read a record from DB in the spot defined by the parameter `spot`.
        Returns a :class:`Vehicle`

        :param int spot: Indicating a specific parking space 

        :returns: The vehicle found. WARNING: The vehicle may be a PLACEHOLDER_EMPTY. Do not use this function directly.
        :rtype: vehicle.Vehicle
        """

        if spot != None: self.db.seek(spot*DB_RECORD_LENGTH)

        current = struct.unpack(STRUCT_FORMAT, self.db.read(DB_RECORD_LENGTH))
        return Vehicle(*current)
    
    def __parking_spots_loop(self):
        """
        This function makes all the loops in this file more readable, by
        compressing all the hard-to-understand stuff here.

        It can be used inside a for loop, and will yield all vehicles from
        the database.
        """
        self.db.seek(0)
        for i in range(self.parking_size):
            current = struct.unpack(STRUCT_FORMAT, self.db.read(DB_RECORD_LENGTH))
            vehicle = Vehicle(*current)
            parking_spot = ParkingSpot(i, vehicle if vehicle.license_plate != PLACEHOLDER_LICENSE_PLATE else None)
            yield parking_spot

    def _is_db_valid(self):
        """
        Checks all the license plates in the db.
        If any plate is not well formatted, it returns `False`.

        :return: Wether the db is well formatted.
        :rtype: bool
        """
        # All errors due to reading the file will be considered as corruption.
        try:
            for spot in self.__parking_spots_loop():
                if spot.occupied() and not valid_license_plate(spot.vehicle.license_plate):
                    return False
        except:
            return False

        # Checking that we have reached the end of file.
        return self.db.read(1).decode() == ""

    def _first_empty_spot_number(self):
        """
        Function to find the first empty spot in the db indicated by "XXXXXXX".

        :return: The number of the first empty spot or None if parking full.
        :rtype: int
        """
        for spot in self.__parking_spots_loop():
            if not spot.occupied():
                return spot.number

        return None

    def insert_vehicle(self, vehicle, spot=None):
        """
        Checks if for a given `license_plate` there is a spot for the car to park. If `spot` is specified, it will 
        look specifically for that spot, otherwise, it will park in the first free space.

        Output codes:
        - 0: Success.
        - 1: Specific spot full.
        - 2: Parking full.
        - 3: License plate already in parking.

        :param vehicle.Vehicle vehicle: The vehicle to insert in the parking spot.
        :param int spot: Indicating a specific parking space.

        :return: The output code specifying the results stated above.
        :rtype: int

        >>> db = ParkingDatabase("./spot_data.dat", 1000, True)
        >>> car = Vehicle('7865GTH', 'pink', 'BMW')
        >>> db.insert_vehicle(car, 565)
        0
        >>> db.check_spot(565)
        Vehicle <License plate: 7865GTH, Brand: BMW, Color: pink>
        >>> db.remove_vehicle("7865GTH")
        0
        >>> db.check_spot(565)
        >>> db.remove_vehicle("7865GTH")
        1
        """
        if spot == None:
            spot = self._first_empty_spot_number()
            # If still empty, parking full (Error 2)
            if spot == None: return 2

        else:
            # Checking if given spot is available
            temp_vehicle = self.__load_vehicle(spot)
            # Spot occupied (Error 1)
            if temp_vehicle.license_plate != PLACEHOLDER_LICENSE_PLATE: return 1

        # Check if car is already in parking (Error 3)
        if self.find_vehicle(vehicle.license_plate) != None: return 3

        self.db.seek(DB_RECORD_LENGTH*spot)
        self.db.write(struct.pack(STRUCT_FORMAT, *vehicle.encode()))
        return 0

    def remove_vehicle(self, license_plate):
        """
        Function used to remove a specific car with `license_plate`.

        Output codes:
        - 0: Success.
        - 1: Car not found in parking.

        :param str license_plate: String to indicate car's plate.

        :return: The output code specified above.
        :rtype: int

        >>> db = ParkingDatabase("./spot_data.dat", 1000, True)
        >>> car = Vehicle('7865FTH', 'pink', 'BMW')
        >>> db.insert_vehicle(car, 566)
        0
        >>> db.check_spot(566)
        Vehicle <License plate: 7865FTH, Brand: BMW, Color: pink>
        >>> db.remove_vehicle("7865FTH")
        0
        >>> db.check_spot(566)
        >>> db.remove_vehicle("7865FTH")
        1
        """
        spot = self.find_vehicle(license_plate)
        if spot == None: return 1

        self.db.seek(DB_RECORD_LENGTH*spot.number)
        self.db.write(struct.pack(STRUCT_FORMAT, *PLACEHOLDER_VEHICLE.encode()))
        return 0

    def check_spot(self, spot_number):
        """
        Used to check if for a specific spot `spot_number`, there's a vehicle.

        :param int spot_number: Indicating a specific parking space 

        :return: The vehicle or None if cars aren't found.
        :rtype: vehicle.Vehicle
        
        >>> db = ParkingDatabase("./spot_data.dat", 1000, True)
        >>> car = Vehicle('9878RTY', 'pink', 'BMW')
        >>> db.insert_vehicle(car, 789)
        0
        >>> db.check_spot(789)
        Vehicle <License plate: 9878RTY, Brand: BMW, Color: pink>
        >>> db.remove_vehicle("9878RTY")
        0
        """
        self.db.seek(DB_RECORD_LENGTH*spot_number)
        vehicle = self.__load_vehicle(spot_number)

        return None if vehicle.license_plate == PLACEHOLDER_LICENSE_PLATE else vehicle

    def empty_spots(self):
        """
        Returns a list of the empty spots in the db.

        :return: The list of empty spots.
        :rtype: list

        >>> db = ParkingDatabase("./spot_data.dat", 1000, True)
        >>> a = len(db.empty_spots())
        >>> car = Vehicle('1264ABC', 'pink', 'BMW')
        >>> db.insert_vehicle(car)
        0
        >>> b = len(db.empty_spots())
        >>> a == b+1
        True
        >>> db.remove_vehicle("1264ABC")
        0
        """
        candidates = []

        for spot in self.__parking_spots_loop():
            if not spot.occupied():
                candidates.append(spot)

        return candidates

    def find_vehicle(self, license_plate: str) -> (ParkingSpot or None):
        """
        Searches for the parking space number for a given car with `license_plate`

        :param str license_plate: String to indicate car's plate

        :return: The vehicle parking spot.
        :rtype: parking_spot.ParkingSpot

        >>> db = ParkingDatabase("./spot_data.dat", 1000, True)
        >>> car = Vehicle('1294ABC', 'pink', 'BMW')
        >>> db.insert_vehicle(car)
        0
        >>> db.find_vehicle("1294ABC")
        Spot 0: Vehicle <License plate: 1294ABC, Brand: BMW, Color: pink>
        >>> db.remove_vehicle("1294ABC")
        0
        """
        for spot in self.__parking_spots_loop():
            if spot.occupied() and spot.vehicle.license_plate == license_plate:
                return spot
        
        return None

    def find_vehicles_with_color(self, color: str) -> list:
        """
        Returns a list of spots where the vehicle has the specified color.

        :param str color: The color of the vehicle.

        :return: The list of :class:`parking_spot.ParkingSpot`.
        :rtype: list

        >>> db = ParkingDatabase("./spot_data.dat", 1000, True)
        >>> car = Vehicle('1214ABC', 'pink', 'BMW')
        >>> list1 = db.find_vehicles_with_color('pink')
        >>> db.insert_vehicle(car)
        0
        >>> list2 = db.find_vehicles_with_color('pink')
        >>> len(list2) == len(list1)+1
        True
        >>> cars1 = [spot.vehicle.license_plate for spot in list1]
        >>> cars2 = [spot.vehicle.license_plate for spot in list2]
        >>> car.license_plate in cars2 and car.license_plate not in cars1
        True
        """
        candidates = []

        for spot in self.__parking_spots_loop():
            if spot.occupied() and spot.vehicle.color == color:
                candidates.append(spot)

        return candidates

    def find_vehicles_with_brand(self, brand: str) -> list:
        """
        Returns a list of spots where the vehicle has the specified brand.

        :param str brand: The brand of the vehicle.

        :return: The list of :class:`parking_spot.ParkingSpot`.
        :rtype: list

        >>> db = ParkingDatabase("./spot_data.dat", 1000, True)
        >>> car = Vehicle('1204ABC', 'pink', 'BMW')
        >>> list1 = db.find_vehicles_with_brand('BMW')
        >>> db.insert_vehicle(car)
        0
        >>> list2 = db.find_vehicles_with_brand('BMW')
        >>> len(list2) == len(list1)+1
        True
        >>> cars1 = [spot.vehicle.license_plate for spot in list1]
        >>> cars2 = [spot.vehicle.license_plate for spot in list2]
        >>> car.license_plate in cars2 and car.license_plate not in cars1
        True
        """
        candidates = []

        for spot in self.__parking_spots_loop():
            if spot.occupied() and spot.vehicle.brand == brand:
                candidates.append(spot)

        return candidates
