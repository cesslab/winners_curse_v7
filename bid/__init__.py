import random

from otree.api import BaseGroup, BaseSubsession, models, BasePlayer

from exp.models import (
    BidHistoryPlayer,
    save_bid_history_for_all_players,
    create_player_bid_histories,
    ExperimentSubSession,
)


from exp.db import close_db, Phase

from .views import Instructions, Update, Bid, Outcome
from .constants import Constants

doc = """
Part One
"""


def creating_session(subsession):
    create_player_bid_histories(subsession, Phase.BID_PHASE)
    save_bid_history_for_all_players(subsession.get_players(), Phase.BID_PHASE)
    if subsession.round_number == 1:
        for player in subsession.get_players():
            player.participant.vars['payoff_lottery_number'] = random.randint(1, Constants.NUM_LOTTERIES)
            player.participant.vars['payoff_lottery_round_number'] = random.randint(1, Constants.ROUNDS_PER_LOTTERY)
    close_db()


class Subsession(BaseSubsession, ExperimentSubSession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer, BidHistoryPlayer):
    bid = models.IntegerField(min=0, max=100)
    tie = models.BooleanField(initial=False)
    win_tie_break = models.BooleanField(initial=False)
    winner = models.BooleanField(initial=False)
    earnings = models.IntegerField()
    new_highest_bid = models.IntegerField()
    highest_market_signal = models.BooleanField(initial=False)

    payoff_round = models.BooleanField(initial=False)
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
    previous_highest_signal = models.IntegerField()
    # Player Bid History
    highest_other_signal = models.IntegerField()
    rounds_per_lottery = models.IntegerField()
    player_bid_history_id = models.IntegerField()
    part_round_number = models.IntegerField()
    be_bid = models.IntegerField()


page_sequence = [Instructions, Bid, Outcome]
