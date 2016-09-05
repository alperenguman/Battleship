import logging
import sys
import os
import ship

class Map:
    owner = None
    size = 10
    rows = None
    columns = None
    coordinates = None
    coordinates_dict = None
    ship_positions = []
    ship_placed = []
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

    def place_ship(self, **kwargs):

        for key, value in kwargs.items():

            if key == 'placement':
                placement = value
                selected_ship = self.ship_placed[-1]

            elif key == 'ship':
                ship_placed_string = [n.name for n in self.ship_placed]
                if value.name in ship_placed_string:
                    selected_ship = self.ship_placed[ship_placed_string.index(value.name)]

                    # CREATE A METHOD THAT REMOVES SELECTED SHIP COORDINATES FROM MAP

                    print("Enter coordinate to reposition your {}".format(selected_ship.name))

                else:
                    selected_ship = value
                    selected_ship.placed = True
                    self.ship_placed.append(selected_ship)

                placement = input("\nWhere do you want to put your {}?"
                                  " (Type Column/Row i.e C3) ".format(selected_ship.name)).lower()

            placement_formatted = (placement[0], int(placement[1]))
            Map.placement_orientation(self, placement_formatted, selected_ship.size, selected_ship.name)

            Map.clear()
            Map.map_display(self)
            logging.info("Position {} is marked by {}"
                         " for ship placement.".format(self.ship_positions[-1], self.owner))
            response = input('Are you sure {}? Press any key to continue'
                             ' or enter another coordinate'
                             ' to replace your {}. '.format(self.owner, selected_ship.name)).lower()

            try:
                response_formatted = (response[0], int(response[1]))
                if response_formatted in self.coordinates:
                    Map.remove_last(self, selected_ship.size)
                    self.place_ship(placement=response)
                else:
                    self.clear()
                    self.map_display()
                    print("Moving on!\n")
            except IndexError:
                self.clear()
                self.map_display()
                print("Moving on!\n")

    def placement_orientation(self, placement, ship_size, ship_name):

        orientation = input("Do you want to place your {} [V]ertically or [H]orizontally? ".format(ship_name)).lower()
        points = range(1,ship_size+1)

        if ship_size % 2 == 0:
            back = int(ship_size/2)
            front = int(ship_size/2 - 1)
            coords = range(-back,front+1)
        else:
            front_back = int(ship_size/2)
            coords = range(-front_back,front_back+1)

        if orientation == 'h':
            x_list = []

            for item in coords:
                x_list.append((self.columns[self.columns.index(placement[0])+item], placement[1]))

            for item in x_list:

                # ADD DIFFERENT DICTIONARY VALUE FOR EVERY DIFFERENT TYPE OF SHIP

                Map.placement_check(self, item)
                self.coordinates_dict[item] = 'SHIP_H'
                self.ship_positions.append(item)


        elif orientation == 'v':

            # MIRROR WHAY YOU'VE DONE FOR HORIZONTAL

            ship_pos=['Y'+str(n) for n in points]
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

        # CHECK FOR EVERY POINT OF SHIP NOT ONLY CENTER

        if placed_point not in self.coordinates:
            print("Sorry, you're trying to place the ship outside"
                  " the bounds of the map.")
            Map.place_ship(self)
            #insert logger
        elif self.coordinates_dict[placed_point] != 'EMPTY':
            print("Sorry your placement intersects another ship.")
            Map.place_ship(self)
            #insert logger
        else:
            pass

    def remove_last(self, ship_size):
        while ship_size > 0:
            last_p = self.ship_positions.pop()
            self.coordinates_dict[last_p] = 'EMPTY'
            self.removed.append(last_p)
            logging.info("Ship placement {} removed by {}".format(last_p, self.owner))
            ship_size -= 1
