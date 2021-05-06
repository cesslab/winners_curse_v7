import random

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
            "num_rounds": range(1, Constants.ROUNDS_PER_LOTTERY+1),
            "num_lotteries": range(1, Constants.NUM_LOTTERIES+1),
            "min_valuation": Constants.MIN_VALUATION,
            "max_valuation": Constants.MAX_VALUATION,
        }

    @staticmethod
    def before_next_page(player, timeout_happened):
        # PREP WORK
        # Point Belief (Worth)
        if player.is_probability_treatment:
            player.prep_worth = player.ticket_probability * player.fixed_value / 100
        else:
            player.prep_worth = player.ticket_value_before * player.fixed_value / 100

        player.prep_emin = player.fixed_value * player.alpha
        player.prep_emax = player.fixed_value * player.beta
        player.prep_worth = player.be_bid

        player.computed_loss = (player.worth - player.prep_worth)*(player.worth - player.prep_worth)
        player.random_k = random.randint(0, 1296)
        if player.computed_loss < player.random_k:
            player.point_earnings = 12
        else:
            player.point_earnings = 0

        # Confidence Interval
        confidence_value = 12.0*(1.0 - (float(player.max_worth - player.min_worth) / float(player.prep_emax - player.prep_emin)))
        if confidence_value > 0.0 and player.min_worth >= player.prep_worth <= player.max_worth:
            player.confidence_earnings = confidence_value
        else:
            player.confidence_earnings = 0

        if player.lottery_order == player.participant.vars['worth_payoff_lottery_number'] and player.lottery_round_number == player.participant.vars['worth_payoff_lottery_round_number']:
            player.participant.vars['worth_payoff_data'] = {
                "previous_highest_bid": player.previous_highest_bid,
                "fixed_value": player.fixed_value,
                "alpha": player.alpha,
                "beta": player.beta,
                "epsilon": player.epsilon,
                "signal": player.signal,
                "treatment": player.treatment,
                "point_earnings": player.point_earnings,
                "confidence_interval_earnings": player.confidence_earnings,
                "lottery_order": player.lottery_order,
                "lottery_round_number": player.lottery_round_number,
                "ticket_value_after": player.ticket_value_after,
                "ticket_value_before": player.ticket_value_before,
                "ticket_probability": player.ticket_probability,
                "prep_worth": player.prep_worth,
                "random_k": player.random_k,
                "computed_loss": player.computed_loss,
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
            "num_rounds": range(1, Constants.ROUNDS_PER_LOTTERY+1),
            "num_lotteries": range(1, Constants.NUM_LOTTERIES+1),
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
            "num_rounds": range(1, Constants.ROUNDS_PER_LOTTERY+1),
            "num_lotteries": range(1, Constants.NUM_LOTTERIES+1),
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
