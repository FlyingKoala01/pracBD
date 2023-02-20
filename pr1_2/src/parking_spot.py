
class ParkingSpot:
    def __init__(self, spot, vehicle) -> None:
        self.vehicle = vehicle
        self.number = spot

    def occupied(self):
        return self.vehicle != None
    
    def __repr__(self) -> str:
        return f"Spot {self.number}: {self.vehicle}"
    
    def __str__(self) -> str:
        return self.__repr__()
    
    def __int__(self) -> int:
        return self.number
