from otree.api import BaseConstants
from exp.constants import ExperimentConstants


class Constants(ExperimentConstants):
    name_in_url = "instructions"
    players_per_group = None
    NUM_LOTTERIES = 3
    ROUNDS_PER_LOTTERY = 2
    num_rounds = NUM_LOTTERIES * ROUNDS_PER_LOTTERY
