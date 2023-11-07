from functions.player_template import Player
from functions.board import Board


class Vry_dumb_AI:
    """Using reinforcement learning, dynamic programming, does NOT respect markov property !
    So the AI is a bit blind to avoid too much computation """

    # first ideas : state : 
    def __init__(self, name):
        self.name = name



    def learnding(self, iterations):


    def make_a_move(self, board : Board, dices : list, throw_left : int)-> (int, list):
        

        self_score = Board.find_score(board, self)




        return choice, dices