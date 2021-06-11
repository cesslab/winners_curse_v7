from otree.api import *

c = Currency

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'quiz'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    q1 = models.IntegerField(
        choices=[[1, 'Your bid'], [2, 'The highest bid'], [3, 'Nothing']],
        widget=widgets.RadioSelect
    )
    q2 = models.IntegerField(
        choices=[
            [1, 'All four bidders bid for the same lottery ticket with the same Selected Probability.'],
            [2, 'All four bidders bid for lottery tickets with different Selected Probabilities.'],
            [3, 'All four bidders bid for lottery tickets with possibly different Selected Probabilities.']],
        widget=widgets.RadioSelect
    )
    q3 = models.IntegerField(
        choices=[
            [1, 'All four bidders receive the same signal about the same Selected Probability.'],
            [2, 'All four bidders receive possibly different signals about the same Selected Probability.'],
            [3, 'All four bidders receive different signals because Selected Proba- bilities differ for each of them.']],
        widget=widgets.RadioSelect
    )
    q4 = models.IntegerField(
        choices=[
            [1, 'The non-zero value of the lottery minus your bid.'],
            [2, 'The outcome of the lottery minus your bid.']],
        widget=widgets.RadioSelect
    )
    q5 = models.IntegerField(
        choices=[
            [1, '18%'],
            [2, '28%'],
            [3, '48%']],
        widget=widgets.RadioSelect
    )
    q6 = models.IntegerField(
        choices=[
            [1, 'can only be 70'],
            [2, '21 ( = 30% x 70 + 70% x 0)'],
            [3, 'can be 0 or 70']],
        widget=widgets.RadioSelect
    )


# PAGES
class Instructions(Page):
    pass

class Quiz(Page):
    form_model = 'player'
    form_fields = ['q1', 'q2', 'q3', 'q4', 'q5', 'q6']


page_sequence = [Instructions, Quiz]
