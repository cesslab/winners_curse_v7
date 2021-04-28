from otree.api import *

from exp.models import (
    BidHistoryPlayer,
)

from .views import Instructions, Outcome
from bid.views import Bid

c = Currency

doc = """
Your app description
"""


def creating_session(subsession):
    for player in subsession.get_players():
        player.treatment = player.session_treatment


class Constants(BaseConstants):
    name_in_url = 'bidsample'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer, BidHistoryPlayer):
    bid = models.IntegerField(min=0, max=100)
    tie = models.BooleanField()
    winner = models.BooleanField()
    # Bid History
    bid_history_id = models.IntegerField(initial=0)
    previous_session_id = models.IntegerField(initial=0)
    lottery_id = models.IntegerField(initial=0)
    treatment = models.StringField(choices=["cp", "cv"])
    lottery_round_number = models.IntegerField(initial=1)
    lottery_order = models.IntegerField(initial=1)
    others_group_id = models.IntegerField(initial=1)
    others_player_id = models.IntegerField(initial=1)
    others_bid = models.IntegerField(initial=50)
    signal = models.IntegerField(initial=23)
    alpha = models.IntegerField(initial=10)
    beta = models.IntegerField(initial=30)
    epsilon = models.IntegerField(initial=4)
    ticket_value_before = models.IntegerField(initial=0)
    ticket_probability = models.IntegerField(initial=75)
    fixed_value = models.IntegerField(initial=75)
    ticket_value_after = models.IntegerField(initial=0)
    previous_highest_bid = models.IntegerField(initial=0)
    # Player Bid History
    rounds_per_lottery = models.IntegerField(initial=1)
    player_bid_history_id = models.IntegerField(initial=0)
    part_round_number = models.IntegerField(initial=0)


page_sequence = [Instructions, Bid, Outcome]
