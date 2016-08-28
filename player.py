class Player:

    name = "Unknown Player"

    def get_name(self):
        self.name = input("What is your name? ")
        name_correct = input("{}, is that correct? [Y]es or any other key for no ".format(self.name))
        if name_correct.lower() == 'y':
            print("Splendid!")
        else:
            self.get_name()

    def __init__(self):
        self.get_name()

    def __str__(self):
        return("{}: {}".format(__class__.__name__, self.name))