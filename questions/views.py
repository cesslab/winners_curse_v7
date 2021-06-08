import random

import ibis
from pathlib import Path

from otree.api import Page

from .constants import Constants


class Instructions(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1

    @staticmethod
    def vars_for_template(player):
        return {
            "player": player,
            "treatment": player.subsession.session.config["treatment"],
        }


class QuestionOneA(Page):
    form_model = "player"
    form_fields = ["worth"]

    @staticmethod
    def vars_for_template(player):
        return {
            "player": player,
            "num_rounds": range(1, Constants.ROUNDS_PER_LOTTERY+1),
            "num_lotteries": range(1, Constants.NUM_LOTTERIES+1),
            "min_valuation": Constants.MIN_VALUATION,
            "max_valuation": Constants.MAX_VALUATION,
            "new_lottery":
                (
                    player.round_number != 1
                    and ((player.round_number - 1) % Constants.ROUNDS_PER_LOTTERY) == 0
                )
        }

    @staticmethod
    def js_vars(player):
        loader = ibis.loaders.FileLoader(Path(__file__).parent)
        return dict(
            display_intro=(player.round_number == 1),
            lottery_max_value=player.lottery_max_value,
            mapping_divisor=player.fixed_value,
            is_probability_treatment=player.is_probability_treatment,
            is_cv_treatment=player.is_value_treatment,
            selected_value_text=player.selected_value_text,
            lottery_worth=loader('LotteryWorthIntro.html').render({"player": player}),
            your_task=loader('YourTaskIntro.html').render({"player": player}),
            instructions_for_slider=loader('InstructionsForSliderIntro.html').render({"player": player}),
        )




class QuestionOneB(Page):
    form_model = "player"
    form_fields = ["worth", "min_worth", "max_worth", "worth_confidence"]

    @staticmethod
    def vars_for_template(player):
        return {
            "player": player,
            "num_rounds": range(1, Constants.ROUNDS_PER_LOTTERY+1),
            "num_lotteries": range(1, Constants.NUM_LOTTERIES+1),
            "min_valuation": Constants.MIN_VALUATION,
            "max_valuation": Constants.MAX_VALUATION,
            "new_lottery":
                (
                    player.round_number != 1
                    and ((player.round_number - 1) % Constants.ROUNDS_PER_LOTTERY) == 0
                )
        }

    @staticmethod
    def error_message(player, values):
        if values["min_worth"] > values["worth"] or values["max_worth"] < values["worth"]:
            return f"Invalid values entered."


    @staticmethod
    def before_next_page(player, timeout_happened):
        # PREP WORK
        # Worth = vLotto *fix (in CV) or pLotto * fix (in CP)
        if player.is_probability_treatment:
            player.prep_worth = player.ticket_probability * player.fixed_value / 100
        else:
            player.prep_worth = player.ticket_value_before * player.fixed_value / 100

        #  Emin = fix * alpha
        #  Emax = fix * beta
        player.prep_emin = player.fixed_value * player.alpha / 100
        player.prep_emax = player.fixed_value * player.beta / 100

        # ---------------------------------------------------------------------
        # Question 1a: point belief about worth of the lottery (unconditional)
        # ---------------------------------------------------------------------
        # Computer computes loss function L= (X-worth)^2
        player.computed_loss = float((player.worth - player.prep_worth)**2)
        # Computer draws random number K ~ U[0,1296]
        player.random_k = random.randint(0, 1296)
        # Computer pays 12 credits if L<K ; 0 otherwise (in particular if L>1296)
        is_guess_sufficiently_close_to_worth = player.computed_loss < player.random_k
        if is_guess_sufficiently_close_to_worth:
            player.point_earnings = 12
        else:
            player.point_earnings = 0

        # ---------------------------------------------------------------------
        # Question 1b: confidence interval about worth of the lottery
        # ---------------------------------------------------------------------
        # Computer computes 12*[1- (u-l)/(Emax-Emin)] if positive and worth in [l,u] (worth is in interval); 0 otherwise
        player.confidence_value = 12.0*(1.0 - (float(player.max_worth - player.min_worth) / float(player.prep_emax - player.prep_emin)))
        is_worth_within_interval = player.min_worth >= player.prep_worth <= player.max_worth
        if player.confidence_value > 0.0 and is_worth_within_interval:
            player.confidence_earnings = player.confidence_value
        else:
            player.confidence_earnings = 0

        if player.lottery_order == player.participant.vars['worth_payoff_lottery_number'] and player.lottery_round_number == player.participant.vars['worth_payoff_lottery_round_number']:
            player.participant.vars['q1_data'] = {
                "previous_highest_bid": player.previous_highest_bid,
                "fixed_value": player.fixed_value,
                "alpha": player.alpha,
                "beta": player.beta,
                "prep_emax": player.prep_emax,
                "prep_emin": player.prep_emin,
                "epsilon": player.epsilon,
                "signal": player.signal,
                "treatment": player.treatment,
                "earnings_q1a": player.point_earnings,
                "max_worth": player.max_worth,
                "min_worth": player.min_worth,
                "worth": player.worth,
                "earnings_q1b": player.confidence_earnings,
                "earnings_q1": player.point_earnings + player.confidence_earnings,
                "is_worth_within_interval": is_worth_within_interval,
                "lottery_order": player.lottery_order,
                "lottery_round_number": player.lottery_round_number,
                "ticket_value_after": player.ticket_value_after,
                "ticket_value_before": player.ticket_value_before,
                "ticket_probability": player.ticket_probability,
                "prep_worth": player.prep_worth,
                "random_k": player.random_k,
                "computed_loss": player.computed_loss,
                "confidence_value": player.confidence_value,
                "is_probability_treatment": player.is_probability_treatment,
                "is_guess_sufficiently_close_to_worth": is_guess_sufficiently_close_to_worth,
            }

    @staticmethod
    def js_vars(player):
        loader = ibis.loaders.FileLoader(Path(__file__).parent)
        return dict(
            display_intro=(player.round_number == 1),
            worth=player.worth,
            lottery_max_value=player.lottery_max_value,
            mapping_divisor=player.fixed_value,
            is_probability_treatment=player.is_probability_treatment,
            is_cv_treatment=player.is_value_treatment,
            selected_value_text=player.selected_value_text,
            interval=loader('IntervalIntro.html').render({"player": player}),
            interval_limits=loader('IntervalLimitsIntro.html').render({"player": player}),
            confidence_level=loader('ConfidenceLevelIntro.html').render({"player": player}),
        )


class QuestionTwo(Page):
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

    @staticmethod
    def before_next_page(player, timeout_happened):
        # ---------------------------------------------------------------------
        # Question 2: point belief about probability of having the highest signal
        # ---------------------------------------------------------------------
        # Computer checks: is signal highest in market? Define variable Highest: 1=yes; 0=no
        highest = 1 if player.highest_market_signal else 0
        # Computer computes loss function: L=(Highest – p/100)^2
        player.prob_computed_loss = (highest - player.probability_highest_signal/100.0)*(highest - player.probability_highest_signal/100.0)
        # Computer draws random number K ~ U[0,1]
        player.random_prob_k = random.uniform(0, 1)
        # Computer pays 24 credits if L < K; 0 otherwise
        player.prob_earnings = 24 if player.prob_computed_loss < player.random_prob_k else 0

        if player.lottery_order == player.participant.vars['worth_payoff_lottery_number'] and player.lottery_round_number == player.participant.vars['worth_payoff_lottery_round_number']:
            player.participant.vars['q2_data'] = {
                "highest": highest,
                "highest_market_signal": player.highest_market_signal,
                "random_prob_k": player.random_prob_k,
                "prob_earnings": player.prob_earnings,
                "probability_highest_signal": player.probability_highest_signal,
                "prob_computed_loss": player.prob_computed_loss
            }

    @staticmethod
    def js_vars(player):
        loader = ibis.loaders.FileLoader(Path(__file__).parent)
        return dict(
            display_intro=(player.round_number == 1),
            lottery_max_value=player.lottery_max_value,
            mapping_divisor=player.fixed_value,
            is_probability_treatment=player.is_probability_treatment,
            is_cv_treatment=player.is_value_treatment,
            selected_value_text=player.selected_value_text,
            your_task=loader('YourTaskProbabilityIntro.html').render({"player": player}),
        )


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


class QuestionThreeA(Page):
    form_model = "player"
    form_fields = ["updated_worth"]

    @staticmethod
    def vars_for_template(player):
        return {
            "player": player,
            "num_rounds": range(1, Constants.ROUNDS_PER_LOTTERY+1),
            "num_lotteries": range(1, Constants.NUM_LOTTERIES+1),
            "min_valuation": Constants.MIN_VALUATION,
            "max_valuation": Constants.MAX_VALUATION,
            "new_lottery":
                (
                    player.round_number != 1
                    and ((player.round_number - 1) % Constants.ROUNDS_PER_LOTTERY) == 0
                )
        }

    @staticmethod
    def js_vars(player):
        loader = ibis.loaders.FileLoader(Path(__file__).parent)
        return dict(
            display_intro=(player.round_number == 1),
            lottery_max_value=player.lottery_max_value,
            mapping_divisor=player.fixed_value,
            is_probability_treatment=player.is_probability_treatment,
            is_cv_treatment=player.is_value_treatment,
            selected_value_text=player.selected_value_text,
            your_task=loader('YourTaskHighestSignalIntro.html').render({"player": player}),
        )


class QuestionThreeB(Page):
    form_model = "player"
    form_fields = ["updated_worth_confidence", "updated_worth", "updated_min_worth", "updated_max_worth"]

    @staticmethod
    def vars_for_template(player):
        return \
        {
            "player": player,
            "num_rounds": range(1, Constants.ROUNDS_PER_LOTTERY+1),
            "num_lotteries": range(1, Constants.NUM_LOTTERIES+1),
            "min_valuation": Constants.MIN_VALUATION,
            "max_valuation": Constants.MAX_VALUATION,
            "new_lottery":
                (
                    player.round_number != 1
                    and ((player.round_number - 1) % Constants.ROUNDS_PER_LOTTERY) == 0
                )
        }

    @staticmethod
    def error_message(player, values):
        if values["updated_min_worth"] > values["updated_worth"] or values["updated_max_worth"] < values["updated_worth"]:
            return f"Invalid values entered."



    @staticmethod
    def before_next_page(player, timeout_happened):
        # ---------------------------------------------------------------------
        # Question 3a: point belief about conditional worth of the lottery.
        # ---------------------------------------------------------------------
        # Prep Work
        cworth = player.be_bid
        # subject enters Cx (updated_worth)
        cx = player.updated_worth
        # Computer computes loss function L= (Cx-Cworth)^2
        l_3a = (cx - cworth)**2
        k_3a = random.randint(0, 1296)
        # Computer pays 12 credits if L<K ; 0 otherwise (in particular if L>1296).
        guess_sufficiently_close_to_estimate = l_3a < k_3a
        if guess_sufficiently_close_to_estimate:
            earnings_3a = 12
        else:
            earnings_3a = 0

        player.l_3a = l_3a
        player.k_3a = k_3a
        player.earnings_3a = earnings_3a
        player.participant.vars['q3a_data'] = {
            "cworth": cworth,
            "cx": cx,
            "l_3a": l_3a,
            "k_3a": k_3a,
            "earnings_3a": earnings_3a,
            "updated_worth": player.updated_worth,
            "guess_sufficiently_close_to_estimate": guess_sufficiently_close_to_estimate,

        }
        # ---------------------------------------------------------------------
        # Question 3b: confidence interval about conditional worth of the lottery.
        # ---------------------------------------------------------------------
        # cl for lower boundary and cu for upper boundary
        cl = player.updated_min_worth
        cu = player.updated_max_worth
        emax = player.prep_emax
        emin = player.prep_emin
        # Computer computes 12*[1- (cu-cl)/(Emax-Emin)] if positive and worth in [cl,cu] (Cworth is in interval); 0 otherwise
        computed_3b = 12.0*(1.0 - float(cu-cl)/float(emax-emin))
        guess_within_chosen_interval = cl <= cworth <= cu
        if computed_3b > 0 and guess_within_chosen_interval:
            earnings_3b = computed_3b
        else:
            earnings_3b = 0

        player.computed_3b = computed_3b
        player.earnings_3b = earnings_3b
        player.participant.vars['q3b_data'] = {
            "cworth": cworth,
            "cx": cx,
            "cu": cu,
            "cl": cl,
            "computed_3b": computed_3b,
            "l_3a": l_3a,
            "k_3a": k_3a,
            "earnings_3b": earnings_3b,
            "updated_min_worth": player.updated_min_worth,
            "updated_max_worth": player.updated_max_worth,
            "earnings_q3": earnings_3a + earnings_3b,
            "guess_within_chosen_interval": guess_within_chosen_interval,
        }

    @staticmethod
    def js_vars(player):
        loader = ibis.loaders.FileLoader(Path(__file__).parent)
        return dict(
            display_intro=(player.round_number == 1),
            worth=player.updated_worth,
            lottery_max_value=player.lottery_max_value,
            mapping_divisor=player.fixed_value,
            is_probability_treatment=player.is_probability_treatment,
            is_cv_treatment=player.is_value_treatment,
            selected_value_text=player.selected_value_text,
            interval=loader('IntervalHighestSignalIntro.html').render({"player": player}),
            confidence_level=loader('ConfidenceLevelHighestSignalIntro.html').render({"player": player}),
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
