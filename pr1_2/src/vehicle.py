

from string import digits, ascii_uppercase

def valid_license_plate(license) -> bool:
    """
    Checks if `license` follows the right format indicated by the documentation.

    :param str license: String indicating the license to be checked
    """
    if len(license) != 7: return False

    for i in range(0, 4):
        if license[i] not in digits: return False
    
    for i in range(4, 7):
        if license[i] not in ascii_uppercase: return False

    return True

class Vehicle:

    BRAND_MAX_LENGTH = 10
    COLOR_MAX_LENGTH = 10
    LICENSE_PLATE_LENGTH = 7

    def __init__(self, license_plate, color, brand, spot=None) -> None:
        """
        Attributes can be bytes or string
        """
        self.license_plate = license_plate if type(license_plate) == str else license_plate.decode()
        self.color = color if type(color) == str else color.decode()
        self.brand = brand if type(brand) == str else brand.decode()
        # Vehicles may contain a parking spot in certain use cases
        self.spot = spot

    def validate(self) -> tuple(bool, str):
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
