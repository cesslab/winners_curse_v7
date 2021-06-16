from otree.api import *

from exp.models import (
    BidHistoryPlayer,
)

doc = """
Venmo Payment
"""


class Constants(BaseConstants):
    name_in_url = 'venmo'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer, BidHistoryPlayer):
    pass


# PAGES
class VenmoPayment(Page):
    @staticmethod
    def vars_for_template(player):
        p1_payoff = player.participant.vars['bid_payoff_data']['earnings']
        if player.payoff_question_number == 1:
            p2_payoff = player.participant.vars['q1_data']['earnings_q1']
        elif player.payoff_question_number == 2:
            p2_payoff = player.participant.vars['q3_data']['earnings_q3']
        else:
            # TODO: replace prob_earnings with earnings_q2
            p2_payoff = player.participant.vars['q2_data']['prob_earnings']

        final_payoff = 10 + 12 + 0.5 * (p1_payoff/6.0) + 0.5 * (p2_payoff/6.0)

        p1_dollars = cu(p1_payoff).to_real_world_currency(player.session)
        p2_dollars = cu(p2_payoff).to_real_world_currency(player.session)
        payoff_dollars = 10 + 12 + 0.5 * p1_dollars + 0.5 * p2_dollars
        return {
            "esid": player.subsession.session.id,
            "pid": player.participant.id,
            "po": round(final_payoff, 2),
            "payoff": payoff_dollars
        }


page_sequence = [VenmoPayment]
