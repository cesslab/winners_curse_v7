from otree.api import BaseConstants

from exp.constants import ExperimentConstants


class Constants(ExperimentConstants):
    name_in_url = "valuation"
    players_per_group = None
    PART_NUMBER = 2
    MIN_VALUATION = 0
    MAX_VALUATION = 100
