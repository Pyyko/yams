from f import Player, MathDice
from board import Board


class GreedyMathguy(Player):
    """justa greedy guy who chose his dices according to"""

    def make_a_move(self, board : Board, dices : list, throw_left : int)-> (int, list):

        if throw_left==0:
            every_proba = self.value_of_this_one(board, dices, [1]*5)
            return self.best_choice(every_proba, board), [1]*5


        selec_dices = [0, 0, 0, 0, 0]
        best_expectation = 0

        for a in [[0],[1]]:
            for b in [[0],[1]]:
                for c in [[0],[1]]:
                    for d in [[0],[1]]:
                        for e in [[0],[1]]:
                            value = sum(self.value_of_this_one(board, dices, a+b+c+d+e)[1:])
                            if value > best_expectation:
                                best_expectation = value
                                selec_dices = a+b+c+d+e

        return self.best_choice(self.value_of_this_one(board, dices, selec_dices), board), selec_dices


    def value_of_this_one(self, board, dices, selec_dices):
        
        every_proba = MathDice.every_probability(board, self, dices, selec_dices)

        for i in range(1,7):
            every_proba[i] *= i

        every_proba[8]*=3.5 #yeah not optimal but haven't implemented a function taht does it properly
        every_proba[9]*=3.5
        every_proba[10]*=25
        every_proba[11]*=30
        every_proba[12]*=40
        every_proba[13]*=50
        every_proba[14]*=18

        return every_proba


    def best_choice(self, every_proba, board):

        best_choice =  board.possibilities(self)[0]
        
        for i in range(1, len(every_proba)):
            if every_proba[i]> every_proba[best_choice]:
                best_choice = i

        return best_choice