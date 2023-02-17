"""
==================

The module will be used to interact with the `spot_data.dat` file. It contains the following classes:


- The parent class :class:`ParkingDatabase`. It is used to interact with the db.

- The exception :class:`DatabaseCorruptionError`, that is raised when the db file is corrupted.

==================
"""
from os import path
from input_manager import valid_license_plate

class DatabaseCorruptionError(Exception):
    """
    This Exception is systematically raised everytime the instruction BRK is being executed.
    It is used to break the simulation in :func:`BREAK.execute`.

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
            return open(file, 'r+')
        else:
            file = open(file, 'w+')
            self.__init_db_file(file)
            return file

    def __init_db_file(self, file):
        """
        Initializes the database in `file`. Fills the car spaces with "XXXXXXX".

        :param str file: String indicating the file name
        """
        # We suppose that the file has been just opened and was empty.
        file.write("XXXXXXX" * self.parking_size)

    def _is_db_valid(self):
        """
        Checks all the license plates in the db. If any plate is not well formatted, it returns `False`.
        """

        self.db.seek(0)

        for _ in range(self.parking_size):
            data = self.db.read(7)
            if data != "XXXXXXX" and not valid_license_plate(data):
                return False

        # Checking that we have reached the end of file.
        return self.db.read(1) == ""

    def _first_empty_spot(self):
        """
        Function to find the first empty spot in the db indicated by "XXXXXXX". Returns the spot number if one is found.
        """
        self.db.seek(0)

        for i in range(self.parking_size):
            if self.db.read(7) == "XXXXXXX":
                return i

        return None

    def insert_vehicle(self, license_plate, spot=None):
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
            self.db.seek(7*spot)
            # Spot occupied (Error 1)
            if self.db.read(7) != "XXXXXXX": return 1
        
        # Check if car is already in parking (Error 3)
        if self.find_vehicle(license_plate) != None: return 3

        self.db.seek(7*spot)
        self.db.write(license_plate)
        return 0

    def remove_vehicle(self, license_plate):
        """
        Function used to remove a specific car with `license_plate`.

        :param str license_plate: String to indicate car's plate
        """
        spot =  self.find_vehicle(license_plate)
        if spot == None: return 1

        self.db.seek(7*spot)
        self.db.write("XXXXXXX")

        return 0

    def check_spot(self, spot_number):
        """
        Used to check if for a specific spot `spot_number`, there is a car parked or not

        :param int spot_number: Indicating a specific parking space 
        """
        self.db.seek(7 * spot_number)
        license_plate = self.db.read(7) 

        return None if license_plate == "XXXXXXX" else license_plate

    def empty_spots(self):
        """
        Returns a list of the empty spots in the db.
        """
        free_spots = []
        self.db.seek(0)

        for i in range(self.parking_size):
            if self.db.read(7) == "XXXXXXX":
                free_spots.append(i)

        return free_spots

    def find_vehicle(self, license_plate):
        """
        Searches for the parking space number for a given car with `license_plate`

        :param str license_plate: String to indicate car's plate
        """
        self.db.seek(0)

        for i in range(self.parking_size):
            if  self.db.read(7) == license_plate:
                return i
        
        return None

    # TODO: check if file is deleted

