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
            elif self.coordinates_dict[item][5] == "H":
                map_display.append('-')
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

            if key == 'placement':
                placement = value
                selected_ship = self.ship_placed[-1]

            elif key == 'ship':
                ship_placed_string = [n.name for n in self.ship_placed]
                if value.name in ship_placed_string:
                    selected_ship = self.ship_placed[ship_placed_string.index(value.name)]

                    self.remove_ship(selected_ship)

                    print("Enter coordinate to reposition your {}".format(selected_ship.name))

                else:
                    selected_ship = value
                    selected_ship.placed = True
                    self.ship_placed.append(selected_ship)

                placement = input("\nWhere do you want to put your {}?"
                                  " (Type Column/Row i.e C3) ".format(selected_ship.name)).lower()
        if len(placement) == 2 and placement[0] in list(string.ascii_lowercase)[:self.size] and int(placement[1]) < self.size:
            placement_formatted = (placement[0], int(placement[1]))
        elif len(placement) == 3:
            placement_formatted = (placement[0], int(placement[1]+placement[2]))
        else:
            print("Please check your formatting")
            self.place_ship(ship=selected_ship)


        Map.placement_orientation(self, placement_formatted, selected_ship)

        Map.clear()
        Map.map_display(self)
        logging.info("Position {} is marked by {}"
                     " for ship placement.".format(self.ship_positions, self.owner))  # CHANGE LOGGING OF SHIP POS
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
                print("Success!\n")
        except IndexError:
            self.clear()
            self.map_display()
            print("Success!\n")

    def placement_orientation(self, placement, selected_ship):

        ship_size = selected_ship.size
        ship_name = selected_ship.name

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
            successful_check = True

            for item in coords:
                if self.columns.index(placement[0])+item < 0 or self.columns.index(placement[0])+item > self.size:
                    successful_check = False
                    break

            if successful_check:
                for item in coords:
                    x_list.append((self.columns[self.columns.index(placement[0])+item], placement[1]))
            else:
                print("Your placement is out of bounds. ")
                Map.place_ship(self, ship=selected_ship)

            for coordinate in x_list:

                Map.placement_check(self, coordinate, selected_ship)

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
                print("Your placement is out of bounds. ")
                Map.place_ship(self, ship=selected_ship)

            for coordinate in y_list:

                Map.placement_check(self, coordinate, selected_ship)
                self.coordinates_dict[coordinate] = 'SHIP_V_'+selected_ship.name
                self.ship_positions.append(coordinate)

        else:
            Map.placement_orientation(self)

    def placement_check(self, coordinate, selected_ship):

        # CHECK FOR EVERY POINT OF SHIP NOT ONLY CENTER

        if coordinate not in self.coordinates:
            print("Sorry, you're trying to place the ship outside"
                  " the bounds of the map.")
            Map.place_ship(self, ship=selected_ship)
            #insert logger
        elif self.coordinates_dict[coordinate] != 'EMPTY':
            print("Sorry your placement intersects another ship.")
            Map.place_ship(self, ship=selected_ship)
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

    def remove_ship(self, ship):

        for key, value in self.coordinates_dict.items():
            if value == 'SHIP_H_'+ship.name:
                self.coordinates_dict[key] = 'EMPTY'

