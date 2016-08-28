from map import Map
import player
import ship
import sys
import os

def clear():
    if sys.platform == 'win32':
        os.system("cls")
    else:
        os.system("clear")

def pass_laptop():
    clear()
    input("{} please pass the game to {} and press any key"
          " when you're ready to continue".format(player1,player2))
    clear()

if __name__ == "__main__":

    player1 = player.Player()
    clear()
    player1map = Map()
    player1map.map_display()
    captured_coordinate = player1map.place_ship()
    player1map.change_map(alperen='guman')

    player2 = "Player 2"
    pass_laptop()
    player2 = player.Player()