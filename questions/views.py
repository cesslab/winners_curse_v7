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
    def before_next_page(player, timeout_happened):
        # PREP WORK
        # Worth = vLotto *fix (in CV) or pLotto * fix (in CP)
        if player.is_probability_treatment:
            player.prep_worth = player.ticket_probability * player.fixed_value
        else:
            player.prep_worth = player.ticket_value_before * player.fixed_value

        #  Emin = fix * alpha
        #  Emax = fix * beta
        player.prep_emin = player.fixed_value * player.alpha
        player.prep_emax = player.fixed_value * player.beta

        # ---------------------------------------------------------------------
        # Question 1a: point belief about worth of the lottery (unconditional)
        # ---------------------------------------------------------------------
        # Computer computes loss function L= (X-worth)^2
        player.computed_loss = (player.worth - player.prep_worth)**2
        # Computer draws random number K ~ U[0,1296]
        player.random_k = random.randint(0, 1296)
        # Computer pays 12 credits if L<K ; 0 otherwise (in particular if L>1296)
        if player.computed_loss < player.random_k:
            player.point_earnings = 12
        else:
            player.point_earnings = 0

        # ---------------------------------------------------------------------
        # Question 1b: confidence interval about worth of the lottery
        # ---------------------------------------------------------------------
        # Computer computes 12*[1- (u-l)/(Emax-Emin)] if positive and worth in [l,u] (worth is in interval); 0 otherwise
        player.confidence_value = 12.0*(1.0 - (float(player.max_worth - player.min_worth) / float(player.prep_emax - player.prep_emin)))
        if player.confidence_value > 0.0 and player.min_worth >= player.prep_worth <= player.max_worth:
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
                "point_earnings": player.point_earnings,
                "max_worth": player.max_worth,
                "min_worth": player.min_worth,
                "worth": player.worth,
                "confidence_interval_earnings": player.confidence_earnings,
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
            }

    @staticmethod
    def js_vars(player):
        return dict(
            display_intro=(player.round_number == 1),
            worth=player.worth,
            lottery_max_value=player.lottery_max_value,
            mapping_divisor=player.fixed_value,
            is_probability_treatment=player.is_probability_treatment,
        )


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
    def before_next_page(player, timeout_happened):
        # PREP WORK
        # Worth = vLotto *fix (in CV) or pLotto * fix (in CP)
        if player.is_probability_treatment:
            player.prep_worth = player.ticket_probability * player.fixed_value
        else:
            player.prep_worth = player.ticket_value_before * player.fixed_value

        #  Emin = fix * alpha
        #  Emax = fix * beta
        player.prep_emin = player.fixed_value * player.alpha
        player.prep_emax = player.fixed_value * player.beta

        # ---------------------------------------------------------------------
        # Question 1a: point belief about worth of the lottery (unconditional)
        # ---------------------------------------------------------------------
        # Computer computes loss function L= (X-worth)^2
        player.computed_loss = (player.worth - player.prep_worth)**2
        # Computer draws random number K ~ U[0,1296]
        player.random_k = random.randint(0, 1296)
        # Computer pays 12 credits if L<K ; 0 otherwise (in particular if L>1296)
        if player.computed_loss < player.random_k:
            player.point_earnings = 12
        else:
            player.point_earnings = 0

        if player.lottery_order == player.participant.vars['worth_payoff_lottery_number'] and player.lottery_round_number == player.participant.vars['worth_payoff_lottery_round_number']:
            player.participant.vars['q1a_data'] = {
                "prep_emax": player.prep_emax,
                "prep_emin": player.prep_emin,
                "prep_worth": player.prep_worth,
                "worth": player.worth,
                "random_k": player.random_k,
                "computed_loss": player.computed_loss,
                "point_earnings": player.point_earnings,
            }

    @staticmethod
    def js_vars(player):
        return dict(
            display_intro=(player.round_number == 1),
            lottery_max_value=player.lottery_max_value,
            mapping_divisor=player.fixed_value,
            is_probability_treatment=player.is_probability_treatment,
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
        # Computer pays 12 credits if L < K; 0 otherwise
        player.prob_earnings = 12 if player.prob_computed_loss < player.random_prob_k else 0

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
        return dict(
            display_intro=(player.round_number == 1),
            lottery_max_value=player.lottery_max_value,
            mapping_divisor=player.fixed_value,
            is_probability_treatment=player.is_probability_treatment,
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
        return dict(
            display_intro=(player.round_number == 1),
            lottery_max_value=player.lottery_max_value,
            mapping_divisor=player.fixed_value,
            is_probability_treatment=player.is_probability_treatment,
        )


class QuestionThreeB(Page):
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
            "new_lottery":
                (
                    player.round_number != 1
                    and ((player.round_number - 1) % Constants.ROUNDS_PER_LOTTERY) == 0
                )
        }

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
        if l_3a < k_3a:
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
            "earnings_3a": earnings_3a
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
        if computed_3b > 0 and cl <= cworth <= cu:
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
            "earnings_3b": earnings_3b
        }

    @staticmethod
    def js_vars(player):
        return dict(
            display_intro=(player.round_number == 1),
            updated_worth=player.updated_worth,
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
