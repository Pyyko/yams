import math
from f import Player, MathDice
from board import Board


def test_value_dices_board():
    """test if combo dices values are correct"""

    player_uno = Player()
    player_dos = Player()
    board = Board([player_uno, player_dos])

    dices = [1,2,1,5,5]
    assert board.points[5](dices) == 10, "2*5 = 10 point for playing 5"
    assert board.points[4](dices) == 0, "0*4 = 0 point for playing 4"
    assert board.points[8](dices) == 14, "14 points for playing 3same"
    assert board.points[13](dices) == 50, "50 points for 5 identical"

    # board.print()


def test_verif_values():
    """test if updating values work"""
    player_uno = Player()
    player_dos = Player()
    its_me = Player()

    board = Board([player_uno, player_dos, its_me])


    #basics updates
    dices = [1,1,1,1,1]
    board.update(its_me, 14, dices)
    board.update(its_me, 1, dices)
    board.update(its_me, 2, dices)

    score_me = board.find_score(its_me)
    score_player = board.find_score(player_uno)

    score_me_answer = [its_me] + [5] + [0] + [None]*4 + [0] + [None]*6 + [5]
    score_player_answer = [player_uno] + [None]*6 + [0] + [None]*7

    assert score_player_answer == score_player, "Score update failed"
    assert score_me == score_me_answer, "Score update failed"


    #possibilities test
    assert board.possibilities(its_me) == [3, 4, 5, 6] + list(range(8, 14)), "Possibilities function failed"    


    #next_player test
    next_player = board.score[0][0]
    if  next_player==its_me:
        next_player = board.score[1][0]

    assert board.who_is_next_player() == next_player, "who_is_next_player from Board failed"


    #testing if update for bonus work and for + 100 bonus if 5 in a row too !

    board.update(its_me, 13, [1, 1, 1, 1, 1])
    score_me_answer = [its_me] + [5] + [0] + [None]*4 + [0] + [None]*5 + [50] + [5]
    score_me = board.find_score(its_me)
    assert score_me_answer == score_me, "Score update for +50 failed"

    #weird because should be in update maybe ?? not in throw
    board.throw([6, 6, 6, 6, 6]) 
    board.update(its_me, 6, [6, 6, 6, 6, 6])
    score_me_answer = [its_me] + [5] + [0] + [None]*3 + [30] + [0] + [None]*5 + [150] + [5]
    score_me = board.find_score(its_me)

    assert score_me_answer == score_me, "Score update for +150 failed"

    #test for the bonus of + 35
    board.update(its_me, 5, [5, 5, 5, 5, 5])
    board.update(its_me, 3, [1, 3, 4, 6, 4])

    score_me_answer = [its_me] + [5] + [0] + [3] + [None]*1 + [25] + [30] + [35] + [None]*5 + [150] + [5]
    score_me = board.find_score(its_me)
    assert score_me_answer == score_me, "Score update for the bonus failed"


def test_player_default():
    """test if all work (with player as a default player) TODO"""
    player = Player()


def test_mathdice():
    """test mathdice"""

    # Find dices method
    assert MathDice.find_dices([1,4,4,2,3], [1,0,0,1,1]) == [1,2,3], "find_dice failed"
    assert MathDice.find_dices([1,4,4,2,3], [0,0,0,0,0]) == [], "find_dice failed"
    assert MathDice.find_dices([1,4,4,2,3], [1,1,1,1,1]) == [1,4,4,2,3], "find_dice failed"

    # Bernoulli (P(X>n))

    assert MathDice.greater_bernoulli(5, 0, 1/6) == 1, "greater_bernoulli failed"
    assert MathDice.greater_bernoulli(5, 1) == round(1 - (5/6)**5, 5), "greater_bernoulli failed"

    # in_a_row
    assert MathDice.in_a_row(2, [1, 2, 3, 3, 4], [1, 1, 1, 1, 1]) == 1, "MathDice.in_a_row failed"
    assert MathDice.in_a_row(2, [2]*5, [1, 1, 1, 1, 1], nb = 5) == 1, "MathDice.in_a_row failed"
    assert MathDice.in_a_row(3, [4, 3, 2, 3, 1], [0, 1, 1, 1, 1], nb = 3) == round(1/6, 5), "MathDice.in_a_row failed"
    assert MathDice.in_a_row(1, [2,3,1,3,2], [0, 0, 1, 0, 0], nb=5) == round((1/6)**(4), 5), "MathDice.in_a_row failed"
    assert MathDice.in_a_row(1, [2,3,1,3,2], [0, 0, 1, 0, 0], nb=2) == round(1-(5/6)**4, 5), "MathDice.in_a_row failed"

    # full

    # usefull to compare with reality
    # from random import randint
    # def simul(n=500000):
        
    #     total = []
    #     for _ in range(n):
    #         total.append([1,1, 2, randint(1,6), randint(1,6)])
    #     result = [l for l in total if (len(set(l))==2 and (l.count(l[0]) in (3, 2)))]
    #     print("resultat veritable : ", len(a)/n)
    # simul()

    assert MathDice.full([1,2,3,3,4], [0, 0, 0, 0 ,0]) == round(((1/6)**(3)*(5/6))*math.comb(5,2), 5), "MathDice.full failed"
    assert MathDice.full([1,1,1,1,1], [1,1,1, 0, 0]) == round(5/6*1/6, 5), "MathDice.full failed"
    assert MathDice.full([1,1,1,1,1], [0,1,0,1,0]) == round((1/6*5/6*1/6)*3 + 5/6*1/6*1/6, 5), "MathDice.full failed"
    assert MathDice.full([1,1,1,1,1], [1, 0, 0, 0, 0]) == round((1/6*1/6*5/6*1/6)*6 + (1/6*5/6*1/6*1/6)*4, 5), "MathDice.full failed"
    assert MathDice.full([1,1,2,1,1], [1,0,1,0,1]) == round(1/36 + 2/36, 5), "MathDice.full failed"
    assert MathDice.full([1,1,2,2,1], [1,0,1,1,1]) == round(1/3, 5), "MathDice.full failed"
    assert MathDice.full([1,2,3,3,4], [1, 1, 1, 0 ,0]) == round(0, 5), "MathDice.full failed"
    #TODO vite fait regarder si on select 1 1 !

    # proba_specific_dices

    # assert round(MathDice.proba_specific_dices([1, 2, 3, 4, 6], [1,1,1,1,0], [1,2,3,4,5]), 5) == round(1/6, 5), "MathDice.proba_specific_dices failed"
    # assert round(MathDice.proba_specific_dices([1, 2, 3, 1, 6], [1,1,1,1,0], [1,2,3,5,4]), 5) == round(0, 5), "MathDice.proba_specific_dices failed"
    # assert round(MathDice.proba_specific_dices([1, 2, 3, 2, 6], [1,1,0,0,0], [1, 4, 5, 3, 6]), 5) == round(0, 5), "MathDice.proba_specific_dices failed"
    # assert round(MathDice.proba_specific_dices([1, 2, 3, 6, 6], [0,0,0,0,1], [1, 2, 3, 6, 5]),5) == round((4*3*2)/(6**4), 5), "MathDice.proba_specific_dices failed"
    # assert round(MathDice.proba_specific_dices([1, 2, 3, 6, 6], [0,0,0,1,1], [1, 2, 3, 6, 5]),5) == round(0, 5), "MathDice.proba_specific_dices failed"

    # long straight

    assert MathDice.long_straight([1, 1, 1, 1, 1], [1,1,1,1,0]) == round(0, 5), "MathDice.long_straight failed"
    assert MathDice.long_straight([1, 2, 3, 6, 6], [1,1,1,1,0]) == round(0, 5), "MathDice.long_straight failed"
    assert MathDice.long_straight([2, 2, 3, 4, 5], [0,1,1,1,1]) == round(1/3, 5), "MathDice.long_straight failed"
    assert MathDice.long_straight([1, 2, 3, 6, 6], [0,0,0,0,1]) == round((4*3*2)/(6**4), 5), "MathDice.long_straight failed"

    # small straight

    #all result have been calculated by simulation
    assert MathDice.small_straight([1, 1, 1, 1, 1], [1,1,1,0,0]) == round(0, 5), "MathDice.small_straight failed"
    assert round(MathDice.small_straight([1, 1, 1, 1, 1], [1,1,0,0,0]),3) == round(0.027816, 3), "MathDice.small_straight failed"
    assert round(MathDice.small_straight([1, 1, 1, 1, 1], [0,0,0,0,0]),3) == round(0.154, 3), "MathDice.small_straight failed"
    assert round(MathDice.small_straight([1, 1, 1, 1, 6], [1,0,0,0,1]),3) == round(0.0556, 3), "MathDice.small_straight failed"
    assert round(MathDice.small_straight([1, 2, 3, 4, 5], [1,1,1,1,1]),3) == round(1, 3), "MathDice.small_straight failed"
    assert round(MathDice.small_straight([1, 2, 3, 4, 5], [1,1,1,1,1]),3) == round(1, 3), "MathDice.small_straight failed"
    assert round(MathDice.small_straight([2, 3, 4, 1, 1], [1,1,1,0,0]),3) == round(0.55569, 3), "MathDice.small_straight failed"
    assert round(MathDice.small_straight([1, 2, 3, 4, 5], [0,1,0,0,0]), 3) == round(0.148284, 3), "MathDice.small_straight failed"
    assert round(MathDice.small_straight([1, 2, 3, 4, 5], [0,0,0,0,0]), 3) == round(0.15407, 3), "MathDice.small_straight failed"
    assert round(MathDice.small_straight([1, 6, 3, 4, 5], [1,1,0,0,0]), 3) == round(0.0556511, 3), "MathDice.small_straight failed"

    # from random import randint
    # n = 100000
    # total = []
    # for _ in range(n):
    #     total.append([1, 6, randint(1,6), randint(1,6), randint(1,6)])

    # possibilities = [[2,3,4,5], [1,2,3,4], [3,4,5,6]]
    
    # a =[]
    # for t in total:
    #     for p in possibilities:
    #         if p[0] in t and p[1] in t and p[2] in t and p[3] in t: # and (2 in t or 1 in t):
    #             a.append(t)
    #             break


if __name__ == "__main__":
    test_value_dices_board()
    test_verif_values()
    test_mathdice()
    print("All test cleared")
                  