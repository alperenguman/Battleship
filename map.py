class Map:

    def setup_map(self):
        map_size = input("Select map size [S]mall [M]edium or [L]arge]")
        if map_size.lower()== 's':
            self.create_map(5)
        elif map_size.lower()== 'm':
            self.create_map(10)
        elif map_size.lower()== 'l':
            self.create_map(15)

    def create_map(self, *kwargs):
        setattr('key','value', 10)
        pass

    def print_map(self):
        pass