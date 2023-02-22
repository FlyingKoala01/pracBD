"""
==================

The module will be used to interact with the `spot_data.dat` file.

In contains the `class.DatabaseCorruptionError` Exception, the class to
manage database connections and an auxiliary function to sort license plates.

==================
"""

from os import path
from input_manager import valid_license_plate

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
    >>> db.insert_vehicle("7865FTH", 565)
    0
    >>> db.check_spot(565)
    '7865FTH'
    >>> db.remove_vehicle("7865FTH")
    0
    >>> db.check_spot(1)
    >>> db.remove_vehicle("7865FTH")
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
        >>> db.insert_vehicle("9877JKL")
        Traceback (most recent call last):
         ...
        ValueError: I/O operation on closed file.
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
            return open(file, 'r+')
        else:
            file = open(file, 'w+')
            self.__init_db_file(file)
            return file

    def __init_db_file(self, file):
        """
        Initializes the database in `file`. Fills the spaces with "XXXXXXX".

        :param str file: String indicating the file name
        """

        # We suppose that the file has been just opened and was empty.
        file.write("XXXXXXX" * self.parking_size)

    def _is_db_valid(self):
        """
        Checks all the license plates in the db.
        If any plate is not well formatted, it returns `False`.

        :return: Wether the db is well formatted.
        :rtype: bool
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
        Function to find the first empty spot in the db indicated by "XXXXXXX".

        :return: The number of the first empty spot or None if parking full.
        :rtype: int
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

        Output codes:
        - 0: Success.
        - 1: Specific spot full.
        - 2: Parking full.
        - 3: License plate already in parking.

        :param str license_plate: String to indicate car's plate.
        :param int spot: Indicating a specific parking space.

        :return: The output code specifying the results stated above.
        :rtype: int

        >>> db = ParkingDatabase("./spot_data.dat", 1000, True)
        >>> db.insert_vehicle("9876DEF")
        0
        >>> place = db.find_vehicle("9876DEF")
        >>> print(db.check_spot(place))
        9876DEF
        >>> db.remove_vehicle("9876DEF")
        0
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

        Output codes:
        - 0: Success.
        - 1: Car not found in parking.

        :param str license_plate: String to indicate car's plate.

        :return: The output code specified above.
        :rtype: int

        >>> db = ParkingDatabase("./spot_data.dat", 1000, True)
        >>> db.insert_vehicle("7865FTH", 565)
        0
        >>> db.check_spot(565)
        '7865FTH'
        >>> db.remove_vehicle("7865FTH")
        0
        >>> db.check_spot(1)
        >>> db.remove_vehicle("7865FTH")
        1
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

        :return: The license_plate or None if cars aren't found.
        :rtype: str
        
        >>> db = ParkingDatabase("./spot_data.dat", 1000, True)
        >>> db.insert_vehicle("9878RTY", 789)
        0
        >>> db.check_spot(789)
        '9878RTY'
        >>> db.remove_vehicle("9878RTY")
        0
        """

        self.db.seek(7 * spot_number)
        license_plate = self.db.read(7) 

        return None if license_plate == "XXXXXXX" else license_plate

    def empty_spots(self):
        """
        Returns a list of the empty spots in the db.

        :return: The list of empty spots.
        :rtype: list

        >>> db = ParkingDatabase("./spot_data.dat", 1000, True)
        >>> a = len(db.empty_spots())
        >>> db.insert_vehicle("3256AGH")
        0
        >>> b = len(db.empty_spots())
        >>> a == b+1
        True
        >>> db.remove_vehicle("3256AGH")
        0
        """

        free_spots = []
        self.db.seek(0)

        for i in range(self.parking_size):
            if self.db.read(7) == "XXXXXXX":
                free_spots.append(i)

        return free_spots
    
    def full_spots(self):
        """
        Returns a list of the empty spots in the db.

        :return: The list of empty spots.
        :rtype: list

        >>> db = ParkingDatabase("./spot_data.dat", 1000, True)
        >>> a = len(db.full_spots())
        >>> db.insert_vehicle("3256AGH")
        0
        >>> b = len(db.full_spots())
        >>> a+1 == b
        True
        >>> db.remove_vehicle("3256AGH")
        0
        """

        free_spots = []
        self.db.seek(0)

        for i in range(self.parking_size):
            license_plate = self.db.read(7)
            if license_plate != "XXXXXXX":
                free_spots.append((i, license_plate))

        return free_spots

    def find_vehicle(self, license_plate):
        """
        Searches for the parking space number for a given car with `license_plate`

        :param str license_plate: String to indicate car's plate

        :return: The vehicle parking spot.
        :rtype: int

        >>> db = ParkingDatabase("./spot_data.dat", 1000, True)
        >>> db.insert_vehicle("3712LOK")
        0
        >>> place = db.find_vehicle("3712LOK")
        >>> print(db.check_spot(place))
        3712LOK
        >>> db.remove_vehicle("3712LOK")
        0
        """
        self.db.seek(0)

        for i in range(self.parking_size):
            if  self.db.read(7) == license_plate:
                return i
        
        return None
    
    def oldest_vehicles(self):
        license_plates = [x[1] for x in self.full_spots()]
        license_plates.sort(key = license_plate_to_alphanumeric)
        return license_plates

def license_plate_to_alphanumeric(license_plate):
    """
    Returns an integer representing the license plate. The number isn't very
    important, what matters is that an older license_plate will always have
    a smaller number.

    :param str license_plate: MUST be a valid license plate

    :return: A number representing the age of the license plate. The smaller, the younger.
    :rtype: int

    >>> a = license_plate_to_alphanumeric('1234GGH')
    >>> b = license_plate_to_alphanumeric('1235GGH')
    >>> c = license_plate_to_alphanumeric('1235GGG')
    >>> d = license_plate_to_alphanumeric('1235MGH')
    >>> c < a and a < b and b < d
    True
    """
    fixed_license_plate = license_plate[4:] + license_plate[:4]
    return int.from_bytes(fixed_license_plate.encode(), 'big')
