"""This module implement the class Human, 
which is design to manually play the yams (interacting with the user with input() and print() method)"""

from .functions.player_template import Player
from .functions.board import Board


class Human(Player):
    """Human is a class which is designed to implement a human player,
      this class interact with the user with input() 
      and print usefull informations to him (with print())"""

    def __init__(self, name):
        self.name = name

    def make_a_move(self, board : Board, dices : list, throw_left : int)-> (int, list):
        """make a move with input asking the player what does he wants to play according to
        the number of throws he has left and the dices he got. 
        Always print the dices and don't stop until the player made a correct choice
        

        TODO : describe what are the shortcuts
        
        """

        print("---------------------\n")
        print("Time to make a choice : \n\nThrows left :",
               throw_left, " | Your dices :", dices, "\n")

        while True:
            try:
                answer = input("Choice : ")
                if len(answer) == 0:
                    choice = board.possibilities(self)[0]
                    dices_str = "11111"

                elif len(answer) in (1,2):
                    choice = int(answer)
                    dices_str = "11111"

                elif len(answer)==5:
                    choice = board.possibilities(self)[0]
                    dices_str = answer

                else:
                    choice, dices_str = answer.split(" ")
                    choice = int(choice)

                dices = []
                for dice in dices_str:
                    dices.append(int(dice))

                    if len(dices)==5:
                        break
                if len(dices)!=5:
                    raise ValueError


                if choice<=0 or choice==7 or choice>14:
                    raise ValueError


            except ValueError:
                print("""\n "ValueError" : Your choice must be under this structur : "n abcde"
                      where n is the choice and a,b,c,d,e are either 0 or 1, 1 if you want to
                      keep the dice 0 if not""")

            else:
                break

        return choice, dices
