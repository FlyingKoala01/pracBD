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
        placeholder_pack = struct.pack(STRUCT_FORMAT, PLACEHOLDER_VEHICLE.encode())
        file.write(placeholder_pack * self.parking_size)

    def _is_db_valid(self):
        """
        Checks all the license plates in the db. If any plate is not well formatted, it returns `False`.
        """

        self.db.seek(0)

        for _ in range(self.parking_size):
            [license_plate, _, _] = struct.unpack(STRUCT_FORMAT, self.db.read(DB_RECORD_LENGTH))
            if license_plate.decode() != PLACEHOLDER_LICENSE_PLATE and not valid_license_plate(license_plate.decode()):
                return False

        # Checking that we have reached the end of file.
        return self.db.read(1).decode() == ""

    def _first_empty_spot(self):
        """
        Function to find the first empty spot in the db indicated by PLACEHOLDER_LICENSE_PLATE. Returns the spot number if one is found.
        """
        self.db.seek(0)

        for i in range(self.parking_size):
            [license_plate, _, _] = struct.unpack(STRUCT_FORMAT, self.db.read(DB_RECORD_LENGTH))
            if license_plate.decode() == PLACEHOLDER_LICENSE_PLATE:
                return i

        return None

    def insert_vehicle(self, vehicle, spot=None):
        """
        Checks if for a given `license_plate` there is a spot for the car to park. If `spot` is specified, it will 
        look specifically for that spot, otherwise, it will park in the first free space.

        :param str license_plate: String to indicate car's plate
        :param int spot: Indicating a specific parking space 
        """
        if spot == None:
            spot = self._first_empty_spot()
            # If still empty, parking full (Error 2)
            if spot == None: return 2

        else:
            # Checking if given spot is available
            self.db.seek(DB_RECORD_LENGTH*spot)
            # Spot occupied (Error 1)
            [temp_lp, _, _] = struct.unpack(STRUCT_FORMAT, self.db.read(DB_RECORD_LENGTH))
            if temp_lp.decode() != PLACEHOLDER_LICENSE_PLATE: return 1

        # Check if car is already in parking (Error 3)
        if self.find_vehicle(vehicle.license_plate) != None: return 3

        self.db.seek(DB_RECORD_LENGTH*spot)
        self.db.write(struct.pack(STRUCT_FORMAT, vehicle.encode()))
        return 0

    def remove_vehicle(self, license_plate):
        """
        Function used to remove a specific car with `license_plate`.

        :param str license_plate: String to indicate car's plate
        """
        spot = self.find_vehicle(license_plate)
        if spot == None: return 1

        self.db.seek(DB_RECORD_LENGTH*spot)
        car_pack = struct.pack(STRUCT_FORMAT, PLACEHOLDER_VEHICLE.encode())
        self.db.write(car_pack * self.parking_size)

        return 0

    def check_spot(self, spot_number):
        """
        Used to check if for a specific spot `spot_number`, there is a car parked or not

        :param int spot_number: Indicating a specific parking space 
        """
        self.db.seek(DB_RECORD_LENGTH*spot_number)
        [lp, color, brand] = struct.unpack(STRUCT_FORMAT, self.db.read(DB_RECORD_LENGTH) )

        return None if lp.decode() == PLACEHOLDER_LICENSE_PLATE else Vehicle(lp, color, brand)

    def empty_spots(self):
        """
        Returns a list of the empty spots in the db.
        """
        free_spots = []
        self.db.seek(0)

        for i in range(self.parking_size):
            [license_plate, _, _] = struct.unpack(STRUCT_FORMAT, self.db.read(DB_RECORD_LENGTH))
            if license_plate.decode() == PLACEHOLDER_LICENSE_PLATE:
                free_spots.append(i)

        return free_spots

    def find_vehicle(self, license_plate: str) -> (int or None):
        """
        Searches for the parking space number for a given car with `license_plate`

        :param str license_plate: String to indicate car's plate
        """
        self.db.seek(0)

        for i in range(self.parking_size):
            [license_plate, _, _] = struct.unpack(STRUCT_FORMAT, self.db.read(DB_RECORD_LENGTH))
            if license_plate.decode() == license_plate:
                return i
        
        return None

    def find_vehicles_with_color(self, color: str) -> list:
        candidates = []
        self.db.seek(0)

        for spot in range(self.parking_size):
            [current_lp, current_color, current_brand] = struct.unpack(STRUCT_FORMAT, self.db.read(DB_RECORD_LENGTH)) 
            if current_color.decode() == color:
                candidates.append(Vehicle(current_lp, current_color, current_brand, spot))
        
        return candidates

    def find_vehicles_with_brand(self, brand: str) -> list:
        candidates = []
        self.db.seek(0)

        for spot in range(self.parking_size):
            [current_lp, current_color, current_brand] = struct.unpack(STRUCT_FORMAT, self.db.read(DB_RECORD_LENGTH)) 
            if current_brand.decode() == brand:
                candidates.append(Vehicle(current_lp, current_color, current_brand, spot))
        
        return candidates

    # TODO: check if file is deleted

