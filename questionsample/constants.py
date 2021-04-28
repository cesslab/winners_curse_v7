from otree.api import BaseConstants


class Constants(BaseConstants):
    name_in_url = "questionsample"
    players_per_group = None
    NUM_LOTTERIES = 1
    ROUNDS_PER_LOTTERY = 1
    num_rounds = NUM_LOTTERIES * ROUNDS_PER_LOTTERY
    PART_NUMBER = 2
    MIN_VALUATION = 0
    MAX_VALUATION = 100
