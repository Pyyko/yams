""" Defining the structur of an object player """
from .board import Board

class Player:
    """ Defining what a class player should have as attributes
    if you want your player to have a name add a player.name field !"""

    # no init method beause it doesn't have the purpose to be instancied only to be a parent
    # idk if it's a correct way to implement things but at least it's clear
    # like abstract class in Java

    def make_a_move(self, board : Board, dices : list, throw_left : int)-> (int, list):
        """
        You have to chose on which combo you want to play
        or (if you haven't use all your throws) the dices you want to keep and those you want to throw

        Main information is :
            - the number of throwing dices you have left 
            - the dices you currently have in hand

            
        Parameters
        ----------
        board : Board object
        where everything is saved and calculated, see help(board)
        dices : list of int
        the dices you currently have in hand
        throw_left : int
        the number of throw you have left, if 0 you have to make a choice !

        Returns
        -------
        out : int, list of int
        int for the choice you make (if you want to throw dices again, still return something)
        list of int : the dice you want to keep and those you want to throw again
        by example [0, 1, 1, 1, 1] mean that you want to keep the four last dices and throw 
        again the first one and [1, 1, 1, 1, 1] mean that you want to keep them all and stop 
        (then the choice you return is important !)
        """

        #default comportement choice is the first in the list and you keep all dices
        return board.possibilities(self)[0], [1, 1, 1, 1 ,1]
