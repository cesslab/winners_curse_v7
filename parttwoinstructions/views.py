import random
import os

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
        return {"player": player}


class Bid(Page):
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
        loader = ibis.loaders.FileLoader(Path(__file__).parent)
        return dict(
            alpha=player.alpha,
            beta=player.beta,
            epsilon=player.epsilon,
            signal=player.signal,
            min_signal=player.min_signal,
            max_signal=player.max_signal,
            is_cv_treatment=player.is_value_treatment,
            selected_value_text=player.selected_value_text,
            the_prize=loader('ThePrize.html').render({"player": player}),
            four_bidders=loader('FourBidders.html').render({"player": player}),
            your_task=loader('YourTaskIntro.html').render({"player": player}),
            your_signal=loader('YourSignalIntro.html').render({"player": player}),
            signal_interpretation=loader('SignalInterpretationIntro.html').render({"player": player}),
            lottery_types=loader('LotteryTypesIntro.html').render({"player": player}),
        )


class Outcome(Page):
    @staticmethod
    def vars_for_template(player):
        return {
            "player": player,
            "num_rounds": range(1, Constants.ROUNDS_PER_LOTTERY + 1),
            "num_lotteries": range(1, Constants.NUM_LOTTERIES + 1),
        }


class Payoff(Page):

    @staticmethod
    def vars_for_template(player):
        return {
            "player": player,
            "num_rounds": range(1, Constants.ROUNDS_PER_LOTTERY + 1),
            "num_lotteries": range(1, Constants.NUM_LOTTERIES + 1),
        }
