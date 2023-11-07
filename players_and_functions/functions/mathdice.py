import math


class MathDice:

    @staticmethod
    def find_dices(dices, selec_dices):
        """return a list of the dice"""
        return [dices[i] for i in range(len(dices)) if selec_dices[i]]

    @staticmethod
    def bernoulli(n, k, p=1/6):
        """give P(X=k) for X following a binomial law"""
        return math.comb(n, k) *((p)**k)*( (1-p)**(n-k))

    @staticmethod
    def greater_bernoulli(n, k, p=1/6):
        """ give P(X>=k) for bernoulli """
        proba = 0
        for i in range(k, n+1):
            proba += math.comb(n, i) *((p)**i)*( (1-p)**(n-i))

        return round(proba, 5)

    @staticmethod
    def in_a_row(dice, dices, selec_dices, nb=0):
        """if nb=0 then expectation of dice else proba of having at least nb of dice in next throw"""

        #having a list of the dice we selected
        dices = MathDice.find_dices(dices, selec_dices)
        nb_of_dice = dices.count(dice)
        n = 5 - len(dices)

        if not nb:
            return n*1/6 + nb_of_dice

        k = nb - nb_of_dice

        # if we already have enough in selected
        if k <= 0:
            return 1

        return MathDice.greater_bernoulli(n, k)

    @staticmethod
    def n_in_a_row(dices, selec_dices, n):
        """n in a row no matter the dice, return a list """
        return [MathDice.in_a_row(i, dices, selec_dices, n) for i in range(1,7)]

    @staticmethod
    def full(dices, selec_dices):

        selected_dices = MathDice.find_dices(dices, selec_dices)
        set_of_dices = list(set(selected_dices))

        if len(set_of_dices) == 0:
            # we want 3 same and then 2 same in this order (and we don't want same dice !)
            # then we multiply with all the order possibles
            return round(((1/6)**(3)*(5/6))*math.comb(5,2), 5)


        if len(set_of_dices) == 1:
            nb_dice = len(selected_dices)
            if len(selected_dices)>=4:
                return 0

            if len(selected_dices)==3:
                return round((5/6)*(1/6), 5)

            p = MathDice.bernoulli(5-nb_dice, 3-nb_dice)*(1/5)
            p += MathDice.bernoulli(5-nb_dice, 2-nb_dice)*(1/5)*(1/5)
            return round(p, 5)

        if len(set_of_dices) == 2:

            nb_dice_first = selected_dices.count(set_of_dices[0])
            nb_dice_second = selected_dices.count(set_of_dices[1])

            if nb_dice_first>=4 or nb_dice_second>=4:
                return 0
            
            if nb_dice_first == 3:
                return round((1/6)**(2-nb_dice_second), 5)

            if nb_dice_second == 3:
                return round((1/6)**(2-nb_dice_first), 5)
            
            p = MathDice.bernoulli(5-nb_dice_first-nb_dice_second,
                                    3-nb_dice_first) * (1/5)**(2-nb_dice_second)
            p += MathDice.bernoulli(5-nb_dice_first-nb_dice_second,
                                    3-nb_dice_second) * (1/5)**(2-nb_dice_first)

            return round(p, 5)

        # if more than 3dices different
        return 0

    @staticmethod
    def __proba_specific_dices(dices, selec_dices, dices_to_find):
        """dices_to_find is a list of dice you want the probability of having after the next throw, must be length of 5
        and ALL DICES HAVE TO BE DIFFERENT """

        # for now it's not a good function because it's not very ambitious
        list_of_select_dices = MathDice.find_dices(dices, selec_dices)
        
        if len(set(dices_to_find))!=5:
            raise ValueError(f"{dices_to_find} isn't a list of 5 different dices ")
            
        # removing dices we already have found
        for dice in list_of_select_dices:
            if dice not in dices_to_find:
                return 0 #because we search for 5 dices if have one extra we won't find it
            dices_to_find.remove(dice)

        n = len(dices_to_find)
        return math.factorial(n)/(6**n)

    @staticmethod
    def long_straight(dices, selec_dices):
        """"""

        possibilities = [[1,2,3,4,5], [2,3,4,5,6]]

        p1 = MathDice.__proba_specific_dices(dices, selec_dices, possibilities[0])
        p2 = MathDice.__proba_specific_dices(dices, selec_dices, possibilities[1])

        return round(p1 + p2, 5) # because P(possibilities) = p1 + p2 - 0

    # def proba_specific(dices, selec_dices, dices_to_find):
    # TODO : will give proba for specific dice (will be useful for (p(s,r|s',a)))


    @staticmethod
    def __proba_specific_4_dices(dices, selec_dices, dices_to_find):
        """dices_to_find is a list of dice you want the probability of having after the next throw, must be length of 4
        and ALL wanted DICES HAVE TO BE DIFFERENT 
        
        only use for the calculation of small straight"""

        list_of_selec_dices = MathDice.find_dices(dices, selec_dices)
        if len(set(dices_to_find))!=4:
            raise ValueError(f"{dices_to_find} isn't a list of 4 differents dices ")
            
        # removing dices we already have
        for dice in list_of_selec_dices:
            if dice in dices_to_find:
                dices_to_find.remove(dice)

        n_to_find = len(dices_to_find)
        n_chances = 5 - len(list_of_selec_dices)
        n_free = n_chances - n_to_find

        # not enough dices left to content expectation
        if n_free < 0:
            return 0

        # otherwise prb with factioal(-1)
        if n_to_find == 0:
            return 1

        # n_free = 1 or 0

        # TO EXPLAIN THE FORMULA
        #
        # different : u know
        # (6-n_to_find)**(n_free) : nb of dices lefts to fill free place and also being
        # *(n_to_find parmi n_chances) : nb of arrangement for the dice to find in between "free dices"
        # * n_to_find! : nb of arrangement for dice known
        #
        # equal :
        # n_free * : if 0 no different possible so 0 arrangement
        # 2 parmi n_chances : the 2 identicals dices arrangement possible inbetween the other dices known
        # *(n_to_find - 1)! nbr of arrangement for the dices diffrents 
        # *4 : the 2 identical dices can be any of them !

        different = (6-n_to_find)**(n_free) * math.comb(n_chances, n_to_find)*math.factorial(n_to_find)
        equal = n_free*(math.comb(n_chances,2)*math.factorial(n_to_find-1))*(n_to_find)
        return (different + equal)/(6**(n_chances))

    @staticmethod
    def small_straight(dices, selec_dices):
        """"""

        p1 = MathDice.__proba_specific_4_dices(dices, selec_dices, [2,3,4,5])
        p2 = MathDice.__proba_specific_4_dices(dices, selec_dices, [1,2,3,4])
        p3 = MathDice.__proba_specific_4_dices(dices, selec_dices, [3,4,5,6])
        
        # formula ez to prove p(a+b+c) = p(a) + p(b + c) -p(a*(b+c))
        return round(p1 + p2 + p3 - MathDice.long_straight(dices, selec_dices), 5)

    @staticmethod
    def every_probability(board, player, dices, selec_dices):
        """ give the expected probabilitu of having it, except for chance and for 1 2 3 5 6 where it's the expected value"""
        score = board.find_score(player)

        for n in range(1,7):
            if score[n]:
                # if you already have unlocked it the proba of having it again is 0
                score[n] = 0
            else:
                score[n] = MathDice.in_a_row(n, dices, selec_dices)

        score[7] = 0 # yes it's weird but normal tqt TODO

        score[8] = 0 if score[8] else sum(MathDice.n_in_a_row(dices, selec_dices, 3))
        score[9] = 0 if score[9] else sum(MathDice.n_in_a_row(dices, selec_dices, 4))
        score[10] = 0 if score[10] else MathDice.full(dices, selec_dices)
        score[11] = 0 if score[11] else MathDice.small_straight(dices, selec_dices)
        score[12] = 0 if score[12] else MathDice.long_straight(dices, selec_dices)
        score[13] = 0 if score[13] else sum(MathDice.n_in_a_row(dices, selec_dices, 5))
        score[14] = 0 if score[14] else 1

        return score
