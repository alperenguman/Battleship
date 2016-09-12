import map


class Player:

    name = "Unknown Player"

    def get_name(self):
        self.name = input("What is your name? ")
        if len(self.name) < 1:
            map.Map.clear()
            print("Give me a letter at least, eh?")
            return self.get_name()

        name_correct = input("{}, is that correct? [Y]es or any other key for no ".format(self.name))
        if name_correct.lower() == 'y':
            print("Splendid!")
        else:
            return self.get_name()

    def __init__(self):
        self.get_name()

    def __str__(self):
        return "{}: {}".format(__class__.__name__, self.name)
