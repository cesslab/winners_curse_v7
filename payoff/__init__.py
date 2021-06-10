from otree.api import *

from exp.models import (
    BidHistoryPlayer,
)

c = Currency

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'payoff'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer, BidHistoryPlayer):
    pass


# PAGES
class BidPayoff(Page):
    @staticmethod
    def vars_for_template(player):
        return player.participant.vars['bid_payoff_data']


class QuestionPayoff(Page):
    @staticmethod
    def vars_for_template(player):
        question_number = player.participant.vars['worth_payoff_question_number']
        if question_number == 1:
            payoff_data = player.participant.vars['q1_data']
        elif question_number == 2:
            payoff_data = player.participant.vars['q3_data']
        else:
            payoff_data = player.participant.vars['q2_data']

        return {
            "question_number": question_number,
            "selected_value_text": player.selected_value_text,
            **payoff_data,
        }


class QuestionPayoffDebug(Page):
    @staticmethod
    def vars_for_template(player):
        question_number = player.participant.vars['worth_payoff_question_number']
        return {
            "question_number": question_number,
            **player.participant.vars['q1_data'],
            **player.participant.vars['q2_data'],
            **player.participant.vars['q3_data'],
        }


page_sequence = [BidPayoff, QuestionPayoff, QuestionPayoffDebug]
