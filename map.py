import logging
import sys
import os


class Map:
    owner = None
    size = 10
    rows = None
    columns = None
    coordinates = None
    coordinates_dict = None
    ship_positions = []
    removed = []

    @staticmethod
    def clear():
        if sys.platform == 'win32':
            os.system("cls")
        else:
            os.system("clear")

    def __init__(self, **kwargs):

        for key, value in kwargs.items():
            setattr(self, key, value)
        Map.setup_map(self)

    def setup_map(self):
        columns_letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
                           'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
                           's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        self.columns = columns_letters[0:self.size]
        numbers = range(1, self.size+1)
        self.rows = [n for n in numbers]
        self.coordinates = []

        for numbers in self.rows:
            for letters in self.columns:
                self.coordinates.append((letters, numbers))

        self.coordinates_dict = {}
        for items in self.coordinates:
            self.coordinates_dict[items]="EMPTY"

    def map_display(self):

        map_display = []
        n = 0
        m = 0
        map_display.append(' '+str(self.rows[m]))
        m = 1
        for item in self.coordinates:
            n += 1
            if self.coordinates_dict[item] == "EMPTY" and n % len(self.columns) == 0 and m < len(self.rows):
                map_display.append('O')
                map_display.append('\n')
                if self.rows[m] < 10:
                    map_display.append(' '+str(self.rows[m]))
                else:
                    map_display.append(str(self.rows[m]))
                m += 1
            elif self.coordinates_dict[item] == "EMPTY" and n % len(self.columns) == 0:
                map_display.append('O')
                map_display.append('\n')
            elif self.coordinates_dict[item] == "EMPTY":
                map_display.append('O')
            elif self.coordinates_dict[item] == "SHIP_H":
                map_display.append('-')
            elif self.coordinates_dict[item] == "SHIP_V":
                map_display.append('|')
            else:
                map_display.append('1')
        print('\n', '  ', ' '.join(self.columns).upper())
        print('', ' '.join(map_display))

    def place_ship(self, ship, **kwargs):
        placement = None
        print(ship.size)
        for key, value in kwargs.items():
            if key == 'placement':
                placement = value

        if placement is not None:
            pass

        else:
            placement = input("\nWhere do you want to put your ship? (Type Column/Row i.e C3) ").lower()

        placement_formatted = (placement[0], int(placement[1]))
        Map.placement_orientation(self, placement_formatted)

        Map.clear()
        Map.map_display(self)
        logging.info("Position {} is marked by {} for ship placement.".format(self.ship_positions[-1], self.owner))
        response = input('Are you sure {}? Press [Y]es to continue'
                         ' or enter another value correct what you just did. '.format(self.owner))

        if response.lower() == 'y':
            pass
        else:
            Map.remove_last(self)
            self.place_ship(placement=response)

    def placement_orientation(self, placement):
        orientation = input("Do you want to place your ship [V]ertically or [H]orizontally? ").lower()
        if orientation == 'h':
            X1 = (self.columns[self.columns.index(placement[0])+1], placement[1])
            X2 = (self.columns[self.columns.index(placement[0])], placement[1])
            X3 = (self.columns[self.columns.index(placement[0])-1], placement[1])
            Map.placement_check(self, X1)
            Map.placement_check(self, X2)
            Map.placement_check(self, X3)
            self.coordinates_dict[X1] = 'SHIP_H'
            self.coordinates_dict[X2] = 'SHIP_H'
            self.coordinates_dict[X3] = 'SHIP_H'
            self.ship_positions.append(X1)
            self.ship_positions.append(X2)
            self.ship_positions.append(X3)

        elif orientation == 'v':
            Y1 = (placement[0],placement[1]+1)
            Y2 = (placement[0],placement[1])
            Y3 = (placement[0],placement[1]-1)
            Map.placement_check(self, Y1)
            Map.placement_check(self, Y2)
            Map.placement_check(self, Y3)
            self.coordinates_dict[Y1] = 'SHIP_V'
            self.coordinates_dict[Y2] = 'SHIP_V'
            self.coordinates_dict[Y3] = 'SHIP_V'
            self.ship_positions.append(Y1)
            self.ship_positions.append(Y2)
            self.ship_positions.append(Y3)
        else:
            Map.placement_orientation(self)

    def placement_check(self, placed_point):

        if placed_point not in self.coordinates:
            print("Sorry you're trying to place the ship out of"
                  " the bounds of the map.")
            Map.place_ship(self)
            #insert logger
        elif self.coordinates_dict[placed_point] != 'EMPTY':
            print("Sorry your placement intersects another ship.")
            Map.place_ship(self)
            #insert logger
        else:
            pass

    def remove_last(self):
        n = 3
        while n > 0:
            last_p = self.ship_positions.pop()
            self.coordinates_dict[last_p] = 'EMPTY'
            self.removed.append(last_p)
            logging.info("Ship placement {} removed by {}".format(last_p, self.owner))
            n -= 1
