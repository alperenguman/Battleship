class Map:

    size = 10
    rows = None
    columns = None
    coordinates = None
    coordinates_dict = None

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

        self.coordinates_dict[('j', 10)] = "FULL"

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

    def change_map(self, **kwargs):

        for key, value in kwargs.items():
            if key in self.coordinates:
                self.coordinates_dict[key] = value
            else:
                setattr(self, key, value)

        Map.map_display(self)

    def place_ship(self):

        placement = input("\nWhere do you want to put your ship? (Type Column/Row i.e C3) ").lower()
        placement_formatted = (placement[0], int(placement[1]))

        if placement_formatted not in self.coordinates_dict:
            print("Sorry that's not a coordinate on the map.")
            Map.place_ship(self)
        else:
            self.coordinates_dict[placement_formatted] = 'SHIP'
