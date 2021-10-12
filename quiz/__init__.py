from otree.api import *

from exp.models import BidHistoryPlayer

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


class Player(BasePlayer, BidHistoryPlayer):
    cp_q1 = models.IntegerField(
        label='1. Suppose that you receive a signal 30 that is at most 4 percentage points away from the Selected Probability. What could be the Selected Probability?',
        choices=[
            [1, '18%'],
            [2, '28%'],
            [3, '38%']],
        widget=widgets.RadioSelect
    )
    cv_q1 = models.IntegerField(
        label='1. Suppose that you receive a signal of 30 that is at most 4 units away from the Selected Value. What could be the Selected Value?',
        choices=[
            [1, '18'],
            [2, '28'],
            [3, '38']],
        widget=widgets.RadioSelect
    )

    cp_q2 = models.IntegerField(
        label='2. Suppose the Selected Probability is 30%. The outcome of the lottery in credits...',
        choices=[
            [1, 'can only be 70'],
            [2, '21 ( = 30% x 70 + 70% x 0)'],
            [3, 'can be 0 or 70']],
        widget=widgets.RadioSelect
    )
    cv_q2 = models.IntegerField(
        label='2. Suppose the Selected Value is 30.The outcome of the lottery in credits...',
        choices=[
            [1, 'can only be 30'],
            [2, '21 ( = 30 x 70% +  0 x 30%)'],
            [3, 'can be 0 or 30']],
        widget=widgets.RadioSelect
    )
    q3 = models.IntegerField(
        label='3. Which of the following alternatives is correct?',
        choices=[
            [1, 'There will be four signals, but you will see none of them.'],
            [2, 'There will be four signals, but you will see only one of them.'],
            [3, 'There will be four signals, but you will see only two of them.'],
            [4, 'You will see four signals.']],
        widget=widgets.RadioSelect
    )

    cp_q4 = models.IntegerField(
        label='4. Which of the following alternatives is correct?',
        choices=[
            [1, 'The four signals are all the same, so if you see one of them, you know all of them.'],
            [2, 'All four signals are possibly different but contain information about the same Selected Probability.'],
            [3, 'The four signals are all different because each one of them is about a different Selected Probability.']],
        widget=widgets.RadioSelect
    )
    cv_q4 = models.IntegerField(
        label='4. Which of the following alternatives is correct?',
        choices=[
            [1, 'The four signals are all the same, so if you see one of them, you know all of them.'],
            [2,
             'All four signals are possibly different but contain information about the same Selected Value.'],
            [3,
             'The four signals are all different because each one of them is about a different Selected Value.']],
        widget=widgets.RadioSelect
    )

    signal = models.IntegerField(initial=30)
    alpha = models.IntegerField(initial=20)
    beta = models.IntegerField(initial=40)
    epsilon = models.IntegerField(initial=4)
    ticket_value_before = models.IntegerField(initial=0)
    ticket_probability = models.IntegerField(initial=70)
    fixed_value = models.IntegerField(initial=70)
    ticket_value_after = models.IntegerField(initial=0)


# PAGES
class Quiz(Page):
    form_model = 'player'

    @staticmethod
    def get_form_fields(player: Player):
        if player.is_value_treatment:
            return ['cv_q1', 'cv_q2', 'q3', 'cv_q4']
        else:
            return ['cp_q1', 'cp_q2', 'q3', 'cp_q4']

Error_Message = 'Incorrect answer. If you do not understand why your answer is wrong, please send a private message to the experimenter.'


def q1_error_message(value):
    if value != 2:
        return Error_Message


def q2_error_message(value):
    if value != 3:
        return Error_Message


def q3_error_message(player, value):
    if value != 2:
        return Error_Message


def q4_error_message(value):
    if value != 2:
        return Error_Message


def cv_q1_error_message(player: Player, value):
    return q1_error_message(value)


def cp_q1_error_message(player: Player, value):
    return q1_error_message(value)


def cv_q2_error_message(player: Player, value):
    return q2_error_message(value)


def cp_q2_error_message(player: Player, value):
    return q2_error_message(value)


def cv_q4_error_message(player: Player, value):
    return q4_error_message(value)


def cp_q4_error_message(player: Player, value):
    return q4_error_message(value)


page_sequence = [Quiz]
