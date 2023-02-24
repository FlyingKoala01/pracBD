"""
==================

This module is used to represent a :class:`Vehicle` with its attributes.

It also contains the :func:`valid_license_plate` function, that checks wether
a license plate is valid.

==================
"""

from string import digits, ascii_uppercase

def valid_license_plate(license) -> bool:
    """
    Checks if `license` follows the right format indicated by the documentation.

    The format needed is very simple and works in most EU countries:

    - Between 5 and 10 characters.
    - All characters must be digits or ascii uppercase.

    :param str license: String indicating the license to be checked

    :return: The validity of the license plate.
    :rtype: bool

    >>> valid_license_plate("1234ABC")
    True
    >>> valid_license_plate("12ABCDEFGHIJ")
    False
    >>> valid_license_plate("1234 5BC")
    False
    >>> valid_license_plate("1234abc")
    False
    """
    if len(license) < 5 or len(license) > 10: return False

    for c in license:
        if c not in digits + ascii_uppercase: return False

    return True

class Vehicle:
    """
    This class represents a Vehicle. A Vehicle has a license plate, a color
    and a brand. The license plate must follow the right format and the
    length of the color and brand must not exceed 10 characters.

    For convenience, attributes can be of string type, but also of byteArray type.

    :param str license_plate: The license plate of the vehicle, in the right format.
    :param str color: The color of the vehicle.
    :param str brand: The brand of the vehicle.

    >>> car = Vehicle("1234ABC", "Red", "BMW")
    >>> car.brand
    'BMW'
    >>> car.validate()[0]
    True
    >>> car
    Vehicle <License plate: 1234ABC, Brand: BMW, Color: Red>
    """

    BRAND_MAX_LENGTH = 10
    COLOR_MAX_LENGTH = 10
    LICENSE_PLATE_LENGTH = 10

    def __init__(self, license_plate, color, brand) -> None:
        """
        Attributes can be bytes or string.

        >>> car = Vehicle("1234ABC", "Red", "BMW")
        >>> car.brand
        'BMW'
        >>> car.validate()[0]
        True
        >>> car
        Vehicle <License plate: 1234ABC, Brand: BMW, Color: Red>
        """
        self.license_plate = license_plate if type(license_plate) == str else license_plate.decode().strip('\x00')
        self.color = color if type(color) == str else color.decode().strip('\x00')
        self.brand = brand if type(brand) == str else brand.decode().strip('\x00')

    def validate(self) -> tuple:
        """
        Returns (bool, str) with (True, "Valid vehicle") or (False, "Reason")
        wether the vehicle is valid.

        :rtype: tuple
        :return: A tuple with the result boolean and a message.

        >>> (Vehicle("1234ABC", "Red", "BMW")).validate()
        (True, 'Valid vehicle')
        >>> (Vehicle("123 ABC", "Red", "BMW")).validate()
        (False, 'Invalid license plate: use digits and uppercase, without spaces')
        >>> (Vehicle("1234ABC", "Reeeeeeeeeeed", "BMW")).validate()
        (False, 'Car color should not exceed 10 characters.')
        >>> (Vehicle("1234ABC", "Red", "BMWWWWWWWWWWWW")).validate()
        (False, 'Car brand should not exceed 10 characters.')
        """

        if not valid_license_plate(self.license_plate):
            return (False, 'Invalid license plate: use digits and uppercase, without spaces')
        if len(self.color) > 10:
            return (False, "Car color should not exceed 10 characters.")
        if len(self.brand) > 10:
            return (False, "Car brand should not exceed 10 characters.")
        return (True, "Valid vehicle")
    
    def __repr__(self) -> str:
        """
        >>> car = Vehicle("1234ABC", "Red", "BMW")
        >>> print(car)
        Vehicle <License plate: 1234ABC, Brand: BMW, Color: Red>
        """
        return f"Vehicle <License plate: {self.license_plate}, Brand: {self.brand}, Color: {self.color}>"
    
    def __str__(self) -> str:
        return self.__repr__()
    
    def encode(self):
        """
        Encodes the vehicle with the database format. Returns a list with
        3 byteArrays.

        >>> car1 = Vehicle("1234ABC", "Red", "BMW")
        >>> car1_s = str(car1)
        >>> car2 = Vehicle(*car1.encode())
        >>> car1_s == str(car2)
        True
        """
        return [self.license_plate.encode(), self.color.encode(), self.brand.encode()]
