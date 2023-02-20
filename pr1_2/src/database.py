"""
==================

The module will be used to interact with the `spot_data.dat` file. It contains the following classes:


- The parent class :class:`ParkingDatabase`. It is used to interact with the db.

- The exception :class:`DatabaseCorruptionError`, that is raised when the db file is corrupted.

==================
"""
from os import path
import struct
from vehicle import valid_license_plate, Vehicle
from parking_spot import ParkingSpot

DB_RECORD_LENGTH = Vehicle.COLOR_MAX_LENGTH + Vehicle.BRAND_MAX_LENGTH + Vehicle.LICENSE_PLATE_LENGTH
STRUCT_FORMAT = f"{Vehicle.LICENSE_PLATE_LENGTH}s{Vehicle.COLOR_MAX_LENGTH}s{Vehicle.BRAND_MAX_LENGTH}s"
PLACEHOLDER_LICENSE_PLATE = "XXXXXXX"
PLACEHOLDER_VEHICLE = Vehicle(PLACEHOLDER_LICENSE_PLATE, "", "")

class DatabaseCorruptionError(Exception):
    """

    >>> raise DatabaseCorruptionError('test')
    Traceback (most recent call last):
     ...
    database.DatabaseCorruptionError: test
    """
    pass

class ParkingDatabase():
    def __init__(self, db_file, parking_size, init_if_not_exist=False):
        """
        Initialize the `db_file` with `parking_size` car-spaces.

        :param str db_file: String indicating the database file name
        :param int parking_size: Integer indicating how many cars will fit in the parking
        """
        self.parking_size = parking_size
        self.db = self.__open_db_file(db_file, init_if_not_exist)
        if not self._is_db_valid(): raise DatabaseCorruptionError

    def end(self):
        """
        Closes the database file. Used when user exists the menu.
        """
        self.db.close()

    def __open_db_file(self, file, init_if_not_exist):
        """
        Creates or opens the `file`. In case the file does not exist, it is created and thus also the db is initialized.

        :param str file: String indicating the file name
        :param bool init_if_not_exist: Boolean value indicating if the `file` exists or not
        """
        if not init_if_not_exist or path.exists(file):
            return open(file, 'rb+')
        else:
            file = open(file, 'wb+')
            self.__init_db_file(file)
            return file

    def __init_db_file(self, file):
        """
        Initializes the database in `file`. Fills the car spaces with "XXXXXXXXXXXXXXXXXXXXXXXXXXX".

        :param str file: String indicating the file name
        """
        # We suppose that the file has been just opened and was empty.
        placeholder_pack = struct.pack(STRUCT_FORMAT, *PLACEHOLDER_VEHICLE.encode())
        file.write(placeholder_pack * self.parking_size)

    def __load_vehicle(self, spot=None):

        if spot != None: self.db.seek(spot*DB_RECORD_LENGTH)

        current = struct.unpack(STRUCT_FORMAT, self.db.read(DB_RECORD_LENGTH))
        return Vehicle(*current)
    
    def __parking_spots_loop(self):
        self.db.seek(0)
        for i in range(self.parking_size):
            current = struct.unpack(STRUCT_FORMAT, self.db.read(DB_RECORD_LENGTH))
            vehicle = Vehicle(*current)
            parking_spot = ParkingSpot(i, vehicle if vehicle.license_plate != PLACEHOLDER_LICENSE_PLATE else None)
            yield parking_spot

    def _is_db_valid(self):
        """
        Checks all the license plates in the db. If any plate is not well formatted, it returns `False`.
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
        Function to find the first empty spot in the db indicated by PLACEHOLDER_LICENSE_PLATE. Returns the spot number if one is found.
        """
        for spot in self.__parking_spots_loop():
            if not spot.occupied():
                return spot.number

        return None

    def insert_vehicle(self, vehicle, spot=None):
        """
        Checks if for a given `license_plate` there is a spot for the car to park. If `spot` is specified, it will 
        look specifically for that spot, otherwise, it will park in the first free space.

        :param str license_plate: String to indicate car's plate
        :param int spot: Indicating a specific parking space 
        """
        if spot == None:
            spot = self._first_empty_spot_number()
            # If still empty, parking full (Error 2)
            if spot == None: return 2

        else:
            # Checking if given spot is available
            vehicle = self.__load_vehicle(spot)
            # Spot occupied (Error 1)
            if vehicle.license_plate != PLACEHOLDER_LICENSE_PLATE: return 1

        # Check if car is already in parking (Error 3)
        if self.find_vehicle(vehicle.license_plate) != None: return 3

        self.db.seek(DB_RECORD_LENGTH*spot)
        self.db.write(struct.pack(STRUCT_FORMAT, *vehicle.encode()))
        return 0

    def remove_vehicle(self, license_plate):
        """
        Function used to remove a specific car with `license_plate`.

        :param str license_plate: String to indicate car's plate
        """
        spot = self.find_vehicle(license_plate)
        if spot == None: return 1

        self.db.seek(DB_RECORD_LENGTH*spot)
        self.db.write(struct.pack(STRUCT_FORMAT, *PLACEHOLDER_VEHICLE.encode()))
        return 0

    def check_spot(self, spot_number):
        """
        Used to check if for a specific spot `spot_number`, there is a car parked or not

        :param int spot_number: Indicating a specific parking space 
        """
        self.db.seek(DB_RECORD_LENGTH*spot_number)
        vehicle = self.__load_vehicle(spot_number)

        return None if vehicle.license_plate == PLACEHOLDER_LICENSE_PLATE else vehicle

    def empty_spots(self):
        """
        Returns a list of the empty spots in the db.
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
        """
        for spot in self.__parking_spots_loop():
            if spot.occupied() and spot.vehicle.license_plate == license_plate:
                return spot
        
        return None

    def find_vehicles_with_color(self, color: str) -> list:
        candidates = []

        for spot in self.__parking_spots_loop():
            if spot.occupied() and spot.vehicle.color == color:
                candidates.append(spot)

        return candidates

    def find_vehicles_with_brand(self, brand: str) -> list:
        candidates = []

        for spot in self.__parking_spots_loop():
            if spot.occupied() and spot.vehicle.brand == brand:
                candidates.append(spot)

        return candidates
