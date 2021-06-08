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
            payoff_data = player.participant.vars['q2_data']
        else:
            payoff_data = {**player.participant.vars['q3a_data'], **player.participant.vars['q3b_data']}

        return {
            "question_number": question_number,
            **player.participant.vars['q1_data'],
            **player.participant.vars['q2_data'],
            **player.participant.vars['q3a_data'],
            **player.participant.vars['q3b_data'],
            "selected_value_text": player.selected_value_text,
        }
        # return {
        #     "selected_value_text": player.selected_value_text,
        #     "selected_lottery_number": player.participant.vars['worth_payoff_lottery_number'],
        #     "selected_round": player.participant.vars['worth_payoff_lottery_round_number'],
        #     "question_number": question_number,
        #     "lottery_round_number": player.participant.vars['q1_data']['lottery_round_number'],
        #     "lottery_order": player.participant.vars['q1_data']['lottery_order'],
        #     "treatment": player.participant.vars['q1_data']['treatment'],
        #     "ticket_value_before": player.participant.vars['q1_data']['ticket_value_before'],
        #     "ticket_value_after": player.participant.vars['q1_data']['ticket_value_after'],
        #     "fixed_value": player.participant.vars['q1_data']['fixed_value'],
        #     "prep_worth": player.participant.vars['q1_data']['prep_worth'],
        #     **payoff_data,
        # }


class QuestionPayoffDebug(Page):
    @staticmethod
    def vars_for_template(player):
        question_number = player.participant.vars['worth_payoff_question_number']
        return {
            "question_number": question_number,
            **player.participant.vars['q1_data'],
            **player.participant.vars['q2_data'],
            **player.participant.vars['q3a_data'],
            **player.participant.vars['q3b_data'],
        }


page_sequence = [BidPayoff, QuestionPayoff, QuestionPayoffDebug]
