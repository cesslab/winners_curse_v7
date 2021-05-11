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
        if player.bid > player.previous_highest_bid:
            player.new_highest_bid = player.bid
            player.tie = False
            player.winner = True
            player.earnings = player.ticket_value_after - player.bid
        elif player.bid < player.previous_highest_bid:
            player.new_highest_bid = player.previous_highest_bid
            player.tie = False
            player.winner = False
            player.earnings = 0
        else:
            player.new_highest_bid = player.previous_highest_bid
            player.tie = True
            player.win_tie_break = random.choice([True, False])
            if player.win_tie_break:
                player.earnings = player.ticket_value_after - player.bid
            else:
                player.earnings = 0
            player.winner = player.win_tie_break

        if player.lottery_order == player.participant.vars['payoff_lottery_number'] and player.lottery_round_number == player.participant.vars['payoff_lottery_round_number']:
            player.participant.vars['bid_payoff_data'] = {
                "bid": player.bid,
                "new_highest_bid": player.new_highest_bid,
                "tie": player.tie,
                "win_tie_break": player.win_tie_break,
                "winner": player.winner,
                "previous_highest_bid": player.previous_highest_bid,
                "fixed_value": player.fixed_value,
                "alpha": player.alpha,
                "beta": player.beta,
                "epsilon": player.epsilon,
                "signal": player.signal,
                "treatment": player.treatment,
                "earnings": player.earnings,
                "lottery_order": player.lottery_order,
                "lottery_round_number": player.lottery_round_number,
                "ticket_value_after": player.ticket_value_after,
                "ticket_probability": player.ticket_probability
            }


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
            "num_rounds": range(1, Constants.ROUNDS_PER_LOTTERY + 1),
            "num_lotteries": range(1, Constants.NUM_LOTTERIES + 1),
        }


class Outcome(Page):
    form_model = "player"

    @staticmethod
    def vars_for_template(player):
        earnings = player.ticket_value_after - player.bid
        return {
            "earnings": earnings,
            "player": player,
            "num_rounds": range(1, Constants.ROUNDS_PER_LOTTERY + 1),
            "num_lotteries": range(1, Constants.NUM_LOTTERIES + 1),
        }


