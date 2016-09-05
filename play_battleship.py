from map import Map
from player import Player
import player
import ship
import sys
import os
import logging

logging.basicConfig(filename='battleship.log', level=logging.DEBUG)


def clear():
    if sys.platform == 'win32':
        os.system("cls")
    else:
        os.system("clear")


def pass_laptop():
    clear()
    input("{} please pass the game to {} and press any key"
          " when you're ready to continue".format(player1.name, player2.name))
    clear()

def choose_ship(map):
    for item in map.ship_placed:
        if item.name in ["Aircraft Carrier", "Battleship",
                         "Cruiser", "Submarine", "Patrol Boat"]:
            print(item.name, "\n")
        else:
            continue

    response = input("[A]ircraft Carrier (Size: 5)\n"
                     "[B]attleship, (Size:4)\n"
                     "[C]ruiser (Size: 3)\n"
                     "[S]ubmarine (Size: 3)\n"
                     "[P]atrol Boat (Size: 2)\n\n"
                     "Please select a ship to place: ")
    if response.lower() == 'a':
        return ship.AircraftCarrier()
    elif response.lower() == 'b':
        return ship.Battleship()
    elif response.lower() == 'c':
        return ship.Cruiser()
    elif response.lower() == 's':
        return ship.Submarine()
    elif response.lower() == 'p':
        return ship.PatrolBoat()
    else:
        choose_ship(on_map)

if __name__ == "__main__":
    clear()
    player1 = Player()
    clear()
    player1_map = Map(owner=player1.name)
    player1_map.map_display()
    while len(player1_map.ship_placed) < 5:
        player1_map.place_ship(ship=choose_ship(player1_map))
    clear()

    input("{} please pass the game to {} and press any key"
          " when you're ready to continue".format(player1.name, 'Player 2'))

    clear()
    player2 = player.Player()