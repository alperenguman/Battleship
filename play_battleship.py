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

if __name__ == "__main__":

    player1 = Player()

    player1_map = Map(owner=player1)
    player1_map.map_display()
    player1_map.place_ship()
    clear()

    input("{} please pass the game to {} and press any key"
          " when you're ready to continue".format(player1.name, 'Player 2'))

    player2 = player.Player()