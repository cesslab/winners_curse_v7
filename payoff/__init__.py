from otree.api import *

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


class Player(BasePlayer):
    pass


# PAGES
class BidPayoff(Page):
    @staticmethod
    def vars_for_template(player):
        return player.participant.vars['bid_payoff_data']


class QuestionPayoff(Page):
    @staticmethod
    def vars_for_template(player):
        return {
            **player.participant.vars['q1_data'],
            **player.participant.vars['q2_data'],
            **player.participant.vars['q3a_data'],
            **player.participant.vars['q3b_data'],
        }


page_sequence = [BidPayoff, QuestionPayoff]
