"""A basic Yams game based on the one implemented on the mobile app "plato", goal is to train a reinforced model on it"""
from f import Player
from board import Board
from players import *
import os
from human import Human
from greedymathguy import GreedyMathguy


#ais_names = os.listdir("ais")
#ais_name = map(lambda name : name[:-3], ais_names)  # Removing ".py"


#for now i won't make a graphical interface

#for name in ais_name:
 #   print(name)

# Shuffle to avoid any repetition in the play order
# random.shuffle(players_names)

me = Human("me")
me_too = Player()
me_too_too = Player()
greed = GreedyMathguy()

board = Board([GreedyMathguy() for i in range(500)])

while board.game_ended() is False:

    #board.print()
    player = board.who_is_next_player()
    choice, dices = board.make_a_throw(player)
    board.update(player, choice, dices)

    # print(f"{board.get_name(player)} just played {choice} with {dices}",
    #       f"and scored {board.points[choice](dices) if board.is_playable(dices, choice) else 0 }")
    # print("")

board.print() # we have to change that


# printing score tab
p_w = board.score_tab()

print("     RESULTATS !")
print("------------------------------------------------------------------\n")
for i,c in enumerate(p_w):
    print(f"{i+1}{'ème' if i>0 else 'er'} : {board.get_name(c[0])} with {c[1]} points !")
print("\n------------------------------------------------------------------\n")

