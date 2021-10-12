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
    final_payoff_dollars = models.CurrencyField()


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

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        part_one_final_payoff_credits = player.get_part_one_payoff()
        part_two_final_payoff_credits = player.get_part_two_payoff()

        player.payoff = 10.0 + 12.0 + (0.5 * (part_one_final_payoff_credits/6.0) + (0.5 * (part_two_final_payoff_credits/6.0)))
        print(f"saving final payoff of {player.payoff}")


class FinalPayoff(Page):
    @staticmethod
    def vars_for_template(player: Player):
        part_one_final_payoff_credits = player.get_part_one_payoff()
        part_two_final_payoff_credits = player.get_part_two_payoff()

        part_one_final_payoff_dollars = cu(round(part_one_final_payoff_credits/6.0, 2)).to_real_world_currency(player.session)
        part_two_final_payoff_dollars = cu(round(part_two_final_payoff_credits/6.0, 2)).to_real_world_currency(player.session)
        return {
            "payoff_part_1_credits": part_one_final_payoff_credits,
            "payoff_part_1_dollars": part_one_final_payoff_dollars,
            "payoff_part_2_credits": part_two_final_payoff_credits,
            "payoff_part_2_dollars": part_two_final_payoff_dollars,
            "final_payment": player.payoff
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


page_sequence = [QuestionPayoff, BidPayoff, FinalPayoff]
