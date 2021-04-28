import random

from otree.api import Page

from .constants import Constants


class Instructions(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1

    @staticmethod
    def vars_for_template(player):
        return {"treatment": player.session_treatment}


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


class Update(Page):
    @staticmethod
    def is_displayed(player):
        return (
            player.round_number != 1
            and ((player.round_number - 1) % Constants.ROUNDS_PER_LOTTERY) == 0
        )

    @staticmethod
    def vars_for_template(player):
        return {
            "treatment": "cp",
            "rounds_per_lottery": Constants.ROUNDS_PER_LOTTERY,
        }


class Outcome(Page):
    form_model = "player"

    @staticmethod
    def vars_for_template(player):
        earnings = player.ticket_value_after - player.bid
        return {
            "earnings": earnings,
            "player": player,
        }


