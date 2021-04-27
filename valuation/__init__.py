from otree.api import BaseGroup, BaseSubsession, models, BasePlayer

from exp.models import (
    BidHistoryPlayer,
    save_bid_history_for_all_players,
    create_player_bid_histories,
    ExperimentSubSession,
)

from exp.db import Phase, close_db

from .views import Instructions, LotteryValuation, Update
from .constants import Constants


doc = """
Part Two
"""


def creating_session(subsession):
    create_player_bid_histories(subsession, Phase.VALUATION_PHASE)
    save_bid_history_for_all_players(subsession.get_players(), Phase.VALUATION_PHASE)
    close_db()


class Subsession(BaseSubsession, ExperimentSubSession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer, BidHistoryPlayer):
    min_worth = models.IntegerField(min=0, max=100)
    max_worth = models.IntegerField(min=0, max=100)
    valuation = models.IntegerField(min=0, max=100)
    # Bid History
    bid_history_id = models.IntegerField()
    previous_session_id = models.IntegerField()
    lottery_id = models.IntegerField()
    treatment = models.StringField(choices=["cp", "cv"])
    lottery_round_number = models.IntegerField()
    lottery_order = models.IntegerField()
    others_group_id = models.IntegerField()
    others_player_id = models.IntegerField()
    others_bid = models.IntegerField()
    signal = models.IntegerField()
    alpha = models.IntegerField()
    beta = models.IntegerField()
    epsilon = models.IntegerField()
    ticket_value_before = models.IntegerField()
    ticket_probability = models.IntegerField()
    fixed_value = models.IntegerField()
    ticket_value_after = models.IntegerField()
    previous_highest_bid = models.IntegerField()
    # Player Bid History
    player_bid_history_id = models.IntegerField()
    part_round_number = models.IntegerField()
    rounds_per_lottery = models.IntegerField()


page_sequence = [Instructions, Update, LotteryValuation]
