from otree.api import BaseConstants


class ExperimentConstants(BaseConstants):
    NUM_LOTTERIES = 3
    ROUNDS_PER_LOTTERY = 2
    num_rounds = NUM_LOTTERIES * ROUNDS_PER_LOTTERY

