"""
==================

This module is used to represent a :class:`Vehicle` with its attributers.
It is used to simplfy the process of handling the 3 characteristics composing a car 
in the parking slot database.

- The parent class :class:`Vehicle`. It is used to create and represent a data type to represent a vehicle 
with 3 attributes, `license plate`, `color` and `brand`.

==================
"""

from string import digits, ascii_uppercase

def valid_license_plate(license) -> bool:
    """
    Checks if `license` follows the right format indicated by the documentation.

    :param str license: String indicating the license to be checked

    >>> valid_license_plate("1234ABC")
    True
    >>> valid_license_plate("12ABCDEF")
    False
    >>> valid_license_plate("12345BC")
    False
    >>> valid_license_plate("1234abc")
    False

    """
    if len(license) != 7: return False

    for i in range(0, 4):
        if license[i] not in digits: return False
    
    for i in range(4, 7):
        if license[i] not in ascii_uppercase: return False

    return True

class Vehicle:
    """
    This class initiates and validates a car. It is also used to fix a size for the registers used in the db.
    It is also used to ease the encoding/decoding of bytes/strings when storing and retrieving data from the db.

    """
    
    BRAND_MAX_LENGTH = 10
    COLOR_MAX_LENGTH = 10
    LICENSE_PLATE_LENGTH = 7

    def __init__(self, license_plate, color, brand) -> None:
        """
        Attributes can be bytes or string
        """
        self.license_plate = license_plate if type(license_plate) == str else license_plate.decode()
        self.color = color if type(color) == str else color.decode().strip('\x00')
        self.brand = brand if type(brand) == str else brand.decode().strip('\x00')

    def validate(self) -> tuple:
        """
        Returns (bool, str) with (True, "Valid vehicle") or (False, "Reason").
        """
        if not valid_license_plate(self.license_plate):
            return (False, "Invalid license plate: use format 0000AAA")
        if len(self.color) > 10:
            return (False, "Car color should not exceed 10 characters.")
        if len(self.brand) > 10:
            return (False, "Car brand should not exceed 10 characters.")
        return (True, "Valid vehicle")
    
    def __repr__(self) -> str:
        return f"Vehicle <License plate: {self.license_plate}, Brand: {self.brand}, Color: {self.color}>"
    
    def __str__(self) -> str:
        return self.__repr__()
    
    def encode(self):
        return [self.license_plate.encode(), self.color.encode(), self.brand.encode()]
