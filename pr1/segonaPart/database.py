"""
==================

The module will be used to interact with the `spot_data.dat` file. It contains the following classes:


- The parent class :class:`ParkingDatabase`. It is used to interact with the db.

- The exception :class:`DatabaseCorruptionError`, that is raised when the db file is corrupted.

==================
"""
from os import path
from struct import * 
from input_manager import valid_license_plate

CAR_COLOR = "XXXXXXXXXX"
CAR_BRAND = "XXXXXXXXXX"
LEN_SLOT_DB = len(CAR_BRAND) + len(CAR_COLOR) + 7

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

        car_pack = pack("7s10s10s", "XXXXXXX".encode(), "XXXXXXXXXX".encode(), "XXXXXXXXXX".encode())
        file.write(car_pack * self.parking_size)

    def _is_db_valid(self):
        """
        Checks all the license plates in the db. If any plate is not well formatted, it returns `False`.
        """

        self.db.seek(0)

        for _ in range(self.parking_size):
            data = unpack("7s10s10s", self.db.read(LEN_SLOT_DB))
            if data[0].decode() != "XXXXXXX" and not valid_license_plate(data[0].decode()):
                return False

        # Checking that we have reached the end of file.

        return self.db.read(1).decode() == ""

    def _first_empty_spot(self):
        """
        Function to find the first empty spot in the db indicated by "XXXXXXX". Returns the spot number if one is found.
        """
        self.db.seek(0)

        for i in range(self.parking_size):
            if (unpack("7s10s10s", self.db.read(LEN_SLOT_DB))[0]).decode() == "XXXXXXX":
                return i

        return None

    def insert_vehicle(self, license_plate, car_color, car_brand, spot=None):
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
            self.db.seek(LEN_SLOT_DB*spot)
            # Spot occupied (Error 1)
            if unpack(self.db.read(LEN_SLOT_DB))[0] != "XXXXXXX": return 1
        
        # Check if car is already in parking (Error 3)
        if self.find_vehicle(license_plate) != None: return 3

        self.db.seek(LEN_SLOT_DB*spot)
        car_pack = pack("7s10s10s", license_plate.encode(), car_color.encode(), car_brand.encode())
        self.db.write(car_pack)
        return 0

    def remove_vehicle(self, license_plate):
        """
        Function used to remove a specific car with `license_plate`.

        :param str license_plate: String to indicate car's plate
        """
        spot =  self.find_vehicle(license_plate)
        if spot == None: return 1

        self.db.seek(LEN_SLOT_DB*spot)
        car_pack = pack("7s10s10s", "XXXXXXX".encode(), CAR_COLOR.encode(), CAR_BRAND.encode())
        self.db.write(car_pack * self.parking_size)

        return 0

    def check_spot(self, spot_number):
        """
        Used to check if for a specific spot `spot_number`, there is a car parked or not

        :param int spot_number: Indicating a specific parking space 
        """
        self.db.seek(LEN_SLOT_DB*spot_number)
        car_pack = unpack("7s10s10s", self.db.read(LEN_SLOT_DB) )

        return None if car_pack[0].decode() == "XXXXXXX" else car_pack

    def empty_spots(self):
        """
        Returns a list of the empty spots in the db.
        """
        free_spots = []
        self.db.seek(0)

        for i in range(self.parking_size):
            if (unpack("7s10s10s", self.db.read(LEN_SLOT_DB))[0]).decode() == "XXXXXXX":
                free_spots.append(i)

        return free_spots

    def find_vehicle(self, license_plate):
        """
        Searches for the parking space number for a given car with `license_plate`

        :param str license_plate: String to indicate car's plate
        """
        self.db.seek(0)

        for i in range(self.parking_size):
            if  (unpack("7s10s10s", self.db.read(LEN_SLOT_DB))[0]).decode() == license_plate:
                return i
        
        return None
    
    def find_vehicle_color(self, color):
        
        candidates = []
        self.db.seek(0)
        print(color)
        for i in range(self.parking_size):
            candidate = unpack("7s10s10s", self.db.read(LEN_SLOT_DB))
            if (candidate[1]).decode() == color:
                print("GOT IT", candidate[1].decode())
                candidates.append((i, candidate))
        
        return None if candidates else candidates 

    def find_vehicle_brand(self, brand):
        
        candidates = []
        self.db.seek(0)

        for i in range(self.parking_size):
            candidate = unpack("7s10s10s", self.db.read(LEN_SLOT_DB)) 
            if  candidate[2].decode() == brand:
                candidates.append((i, candidate))
        
        return None if candidates else candidates 

    # TODO: check if file is deleted

