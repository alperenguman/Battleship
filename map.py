import logging


class Map:
    owner = None
    size = 10
    rows = None
    columns = None
    coordinates = None
    coordinates_dict = None
    ship_positions = []
    removed = []

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
                map_display.append('0')
                map_display.append('\n')
                if self.rows[m] < 10:
                    map_display.append(' '+str(self.rows[m]))
                else:
                    map_display.append(str(self.rows[m]))
                m += 1
            elif self.coordinates_dict[item] == "EMPTY" and n % len(self.columns) == 0:
                map_display.append('0')
                map_display.append('\n')
            elif self.coordinates_dict[item] == "EMPTY":
                map_display.append('0')
            else:
                map_display.append('1')
        print('\n', '  ', ' '.join(self.columns).upper())
        print('', ' '.join(map_display))

    def place_ship(self, **kwargs):
        placement = None

        for key, value in kwargs.items():
            if key == 'placement':
                placement = value

        if placement is not None:
            pass
        else:
            placement = input("\nWhere do you want to put your ship? (Type Column/Row i.e C3) ").lower()

        placement_formatted = (placement[0], int(placement[1]))

        if placement_formatted not in self.coordinates_dict:
            print("Sorry that's not a coordinate on the map.")
            Map.place_ship(self)
        else:
            self.ship_positions.append(placement_formatted)
            self.coordinates_dict[placement_formatted] = 'SHIP'

        Map.map_display(self)

        logging.info("Position {} is marked by {} for ship placement.".format(self.ship_positions[-1], self.owner))

        response = input('are you sure {}? Press [Y]es to continue'
                         ' or enter other value correct what you just did '.format(self.owner))

        if response.lower() == 'y':
            pass
        else:
            Map.remove_last(self)

            self.place_ship(placement=response)

    def remove_last(self):
        last_p = self.ship_positions.pop()
        self.coordinates_dict[last_p] = 'EMPTY'
        self.removed.append(last_p)
        logging.info("Ship placement {} removed by {}".format(last_p, self.owner))
        self.map_display()
