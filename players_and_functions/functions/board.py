"""Implement the class board which will hold the sccore"""

import random


class Board:
    """The board which hold scores"""


    def __init__(self, players_objects : list):

        # just for fun using lambda :
        f_number = lambda number_list : lambda dices: sum ([i for i in dices if i in number_list]) 

        # give it dices it will give the score that you have done for figure i
        self.points = [None, f_number([1]), f_number([2]), f_number([3]), f_number([4]),
                        f_number([5]), f_number([6]), None, f_number([1,2,3,4,5,6]),
                        f_number([1,2,3,4,5,6]), lambda dices : 25, lambda dices : 30,
                        lambda dices : 40, lambda dices : 50, f_number([1,2,3,4,5,6])]

        self.score = []

        # Structure of self.score : [[Player_object of player 1:, score_for 1, ..., score for 14],
        #                           [[Player_object of player 2: str, ...]]
        #                           [...]


        self.players_names = {}
        # self.player_name[player_object] = name

        for player in players_objects:

            # giving a name mainly for print function
            player_name = "player_" + str(len(self.score))
            if hasattr(player, "name"):
                player_name = player.name
            self.players_names[player] = player_name


            self.score.append([player] + [None]*6 + [0] + [None]*7)

    def get_name(self, player_object):
        """return the name of a player object"""
        return self.players_names[player_object]

    def print(self):
        """basic print"""

        for player in self.score:
            print(self.get_name(player[0]) + " "*(15 - len(self.players_names[player[0]])), end='')

            print("")
            print("------------------------------------------------------------------\n")
            print("1 : Ones :          ", "  " if player[1] is None else player[1])
            print("2 : Twos :          ", "  " if player[2] is None else player[2])
            print("3 : Threes :        ", "  " if player[3] is None else player[3])
            print("4 : Fours :         ", "  " if player[4] is None else player[4])
            print("5 : Fives :         ", "  " if player[5] is None else player[5])
            print("6 : Sixes :         ", "  " if player[6] is None else player[6])
            print("Bonus :             ", "  " if player[7] is None else player[7])
            print("8 : 3 of a kind  :  ", "  " if player[8] is None else player[8])
            print("9 : 4 of a kind :   ", "  " if player[9] is None else player[9])
            print("10 : Full :         ", "  " if player[10] is None else player[10])
            print("11 : Sm. Straight : ", "  " if player[11] is None else player[11])
            print("12 : Lg. Straight : ", "  " if player[12] is None else player[12])   
            print("13 : 5 of a kind :  ", "  " if player[13] is None else player[13])
            print("14 : Chance :       ", "  " if player[14] is None else player[14])
            print("\n")

    def is_playable(self, dices, choice):
        """look if choice is playable or not (0 score if not otherwise self.point(choice) score)"""
        counting = [0,0,0,0,0,0]
        for dice in dices:
            counting[dice-1]+=1

        # 3 same
        if choice == 8:
            return max(counting)>=3

        if choice == 9:
            return max(counting)>=4

        if choice == 10:
            return (3 in counting) and (2 in counting)

        if choice == 11:
            return (counting[2]>0 and counting[3]>0) and (
                (counting[0]>0 and counting[1]>0) or
                (counting[1]>0 and counting[4]>0) or
                (counting[4]>0 and counting[5]>0))

        if choice == 12:
            return 1==counting[1]==counting[2]==counting[3]==counting[4]

        if choice == 13:
            return len(set(dices))==1

        # remaining choices which have no condition
        return True


    def game_ended(self):
        """return True if game_ended else False"""
        return None not in self.score[-1]


    def update(self, player, choice : int, dices):
        """choice is the number of the move played"""

        if choice<=0 or choice==7 or choice>=15:
            raise ValueError(f"\n ! Invalid choice {choice} isn't bewteen 1 and 14 or is 7\n")
        indice = 0
        for i, score in enumerate(self.score):
            if score[0] == player:
                indice = i
                break

        if self.score[indice][choice]:
            raise ValueError(f"! You already played this : {choice}!")

        if self.is_playable(dices, choice):
            self.score[indice][choice] = self.points[choice](dices)
        else:
            self.score[indice][choice] = 0


        if self.score[indice][7] == 0:
            score_for_bonus = sum([self.score[indice][i] for i in range(1,7) if self.score[indice][i] is not None])
            if score_for_bonus >= 63:
                self.score[indice][7] = 35

        return 0

    def throw(self, selectionned_dices):
        """ will make a trow with the other than selectionned dice
        Return a list of the non-played choices possibles for player
            
        Parameters
        ----------
        selectionned_dices: selec_dices


        Returns
        -------
        out : list
        list of int of all choices left
        """

        dices = []
        for _ in range(5-len(selectionned_dices)):
            dices.append(random.randint(1,6))

        return selectionned_dices + dices

    def possibilities(self, player):
        """
        Return a list of the non-played choices possibles for player
            
        Parameters
        ----------
        player: Player object
        player object of the player you are looking for possibles choices
            
        Returns
        -------
        out : list
        list of int of all choices left
        """

        player_score = self.find_score(player)
        return [i for i in range(1, len(player_score)) if player_score[i] is None]


    def find_score(self, player):
        """give the score of player"""

        for score in self.score:
            if score[0] == player:
                return score.copy()

        raise ValueError(f"player {player} not found")


    def who_is_next_player(self):
        """give the next player"""

        more_move_played = [0]*len(self.score)

        for i, player_score in enumerate(self.score):
            for played in player_score:
                if played is not None:
                    more_move_played[i]+=1

        # the first with less move played is the next player
        i = more_move_played.index(min(more_move_played))

        return self.score[i][0]

    def make_a_throw(self, player_object):
        """will intereact with an object Player to decide the trow """

        # need the  player because bonus of + 100 if 5 in a row even if not scored
        # ( TODO : weird have to check that again)

        # can be changed, has to be >= 1
        number_of_throw = 3

        dices = self.throw([])
        number_of_throw -= 1
        choice, index_of_dices_kept = player_object.make_a_move(self, dices, number_of_throw)

        while number_of_throw!=0:
            number_of_throw -= 1

            if not(index_of_dices_kept)==[1, 1, 1, 1, 1]:
                dices_kept = [dices[i] for i in range(5) if index_of_dices_kept[i]==1]
                dices = self.throw(dices_kept)
                choice, index_of_dices_kept = player_object.make_a_move(self, dices, number_of_throw)

        return choice, dices

    def score_tab(self):
        """ues"""

        tab = []
        for score in self.score:
            s = score[0]
            p = sum([i for i in score[1:] if i is not None])
            tab.append((s,p))

        tab.sort(key = lambda sp : sp[1], reverse = True)
        return tab
