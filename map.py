class Map:

    size = 10

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        if 'size' not in kwargs:
            self.setup_map()
            self.print_map()
        else:
           pass

    def setup_map(self):
        map_size = input("Select map size [S]mall [M]edium or [L]arge]")
        if map_size.lower()== 's':
            self.size=5
        elif map_size.lower()== 'm':
            self.size=10
        elif map_size.lower()== 'l':
            self.size=15

    def print_map(self):
        columns_letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q',
                   'r','s','t','u','v','w','x','y','z']
        columns = columns_letters[0:self.size]
        numbers = range(1, self.size+1)
        rows = [n for n in numbers]
        coordinates = []

        for x in columns:
            for y in rows:
                coordinates.append((x, y))


        print(rows)
        print(columns)
        print(coordinates)

        print("\n")
        n = 0
        row_number = 0
        while n != self.size:
            print(row_number, "0 "*self.size)
            row_number += 1
            n = n + 1