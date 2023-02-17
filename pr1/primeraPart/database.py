from os import path
from input_manager import valid_license_plate

class DatabaseCorruptionError(Exception):
    pass

class ParkingDatabase():
    def __init__(self, db_file, parking_size, init_if_not_exist=False):
        self.parking_size = parking_size
        self.db = self.__open_db_file(db_file, init_if_not_exist)
        if not self._is_db_valid(): raise DatabaseCorruptionError

    def end(self):
        self.db.close()

    def __open_db_file(self, file, init_if_not_exist):
        if not init_if_not_exist or path.exists(file):
            return open(file, 'r+')
        else:
            file = open(file, 'w+')
            self.__init_db_file(file)
            return file

    def __init_db_file(self, file):
        # We suppose that the file has been just opened and was empty.
        file.write("XXXXXXX" * self.parking_size)

    def _is_db_valid(self):
        self.db.seek(0)

        for _ in range(self.parking_size):
            data = self.db.read(7)
            if data != "XXXXXXX" and not valid_license_plate(data):
                return False

        # Checking that we have reached the end of file.
        return self.db.read(1) == ""

    def _first_empty_spot(self):
        self.db.seek(0)

        for i in range(self.parking_size):
            if self.db.read(7) == "XXXXXXX":
                return i

        return None

    def insert_vehicle(self, license_plate, spot=None):
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
        spot =  self.find_vehicle(license_plate)
        if spot == None: return 1

        self.db.seek(7*spot)
        self.db.write("XXXXXXX")

        return 0

    def check_spot(self, spot_number):
        self.db.seek(7 * spot_number)
        license_plate = self.db.read(7) 

        return None if license_plate == "XXXXXXX" else license_plate

    def empty_spots(self):
        free_spots = []
        self.db.seek(0)

        for i in range(self.parking_size):
            if self.db.read(7) == "XXXXXXX":
                free_spots.append(i)

        return free_spots

    def find_vehicle(self, license_plate):
        self.db.seek(0)

        for i in range(self.parking_size):
            if  self.db.read(7) == license_plate:
                return i
        
        return None

    # TODO: check if file is deleted

