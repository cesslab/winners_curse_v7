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
    QuestionOneA,
    QuestionOneB,
    Update,
    QuestionTwo,
    QuestionThreeA,
    QuestionThreeB
)
from .constants import Constants

doc = """
Part Three
"""


def creating_session(subsession):
    if subsession.round_number == 1:
        create_player_bid_histories(
            subsession.get_treatment_code(),
            subsession.get_players(),
            subsession.get_lottery_ids(Constants.NUM_LOTTERIES, Constants.PREFIX),
            subsession.session_id,
            Constants.ROUNDS_PER_LOTTERY,
            Phase.QUESTION_PHASE)

        for player in subsession.get_players():
            player.participant.vars['question_phase_payoff_lottery_number'] = random.randint(1, Constants.NUM_LOTTERIES)
            player.participant.vars['question_phase_payoff_lottery_round_number'] = random.randint(1, Constants.ROUNDS_PER_LOTTERY)
            player.participant.vars['question_phase_payoff_question_number'] = random.randint(1, Constants.NUM_QUESTIONS)

    save_bid_history_for_all_players(subsession.get_players(), Constants.ROUNDS_PER_LOTTERY, Phase.QUESTION_PHASE)
    close_db()


class Subsession(BaseSubsession, ExperimentSubSession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer, BidHistoryPlayer):
    min_worth = models.IntegerField(min=0, max=100)
    max_worth = models.IntegerField(min=0, max=100)
    worth = models.IntegerField(min=0, max=100)
    worth_confidence = models.IntegerField(min=0, max=100)
    updated_worth_confidence = models.IntegerField(min=0, max=100)
    updated_min_worth = models.IntegerField(min=0, max=100)
    updated_max_worth = models.IntegerField(min=0, max=100)
    updated_worth = models.IntegerField(min=0, max=100)
    probability_highest_signal = models.IntegerField(min=0, max=100)
    highest_market_signal = models.BooleanField(initial=False)
    confidence_value = models.FloatField(initial=0.0)
    is_payment_round = models.BooleanField(initial=False)
    # Payoff
    prep_worth = models.FloatField()
    prep_emin = models.FloatField()
    prep_emax = models.FloatField()
    prob_computed_loss = models.FloatField()
    computed_loss = models.FloatField()
    random_k = models.IntegerField()
    random_prob_k = models.FloatField()
    # Payoff: Question 3A
    k_3a = models.IntegerField()
    l_3a = models.IntegerField()
    earnings_3a = models.FloatField()
    # Payoff: Question 3B
    computed_3b = models.FloatField()
    earnings_3b = models.FloatField()
    point_earnings = models.FloatField()
    confidence_earnings = models.FloatField()
    prob_earnings = models.FloatField()
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
    highest_other_signal = models.IntegerField()
    rounds_per_lottery = models.IntegerField()
    player_bid_history_id = models.IntegerField()
    part_round_number = models.IntegerField()
    be_bid = models.IntegerField()


page_sequence = [Instructions, QuestionOneA, QuestionOneB, QuestionThreeA, QuestionThreeB, QuestionTwo]
