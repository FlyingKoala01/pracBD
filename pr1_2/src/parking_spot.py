"""
==================

This module, similarly to :class:`Vehicle`, will be used to represent
with ease a data type representing a parking spot.

==================
"""
class ParkingSpot:
    """
    This class initiates and represents a parking spot.
    It holds the parking spot number and the vehicle that is in it.

    :param int spot: The number of the parking spot.
    :param vehicle.Vehicle vehicle: The vehicle that's in that spot or None if the spot is empty.

    >>> from vehicle import Vehicle
    >>> car = Vehicle("1234ABC", "Red", "BMW")
    >>> ps = ParkingSpot(0, car)
    >>> ps.vehicle == car
    True
    >>> ps.number == 0
    True
    >>> ps
    Spot 0: Vehicle <License plate: 1234ABC, Brand: BMW, Color: Red>
    >>> int(ps)
    0
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
        Returns wether the parking spot is occupied.

        :return: Wether the parking spot is occupied.
        :rtype: bool

        >>> from vehicle import Vehicle
        >>> car = Vehicle("1234ABC", "Red", "BMW")
        >>> ps = ParkingSpot(0, car)
        >>> ps.occupied()
        True
        >>> ps2 = ParkingSpot(1, None)
        >>> ps2.occupied()
        False
        """
        return self.vehicle != None
    
    def __repr__(self) -> str:
        """
        String representation of a vehicle.

        >>> from vehicle import Vehicle
        >>> car = Vehicle("1234ABC", "Red", "BMW")
        >>> print(ParkingSpot(0, car))
        Spot 0: Vehicle <License plate: 1234ABC, Brand: BMW, Color: Red>
        """
        return f"Spot {self.number}: {self.vehicle}"
    
    def __str__(self) -> str:
        return self.__repr__()
    
    def __int__(self) -> int:
        """
        Returns the number of the parking spot.

        >>> from vehicle import Vehicle
        >>> car = Vehicle("1234ABC", "Red", "BMW")
        >>> ps = ParkingSpot(0, car)
        >>> int(ps)
        0
        """
        return self.number
