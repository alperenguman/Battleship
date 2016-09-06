import logging
import sys
import os
import string
import ship
import pdb


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
        columns_letters = list(string.ascii_lowercase)
        self.columns = columns_letters[0:self.size]
        numbers = range(1, self.size+1)
        self.rows = [n for n in numbers]
        self.coordinates = []

        for numbers in self.rows:
            for letters in self.columns:
                self.coordinates.append((letters, numbers))

        self.coordinates_dict = {}
        for items in self.coordinates:
            self.coordinates_dict[items] = "EMPTY"

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
            elif self.coordinates_dict[item][5] == "H" and n % len(self.columns) == 0 and m < len(self.rows):
                map_display.append('-')
                map_display.append('\n')
                if self.rows[m] < 10:
                    map_display.append(' '+str(self.rows[m]))
                else:
                    map_display.append(str(self.rows[m]))
                m += 1
            elif self.coordinates_dict[item][5] == "H" and n % len(self.columns) == 0:
                map_display.append('-')
                map_display.append('\n')
            elif self.coordinates_dict[item][5] == "H":
                map_display.append('-')
            elif self.coordinates_dict[item][5] == "V" and n % len(self.columns) == 0 and m < len(self.rows):
                map_display.append('|')
                map_display.append('\n')
                if self.rows[m] < 10:
                    map_display.append(' '+str(self.rows[m]))
                else:
                    map_display.append(str(self.rows[m]))
                m += 1
            elif self.coordinates_dict[item][5] == "V" and n % len(self.columns) == 0:
                map_display.append('|')
                map_display.append('\n')
            elif self.coordinates_dict[item][5] == "V":
                map_display.append('|')
            else:
                map_display.append('1')

        print('\n', '  ', ' '.join(self.columns).upper())
        print('', ' '.join(map_display))

    def place_ship(self, **kwargs):

        placement = None
        selected_ship = None

        for key, value in kwargs.items():

            if key == 'ship' and value == 'escape':
                return 'escape'

            elif key == 'placement':
                placement = value
                selected_ship = self.ship_placed[-1]

            elif key == 'ship':

                ship_placed_string = [n.name for n in self.ship_placed]
                if value.name in ship_placed_string:
                    selected_ship = self.ship_placed[ship_placed_string.index(value.name)]

                    self.remove_ship(selected_ship)

                    print("\nEnter coordinate to reposition your {}".format(selected_ship.name))

                else:
                    selected_ship = value
                    selected_ship.placed = True
                    self.ship_placed.append(selected_ship)

                placement = input("Where do you want to put your {}?"
                                  " (Type Column/Row i.e C3) ".format(selected_ship.name)).lower()

        if len(placement) == 2 and placement[0] in list(string.ascii_lowercase)[:self.size]\
           and int(placement[1]) < self.size:

            placement_formatted = (placement[0], int(placement[1]))

            # REPEATED CODE NEST IN A SEPARATE FUNCTION
            if placement_formatted not in self.coordinates_dict:
                Map.clear()
                Map.map_display(self)
                print("Out of bounds, try again.")
                self.place_ship(ship=selected_ship)

            orientation_result = Map.placement_orientation(self, placement_formatted, selected_ship)

            if orientation_result == 'escape':
                return self.place_ship(ship=selected_ship)
            elif orientation_result == 'soft_escape':
                self.clear()
                self.map_display()
                print("{}, please use 'H' or 'V' to specify\n"
                      "the orientation of your {}.\n".format(self.owner, selected_ship.name))
                return self.place_ship(placement=placement_formatted)

            else:
                Map.clear()
                Map.map_display(self)
                logging.info("Position {} is marked by {}"
                             " for ship placement.".format(self.ship_positions, self.owner))  # CHANGE LOGGING OF POS

        elif len(placement) == 3 and placement[0] in list(string.ascii_lowercase)[:self.size]:

            placement_formatted = (placement[0], int(placement[1]+placement[2]))

            # REPEATED CODE BELOW NEST IN A SEPARATE FUNCTION
            if placement_formatted not in self.coordinates_dict:
                Map.clear()
                Map.map_display(self)
                print("Out of bounds, try again.")
                self.place_ship(ship=selected_ship)

            orientation_result = Map.placement_orientation(self, placement_formatted, selected_ship)

            if orientation_result == 'escape':
                return self.place_ship(ship=selected_ship)
            elif orientation_result == 'soft_escape':
                self.clear()
                self.map_display()
                print("{}, please use 'H' or 'V' to specify\n"
                      "the orientation of your {}.\n".format(self.owner, selected_ship.name))
                return self.place_ship(placement=placement_formatted)

            else:
                Map.clear()
                Map.map_display(self)
                logging.info("Position {} is marked by {}"
                             " for ship placement.".format(self.ship_positions, self.owner))  # CHANGE LOGGING OF POS

        else:
            Map.clear()
            Map.map_display(self)
            print("Please check your formatting")
            self.place_ship(ship=selected_ship)

    def placement_orientation(self, placement, selected_ship):

        ship_size = selected_ship.size
        ship_name = selected_ship.name

        orientation = input("Do you want to place your {} [V]ertically or [H]orizontally? ".format(ship_name)).lower()

        if ship_size % 2 == 0:
            back = int(ship_size/2)
            front = int(ship_size/2 - 1)
            coords = range(-back,front+1)
        else:
            front_back = int(ship_size/2)
            coords = range(-front_back,front_back+1)

        if orientation == 'h':
            x_list = []
            successful_check = True

            for item in coords:
                if self.columns.index(placement[0])+item < 0 or self.columns.index(placement[0])+item > self.size:
                    successful_check = False
                    break

            if successful_check:
                for item in coords:
                    x_list.append((self.columns[self.columns.index(placement[0])+item], placement[1]))
            else:
                self.clear()
                self.map_display()
                print("Your placement is out of bounds. ")
                return 'escape'

            for coordinate in x_list:
                if self.placement_check(coordinate):
                    self.remove_ship(selected_ship)
                    self.clear()
                    self.map_display()
                    print("Your placement intersects another ship. ")
                    return 'escape'
                self.coordinates_dict[coordinate] = 'SHIP_H_'+selected_ship.name
                self.ship_positions.append(coordinate)

        elif orientation == 'v':

            y_list = []
            successful_check = True

            for item in coords:
                if self.rows.index(placement[1])+item < 0 or self.rows.index(placement[1])+item > self.size:
                        successful_check = False
                        break

            if successful_check:
                for item in coords:
                    y_list.append((placement[0], self.rows[self.rows.index(placement[1])+item]))
            else:
                self.clear()
                self.map_display()
                print("Your placement is out of bounds. ")
                return 'escape'

            for coordinate in y_list:
                if self.placement_check(coordinate):
                    self.remove_ship(selected_ship)
                    self.clear()
                    self.map_display()
                    print("Your placement intersects another ship. ")
                    return 'escape'
                self.coordinates_dict[coordinate] = 'SHIP_V_'+selected_ship.name
                self.ship_positions.append(coordinate)
        else:
            return 'soft_escape'

    def placement_check(self, coordinate):
        if coordinate not in self.coordinates:
            return False

        elif self.coordinates_dict[coordinate] != 'EMPTY':
            return True

        else:
            return False

    def remove_ship(self, selected_ship):

        for key, value in self.coordinates_dict.items():
            if value == 'SHIP_H_'+selected_ship.name or value == 'SHIP_V_'+selected_ship.name:
                self.coordinates_dict[key] = 'EMPTY'

