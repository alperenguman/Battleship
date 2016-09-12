from map import Map
from player import Player
import ship
import sys
import os
import logging
import pdb


def clear():
    if sys.platform == 'win32':
        os.system("cls")
    else:
        os.system("clear")


def choose_ship(which_map):
    a_placed = ("Aircraft Carrier" in [item.name for item in which_map.ship_placed])
    b_placed = ("Battleship" in [item.name for item in which_map.ship_placed])
    c_placed = ("Cruiser" in [item.name for item in which_map.ship_placed])
    s_placed = ("Submarine" in [item.name for item in which_map.ship_placed])
    p_placed = ("Patrol Boat" in [item.name for item in which_map.ship_placed])

    if a_placed and b_placed and c_placed and s_placed and p_placed:
        clear()
        which_map.map_display()
        print("Great! you placed all your ships {}\n".format(which_map.owner))
        response = input("[A]ircraft Carrier (Size: 5)" + "."*3*a_placed+"PLACED"*a_placed+"\n"
                         "[B]attleship, (Size:4)"+"."*9*b_placed+"PLACED"*b_placed+"\n"
                         "[C]ruiser (Size: 3)"+"."*12*c_placed+"PLACED"*c_placed+"\n"
                         "[S]ubmarine (Size: 3)"+"."*10*s_placed+"PLACED"*s_placed+"\n"
                         "[P]atrol Boat (Size: 2)"+"."*8*p_placed+"PLACED"*p_placed+"\n\n"
                         "Press any key to move on\n"
                         "or select a ship to edit its position: ")
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


def game_setup():

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
        player2 = Player()
        clear()
        player2_map = Map(owner=player2.name)
        player2_map.map_display()

        while True:
            if player2_map.place_ship(ship=choose_ship(player2_map)) == 'escape':
                break
        clear()
        return player1, player2, player1_map, player2_map


def hit_or_miss(event):
    if event[0] == 'Missed':
        return 0
    else:
        return 1


def game_loop(self_prompt, other_prompt):

    player1_map.guess_map_display()
    print("{} above is your enemy's map.\n"
          "Please select where you want to attack.".format(player2_map.owner))
    player2_map.map_display()
    player2_attack = input("\nEnter coordinate to attack:")
    last_event = player1_map.attack(player2_attack)
    hit_miss_binary = hit_or_miss(last_event)
    clear()
    player1_map.guess_map_display()
    print("You" + last_event[0] + "an enemy ship!"*hit_miss_binary)
    a_n2, b_n2, c_n2, s_n2, p_n2 = player2_map.map_display()
    input("Please press any key to continue.")

    clear()
    input("Please pass the laptop to {} and press any key to continue.".format(player1_map.owner))

    clear()
    player2_map.guess_map_display()
    print("{} above is your guess map.\n"
          "Please select where you want to attack.".format(player1_map.owner))
    player1_map.map_display()
    player1_attack = input("\nEnter coordinate to attack:")
    last_event = player2_map.attack(player1_attack)

    clear()
    player2_map.guess_map_display()
    print("You" + last_event[0])
    a_n, b_n, c_n, s_n, p_n = player1_map.map_display()
    input("Please press any key to continue.")

    clear()
    input("Please pass the laptop to {} and press any key to continue.".format(player2_map.owner))

    ship_sizes_sum = ship.AircraftCarrier.size + ship.Battleship.size + ship.Cruiser.size + \
        ship.Ship.size + ship.PatrolBoat.size
    player1_taken_hits_sum = a_n + b_n + c_n + s_n + p_n
    player2_taken_hits_sum = a_n2 + b_n2 + c_n2 + s_n2 + p_n2

    return ship_sizes_sum, player1_taken_hits_sum, player2_taken_hits_sum

if __name__ == "__main__":

    logging.basicConfig(filename='battleship.log', level=logging.DEBUG)
    clear()

    logo_path = os.path.dirname(__file__) + "/logo"
    with open(logo_path) as logo:
        logo_string = [letters for letters in logo]
        input(''.join(logo_string))

    player1, player2, player1_map, player2_map = game_setup()

    ship_sizes_sum, player1_taken_hits_sum, player2_taken_hits_sum = game_loop()

    while player1_taken_hits_sum < ship_sizes_sum or  player2_taken_hits_sum < ship_sizes_sum:

        clear()
        player1_map.guess_map_display()
        print("{}, {}.\n"
              "Please select where you want to attack.".format(player2_map.owner, last_event))
        player2_map.map_display()

        player2_attack = input("\nEnter coordinate to attack:")
        player1_map.attack(player2_attack)
        clear()
        player1_map.guess_map_display()
        player2_map.map_display()
        input("Please press any key to continue.")
        clear()
        input("Please pass the laptop to {} and press any key to continue.".format(player1_map.owner))
        clear()
        player2_map.guess_map_display()
        print("{} above is your guess map.\n"
              "Please select where you want to attack.".format(player1_map.owner))
        player1_map.map_display()
        player1_attack = input("\nEnter coordinate to attack:")
        player2_map.attack(player1_attack)
        clear()
        player2_map.guess_map_display()
        a_n, b_n, c_n, s_n, p_n = player1_map.map_display()
        input("Please press any key to continue.")
        clear()
        input("Please pass the laptop to {} and press any key to continue.".format(player2_map.owner))
        clear()
    if player1_taken_hits_sum == ship_sizes_sum:
        player2_map.map_display()
        print("{} WINS!".format(player2.name))
        player1_map.map_display()
    elif player2_taken_hits_sum == ship_sizes_sum:
        player1_map.map_display()
        print("{} WINS!".format(player1.name))
        player2_map.map_display()
