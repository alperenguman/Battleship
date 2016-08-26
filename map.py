class Map:

    size = 10

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def print_map(self):
        columns_letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q',
                   'r','s','t','u','v','w','x','y','z']
        columns = columns_letters[0:self.size]
        numbers = range(1, self.size+1)
        rows = [n for n in numbers]
        coordinates = []

        for numbers in rows:
            for letters in columns:
                coordinates.append((letters, numbers))

        coordinates_dict = {}
        for items in coordinates:
            coordinates_dict[items]="EMPTY"

        coordinates_dict[('c',2)] = "FULL"

        map_display = []
        n = 0
        m = 0
        map_display.append(' '+str(rows[m]))
        m = 1
        for item in coordinates:
            n = n+1
            if coordinates_dict[item]=="EMPTY" and n%len(columns) == 0 and m<len(rows):
                map_display.append('0')
                map_display.append('\n')
                if rows[m]<10:
                    map_display.append(' '+str(rows[m]))
                else:
                    map_display.append(str(rows[m]))
                m = m+1
            elif coordinates_dict[item]=="EMPTY" and n%len(columns) == 0:
                map_display.append('0')
                map_display.append('\n')
            elif coordinates_dict[item]=="EMPTY":
                map_display.append('0')
            else:
                map_display.append('1')
        print('\n','  ', ' '.join(columns).upper())
        print('',' '.join(map_display))



        print(coordinates_dict)
        print(rows)
        print(columns)

