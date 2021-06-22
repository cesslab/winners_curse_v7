import random

import ibis
from pathlib import Path

from otree.api import Page, cu

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
    form_fields = ["worth", "min_worth", "max_worth"]

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
        MAX_DISTANCE = 1296
        # Computer computes loss function L= (X-worth)^2
        player.computed_loss = float((player.worth - player.prep_worth)**2)
        # Computer draws random number K ~ U[0,1296]
        player.random_k = random.randint(0, MAX_DISTANCE)
        # Computer pays 12 credits if L<K ; 0 otherwise (in particular if L>1296)
        is_guess_sufficiently_close_to_worth = player.computed_loss < player.random_k
        if is_guess_sufficiently_close_to_worth:
            player.point_earnings = 12.0
        else:
            player.point_earnings = 0.0

        # ---------------------------------------------------------------------
        # Question 1b: confidence interval about worth of the lottery
        # ---------------------------------------------------------------------
        # Computer computes 12*[1- (u-l)/(Emax-Emin)] if positive and worth in [l,u] (worth is in interval); 0 otherwise
        player.confidence_value = round(12.0*(1.0 - (float(player.max_worth - player.min_worth) / float(player.prep_emax - player.prep_emin))), 2)
        is_worth_within_interval = player.min_worth <= player.prep_worth <= player.max_worth
        computed_value_non_zero = player.confidence_value > 0.0
        if computed_value_non_zero and is_worth_within_interval:
            player.confidence_earnings = player.confidence_value
        else:
            player.confidence_earnings = 0

        if player.is_question_phase_payoff(question_number=1, rounds_per_lottery=Constants.ROUNDS_PER_LOTTERY):
            player.is_payment_round = True
            player.participant.vars['q1_data'] = {
                # "previous_highest_bid": player.previous_highest_bid,
                "fixed_value": player.fixed_value,
                "alpha": player.alpha,
                "beta": player.beta,
                "epsilon": player.epsilon,
                "signal": player.signal,
                "treatment": player.treatment,
                "lottery_order": player.lottery_order,
                "lottery_round_number": player.lottery_round_number,
                "ticket_value_after": player.ticket_value_after,
                "ticket_value_before": player.ticket_value_before,
                "ticket_probability": player.ticket_probability,
                "is_probability_treatment": player.is_probability_treatment,
                "is_value_treatment": player.is_value_treatment,
                # Question 1 Variables
                "prob": int(((MAX_DISTANCE - player.computed_loss) / MAX_DISTANCE)*100.0),
                "prep_emax": player.prep_emax,
                "prep_emin": player.prep_emin,
                "earnings_q1a": player.point_earnings,
                "max_worth": player.max_worth,
                "min_worth": player.min_worth,
                "worth": player.worth,
                "earnings_q1b": player.confidence_earnings,
                "earnings_q1": player.point_earnings + player.confidence_earnings,
                "is_worth_within_interval": is_worth_within_interval,
                "prep_worth": player.prep_worth,
                "random_k": player.random_k,
                "computed_loss": player.computed_loss,
                "confidence_value": player.confidence_value,
                "is_guess_sufficiently_close_to_worth": is_guess_sufficiently_close_to_worth,
                "computed_value_non_zero": computed_value_non_zero,
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
            interval_part_one=loader('IntervalOneBIntro.html').render({"player": player}),
            interval_part_two=loader('IntervalOneBContinuedIntro.html').render({"player": player}),
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
        player.prob_computed_loss = (highest - player.probability_highest_signal/100.0)**2
        # Computer draws random number K ~ U[0,1]
        player.random_prob_k = random.uniform(0, 1)
        # Computer pays 24 credits if L < K; 0 otherwise
        player.prob_earnings = 24.0 if player.prob_computed_loss < player.random_prob_k else 0.0

        if player.is_question_phase_payoff(question_number=3, rounds_per_lottery=Constants.ROUNDS_PER_LOTTERY):
            player.is_payment_round = True
            player.participant.vars['q2_data'] = {
                "fixed_value": player.fixed_value,
                "alpha": player.alpha,
                "beta": player.beta,
                "epsilon": player.epsilon,
                "signal": player.signal,
                "treatment": player.treatment,
                "lottery_order": player.lottery_order,
                "lottery_round_number": player.lottery_round_number,
                "ticket_value_after": player.ticket_value_after,
                "ticket_value_before": player.ticket_value_before,
                "ticket_probability": player.ticket_probability,
                "is_probability_treatment": player.is_probability_treatment,
                "is_value_treatment": player.is_value_treatment,
                "prep_worth": player.prep_worth,
                # Question 2 variables
                "highest": highest,
                "highest_market_signal": player.highest_market_signal,
                "highest_other_signal": player.highest_other_signal,
                "random_prob_k": player.random_prob_k,
                "prob_earnings": player.prob_earnings,
                # TODO: replace prob_earnings with earnings_q2
                "earnings_q2": player.prob_earnings,
                "probability_highest_signal": player.probability_highest_signal,
                "prob_computed_loss": player.prob_computed_loss,
                "prob": int((1 - player.prob_computed_loss) * 100)
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
            your_task_continued=loader('YourTaskProbabilityContinuedIntro.html').render({"player": player}),
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
            question=loader('QuestionIntro.html').render({"player": player}),
            your_task=loader('YourTaskHighestSignalIntro.html').render({"player": player}),
        )


class QuestionThreeB(Page):
    form_model = "player"
    form_fields = ["updated_worth", "updated_min_worth", "updated_max_worth"]

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
        MAX_DISTANCE = 1296
        # Prep Work
        cworth = player.be_bid
        # subject enters Cx (updated_worth)
        cx = player.updated_worth
        # Computer computes loss function L= (Cx-Cworth)^2
        l_3a = (cx - cworth)**2
        k_3a = random.randint(0, MAX_DISTANCE)
        # Computer pays 12 credits if L<K ; 0 otherwise (in particular if L>1296).
        guess_sufficiently_close_to_estimate = l_3a < k_3a
        if guess_sufficiently_close_to_estimate:
            earnings_3a = 12.0
        else:
            earnings_3a = 0.0

        player.l_3a = l_3a
        player.k_3a = k_3a
        player.earnings_3a = earnings_3a

        # ---------------------------------------------------------------------
        # Question 3b: confidence interval about conditional worth of the lottery.
        # ---------------------------------------------------------------------
        # cl for lower boundary and cu for upper boundary
        c_lower = player.updated_min_worth
        c_upper = player.updated_max_worth
        emax = player.prep_emax
        emin = player.prep_emin
        # Computer computes 12*[1- (cu-cl)/(Emax-Emin)] if positive and worth in [cl,cu] (Cworth is in interval); 0 otherwise
        computed_3b = round(12.0*(1.0 - float(c_upper-c_lower)/float(emax-emin)), 2)
        guess_within_chosen_interval = c_lower <= cworth <= c_upper
        computed_value_non_zero = computed_3b > 0
        if computed_value_non_zero and guess_within_chosen_interval:
            earnings_3b = computed_3b
        else:
            earnings_3b = 0

        player.computed_3b = computed_3b
        player.earnings_3b = earnings_3b
        earnings_q3 = earnings_3a + earnings_3b

        if player.is_question_phase_payoff(question_number=2, rounds_per_lottery=Constants.ROUNDS_PER_LOTTERY):
            player.is_payment_round = True
            player.payoff = cu(earnings_q3)
            player.participant.vars['q3_data'] = {
                "fixed_value": player.fixed_value,
                "alpha": player.alpha,
                "beta": player.beta,
                "epsilon": player.epsilon,
                "signal": player.signal,
                "treatment": player.treatment,
                "lottery_order": player.lottery_order,
                "lottery_round_number": player.lottery_round_number,
                "ticket_value_after": player.ticket_value_after,
                "ticket_value_before": player.ticket_value_before,
                "ticket_probability": player.ticket_probability,
                "is_probability_treatment": player.is_probability_treatment,
                "is_value_treatment": player.is_value_treatment,
                "prep_worth": player.prep_worth,
                # Question 3 variables
                "cworth": cworth,
                "cx": cx,
                "l_3a": l_3a,
                "k_3a": k_3a,
                "emax": emax,
                "emin": emin,
                "earnings_3a": earnings_3a,
                "updated_worth": player.updated_worth,
                "guess_sufficiently_close_to_estimate": guess_sufficiently_close_to_estimate,
                "cu": c_upper,
                "cl": c_lower,
                "computed_3b": computed_3b,
                "earnings_3b": earnings_3b,
                "updated_min_worth": player.updated_min_worth,
                "updated_max_worth": player.updated_max_worth,
                "earnings_q3": earnings_q3,
                "guess_within_chosen_interval": guess_within_chosen_interval,
                "prob": int(((MAX_DISTANCE - l_3a) / MAX_DISTANCE) * 100),
                "computed_value_non_zero": computed_value_non_zero,
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
            interval_part_one=loader('IntervalThreeBIntro.html').render({"player": player}),
            interval_part_two=loader('IntervalThreeBContinuedIntro.html').render({"player": player}),
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
