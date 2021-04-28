from otree.api import BaseGroup, BaseSubsession, models, BasePlayer

from exp.models import (
    BidHistoryPlayer,
    create_player_bid_histories,
    ExperimentSubSession,
    save_bid_history_for_all_players
)


from .views import Instructions
from .constants import Constants

doc = """
Instructions
"""


def creating_session(subsession):
    pass


class Subsession(BaseSubsession, ExperimentSubSession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer, BidHistoryPlayer):
    pass


page_sequence = [Instructions]
