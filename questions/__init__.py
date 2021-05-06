import random

from otree.api import BaseGroup, BaseSubsession, models, BasePlayer

from exp.models import (
    BidHistoryPlayer,
    save_bid_history_for_all_players,
    ExperimentSubSession,
    create_player_bid_histories,
)

from exp.db import Phase, close_db

from .views import (
    Instructions,
    Worth,
    Update,
    Probability,
    UpdatedWorth,
)
from .constants import Constants

doc = """
Part Three
"""


def creating_session(subsession):
    create_player_bid_histories(subsession, Phase.QUESTION_PHASE)
    save_bid_history_for_all_players(subsession.get_players(), Phase.QUESTION_PHASE)
    if subsession.round_number == 1:
        for player in subsession.get_players():
            player.participant.vars['worth_payoff_lottery_number'] = random.randint(1, Constants.NUM_LOTTERIES)
            player.participant.vars['worth_payoff_lottery_round_number'] = random.randint(1, Constants.ROUNDS_PER_LOTTERY)
    close_db()


class Subsession(BaseSubsession, ExperimentSubSession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer, BidHistoryPlayer):
    min_worth = models.IntegerField(min=0, max=100)
    max_worth = models.IntegerField(min=0, max=100)
    worth = models.IntegerField(min=0, max=100)
    updated_min_worth = models.IntegerField(min=0, max=100)
    updated_max_worth = models.IntegerField(min=0, max=100)
    updated_worth = models.IntegerField(min=0, max=100)
    probability_highest_signal = models.IntegerField(min=0, max=100)
    # Payoff
    prep_worth = models.IntegerField()
    prep_emin = models.IntegerField()
    prep_emax = models.IntegerField()
    computed_loss = models.IntegerField()
    random_k = models.IntegerField()
    point_earnings = models.FloatField()
    confidence_earnings = models.FloatField()
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
    rounds_per_lottery = models.IntegerField()
    player_bid_history_id = models.IntegerField()
    part_round_number = models.IntegerField()
    be_bid = models.IntegerField()


page_sequence = [Instructions, Update, Worth, Probability, UpdatedWorth]
