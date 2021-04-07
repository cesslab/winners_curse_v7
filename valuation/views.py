from otree.api import Page

from .constants import Constants


class Instructions(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1

    @staticmethod
    def vars_for_template(player):
        return {"treatment": player.subsession.session.config["treatment"]}


class LotteryValuation(Page):
    form_model = "player"
    form_fields = ["valuation", "min_worth", "max_worth"]

    @staticmethod
    def vars_for_template(player):

        return {
            "player": player,
            "min_valuation": Constants.MIN_VALUATION,
            "max_valuation": Constants.MAX_VALUATION,
        }

    @staticmethod
    def js_vars(player):
        pass
        return dict(
            lottery_max_value=player.lottery_max_value,
            mapping_divisor=player.fixed_value,
            is_probability_treatment=player.is_probability_treatment,
        )


class Update(Page):
    @staticmethod
    def is_displayed(player):
        return ((player.round_number - 1) % Constants.ROUNDS_PER_LOTTERY) == 0

    @staticmethod
    def vars_for_template(player):
        return {
            "treatment": "cp",
            "rounds_per_lottery": Constants.ROUNDS_PER_LOTTERY,
        }
