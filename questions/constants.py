from otree.api import BaseConstants


class Constants(BaseConstants):
    name_in_url = "questions"
    players_per_group = None
    NUM_LOTTERIES = 3
    ROUNDS_PER_LOTTERY = 2
    num_rounds = NUM_LOTTERIES * ROUNDS_PER_LOTTERY
    PART_NUMBER = 2
    PART_ONE = 1
    MIN_VALUATION = 0
    MAX_VALUATION = 100
