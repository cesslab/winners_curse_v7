from otree.api import Page

from .constants import Constants


class Instructions(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1

    @staticmethod
    def vars_for_template(player):
        return {"treatment": player.subsession.session.config["treatment"]}


class Worth(Page):
    form_model = "player"
    form_fields = ["worth", "min_worth", "max_worth"]

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


class Probability(Page):
    form_model = "player"
    form_fields = ["probability_highest_signal"]

    @staticmethod
    def vars_for_template(player):
        return {
            "player": player,
            "min_valuation": Constants.MIN_VALUATION,
            "max_valuation": Constants.MAX_VALUATION,
        }


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


class UpdatedWorth(Page):
    form_model = "player"
    form_fields = ["updated_worth", "updated_min_worth", "updated_max_worth"]

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
        return (
            player.round_number != 1
            and ((player.round_number - 1) % Constants.ROUNDS_PER_LOTTERY) == 0
        )

    @staticmethod
    def vars_for_template(player):
        return {
            "player": player,
            "rounds_per_lottery": Constants.ROUNDS_PER_LOTTERY,
        }
