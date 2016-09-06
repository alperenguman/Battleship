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


def choose_ship(which_map):
    a_placed = ("Aircraft Carrier" in [item.name for item in which_map.ship_placed])
    b_placed = ("Battleship" in [item.name for item in which_map.ship_placed])
    c_placed = ("Cruiser" in [item.name for item in which_map.ship_placed])
    s_placed = ("Submarine" in [item.name for item in which_map.ship_placed])
    p_placed = ("Patrol Boat" in [item.name for item in which_map.ship_placed])

    if a_placed and b_placed and c_placed and s_placed and p_placed:
        clear()
        which_map.map_display()
        response = input("Great! you placed all your ships {}.\n\n"
                         "[A]ircraft Carrier (Size: 5)" + "."*3*a_placed+"PLACED"*a_placed+"\n"
                         "[B]attleship, (Size:4)"+"."*9*b_placed+"PLACED"*b_placed+"\n"
                         "[C]ruiser (Size: 3)"+"."*12*c_placed+"PLACED"*c_placed+"\n"
                         "[S]ubmarine (Size: 3)"+"."*10*s_placed+"PLACED"*s_placed+"\n"
                         "[P]atrol Boat (Size: 2)"+"."*8*p_placed+"PLACED"*p_placed+"\n\n"
                         "Press any key to move on\n"
                         "or select a ship to edit its position: ".format(which_map.owner))
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
            return 'escape'

    response = input("[A]ircraft Carrier (Size: 5)" + "."*3*a_placed+"PLACED"*a_placed+"\n"
                     "[B]attleship, (Size:4)"+"."*9*b_placed+"PLACED"*b_placed+"\n"
                     "[C]ruiser (Size: 3)"+"."*12*c_placed+"PLACED"*c_placed+"\n"
                     "[S]ubmarine (Size: 3)"+"."*10*s_placed+"PLACED"*s_placed+"\n"
                     "[P]atrol Boat (Size: 2)"+"."*8*p_placed+"PLACED"*p_placed+"\n\n"
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
        clear()
        which_map.map_display()
        print("'{}' does not denote a ship.\n Please select a ship using its first letter.\n".format(response))
        return choose_ship(which_map)

if __name__ == "__main__":
    clear()
    logo_path = os.path.dirname(__file__) + "/logo"
    with open(logo_path) as logo:
        logo_string = [letters for letters in logo]
        input(''.join(logo_string))

    player1 = Player()
    clear()
    player1_map = Map(owner=player1.name)
    player1_map.map_display()

    while True:
        if player1_map.place_ship(ship=choose_ship(player1_map)) == 'escape':
            break

    clear()
    input("{} please pass the game to {} and press any key"
          " when you're ready to continue".format(player1.name, 'Player 2'))

    clear()
    player2 = player.Player()