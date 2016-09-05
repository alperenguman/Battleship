class Ship:
    size = 3
    name = 'ship'
    sunk = False
    placed = False


class AircraftCarrier(Ship):
    size = 5
    name = 'Aircraft Carrier'


class Battleship(Ship):
    size = 4
    name = 'Battleship'


class Submarine(Ship):
    size = 3
    name = 'Submarine'


class Cruiser(Ship):
    size = 3
    name = 'Cruiser'


class PatrolBoat(Ship):
    size = 2
    name = 'Patrol Boat'

