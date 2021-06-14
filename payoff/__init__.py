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
        if player.payoff_question_number == 1:
            payoff_data = player.question_one_data
        elif player.payoff_question_number == 2:
            payoff_data = player.question_three_data
        else:
            payoff_data = player.question_two_data

        return {
            "selected_value_text": player.selected_value_text,
            **payoff_data,
            "question_number": player.payoff_question_number,
        }


class FinalPayoff(Page):
    @staticmethod
    def vars_for_template(player: Player):
        part_one_final_payoff_credits = player.participant.vars['bid_payoff_data']['earnings']
        if player.payoff_question_number == 1:
            part_two_final_payoff_credits = player.participant.vars['q1_data']['earnings_q1']
        elif player.payoff_question_number == 2:
            part_two_final_payoff_credits = player.participant.vars['q3_data']['earnings_q3']
        else:
            # TODO: replace prob_earnings with earnings_q2
            part_two_final_payoff_credits = player.participant.vars['q2_data']['prob_earnings']

        return {
            "payoff_part_1": cu(part_one_final_payoff_credits).to_real_world_currency(player.session),
            "payoff_part_2": cu(part_two_final_payoff_credits).to_real_world_currency(player.session),
            "final_payment": 10 + 12 + 0.5 * part_one_final_payoff_credits + 0.5 * part_two_final_payoff_credits,
        }


class QuestionPayoffDebug(Page):
    @staticmethod
    def vars_for_template(player):
        part_one_payoff_data = player.participant.vars['bid_payoff_data']
        if player.payoff_question_number == 1:
            part_two_payoff_data = player.question_one_data
        elif player.payoff_question_number == 2:
            part_two_payoff_data = player.question_three_data
        else:
            part_two_payoff_data = player.question_two_data

        return {
            "selected_value_text": player.selected_value_text,
            **part_one_payoff_data,
            **part_two_payoff_data,
            "question_number": player.payoff_question_number,
        }


page_sequence = [BidPayoff, QuestionPayoff, FinalPayoff, QuestionPayoffDebug]
