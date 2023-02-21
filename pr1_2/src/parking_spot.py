"""
==================

This module, similarly to :class:`Vehicle`, will be used to represent with ease a data type representing a parking spot

- The parent class :class:`ParkingSpot`. It is used to represent information regarding a `spot` in the db.

==================
"""
class ParkingSpot:
    """
    This class initiates and represents a parking spot. It will show the attributes `spot` and :class:`Vehicle`

    """

    def __init__(self, spot, vehicle) -> None:
        """
        >>> from vehicle import Vehicle
        >>> car = Vehicle("1234ABC", "Red", "BMW")
        >>> ps = ParkingSpot(0, car)
        """
        self.vehicle = vehicle
        self.number = spot

    def occupied(self):
        """
        Returns :class:`Vehicle` if the spot is occupied, otherwise it does not return anything.

        >>> from vehicle import Vehicle
        >>> car = Vehicle("1234ABC", "Red", "BMW")
        >>> ps = ParkingSpot(0, car)
        >>> ps.occupied()
        True
        >>> ps2 = ParkingSpot(1, None)
        """
        return self.vehicle != None
    
    def __repr__(self) -> str:
        """
        >>> from vehicle import Vehicle
        >>> car = Vehicle("1234ABC", "Red", "BMW")
        >>> print(ParkingSpot(0, car))
        Spot 0: Vehicle <License plate: 1234ABC, Brand: BMW, Color: Red>
        """
        return f"Spot {self.number}: {self.vehicle}"
    
    def __str__(self) -> str:
        return self.__repr__()
    
    def __int__(self) -> int:
        return self.number
