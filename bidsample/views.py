import random

from otree.api import Page

from bid.constants import Constants


class Instructions(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1

    @staticmethod
    def vars_for_template(player):
        return {"treatment": player.subsession.session.config["treatment"]}


class Bid(Page):
    form_model = "player"
    form_fields = ["bid"]

    @staticmethod
    def vars_for_template(player):
        return {
            "player": player,
            "min_valuation": Constants.MIN_VALUATION,
            "max_valuation": Constants.MAX_VALUATION,
        }

    @staticmethod
    def before_next_page(player, timeout_happened):
        if player.bid > player.previous_highest_bid:
            player.tie = False
            player.winner = True
        elif player.bid < player.previous_highest_bid:
            player.tie = False
            player.winner = False
        else:
            player.tie = True
            player.winner = random.choice([True, False])


class Outcome(Page):
    form_model = "player"

    @staticmethod
    def vars_for_template(player):
        return {
            "player": player,
        }


