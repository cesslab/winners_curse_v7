import random

from otree.api import Page


class Instructions(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1

    @staticmethod
    def vars_for_template(player):
        return {"treatment": player.session_treatment}


class Outcome(Page):
    form_model = "player"

    @staticmethod
    def vars_for_template(player):
        return {
            "player": player,
        }


