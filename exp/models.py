from otree.api import models, BasePlayer
from .db import BidHistory, PlayerBidHistory
from .constants import ExperimentConstants


class ExperimentSubSession:
    def get_lottery_ids(self):
        return [
            int(self.session.config[lottery_key])
            for lottery_key in [
                f"lottery_{key}"
                for key in range(1, ExperimentConstants.NUM_LOTTERIES + 1)
            ]
        ]

    def get_treatment_code(self) -> str:
        treatment_code = self.session.config["treatment"].strip()
        assert treatment_code == "cp" or treatment_code == "cv"
        return treatment_code


def save_bid_history_to_player(player, player_bid_history: PlayerBidHistory):
    player.rounds_per_lottery = ExperimentConstants.ROUNDS_PER_LOTTERY
    bid_history: BidHistory = player_bid_history.bid_history
    # Player Bid History
    player.player_bid_history_id = player_bid_history.id
    player.lottery_order = player_bid_history.lottery_order
    player.lottery_round_number = player_bid_history.lottery_round_number
    player.highest_other_signal = player_bid_history.highest_other_signal
    player.highest_market_signal = bid_history.signal > player_bid_history.highest_other_signal
    player.previous_highest_bid = player_bid_history.highest_other_bid
    # Bid History
    player.bid_history_id = bid_history.id
    player.previous_session_id = bid_history.session_id
    player.lottery_id = bid_history.lottery_id
    player.treatment = bid_history.treatment_code
    player.part_round_number = bid_history.part_round_number
    player.others_group_id = bid_history.group_id
    player.others_player_id = bid_history.player_id
    player.others_bid = bid_history.bid
    player.signal = bid_history.signal
    player.alpha = bid_history.alpha
    player.beta = bid_history.beta
    player.epsilon = bid_history.epsilon
    player.ticket_value_before = bid_history.ticket_value_before
    player.ticket_probability = bid_history.ticket_probability
    player.fixed_value = bid_history.fixed_value
    player.ticket_value_after = bid_history.ticket_value_after
    player.be_bid = bid_history.be_bid


def create_player_bid_histories(subsession, phase):
    if subsession.round_number == 1:
        BidHistory.excel_to_db()
        PlayerBidHistory.create_db()
        treatment_code = subsession.get_treatment_code()

        for player in subsession.get_players():
            lottery_ids = subsession.get_lottery_ids()
            for index, lottery_id in enumerate(lottery_ids):
                for lottery_round_number in range(
                    1, ExperimentConstants.ROUNDS_PER_LOTTERY + 1
                ):
                    unused_bid_histories = BidHistory.get_unused_bid_histories(
                        lottery_id,
                        treatment_code,
                        subsession.session.id,
                        player.participant.id,
                    )
                    bid_history = unused_bid_histories[lottery_round_number - 1]
                    PlayerBidHistory.add_bid_history(
                        bid_history=bid_history,
                        session_id=subsession.session.id,
                        lottery_round_number=lottery_round_number,
                        participant_id=player.participant.id,
                        lottery_order=index + 1,
                        phase=phase
                    )


def save_bid_history_for_all_players(players, phase):
    for player in players:
        player_bid_history: PlayerBidHistory = PlayerBidHistory.get_player_bid_history(
            session_id=player.subsession.session.id,
            lottery_round_number=player.get_lottery_round_number(),
            lottery_order=player.get_lottery_order(),
            participant_id=player.participant.id,
            phase=phase
        )
        save_bid_history_to_player(player, player_bid_history)


class BidHistoryPlayer:
    def __repr__(self):
        return f"""<Player(
            bid_history_id={self.bid_history_id}, previous_session_id={self.previous_session_id},
            lottery_id={self.lottery_id}, treatment={self.treatment}, lottery_round_number={self.lottery_round_number},
            lottery_order={self.lottery_order}, lottery_round_number={self.lottery_round_number},
            others_group_id={self.others_group_id}, others_player_id={self.others_player_id},
            others_bid={self.others_bid}, signal={self.signal}, alpha={self.alpha},
            beta={self.beta}, epsilon={self.epsilon}, ticket_value_before={self.ticket_value_before},
            ticket_probability={self.ticket_probability}, fixed_value={self.fixed_value},
            ticket_value_after={self.ticket_value_after}, previous_highest_bid={self.previous_highest_bid},
            player_bid_history_id={self.player_bid_history_id},
            lottery_order={self.lottery_order}, lottery_round_number={self.lottery_round_number},
            rounds_per_lottery={self.rounds_per_lottery}, be_bid={self.be_bid}
            )
            """

    def is_question_phase_payoff(self, question_number):
        lottery_number = self.get_lottery_order()
        round_number = self.get_lottery_round_number()
        payoff_question_number = self.participant.vars['question_phase_payoff_question_number']
        payoff_round_number = self.participant.vars['question_phase_payoff_lottery_round_number']
        payoff_lottery_number = self.participant.vars['question_phase_payoff_lottery_number']
        return round_number == payoff_round_number and lottery_number == payoff_lottery_number and question_number == payoff_question_number

    @property
    def payoff_question_number(self):
        return self.participant.vars['question_phase_payoff_question_number']

    @property
    def question_one_data(self):
        return self.participant.vars['q1_data']

    @property
    def question_two_data(self):
        return self.participant.vars['q2_data']

    @property
    def question_three_data(self):
        return self.participant.vars['q3_data']

    def get_lottery_round_number(self):
        return (self.round_number - 1) % ExperimentConstants.ROUNDS_PER_LOTTERY + 1

    def get_lottery_order(self):
        return ((self.round_number - 1) // ExperimentConstants.ROUNDS_PER_LOTTERY) + 1

    @property
    def lottery_number(self):
        return self.get_lottery_order()

    @property
    def rounds_per_lottery(self):
        return ExperimentConstants.ROUNDS_PER_LOTTERY

    @property
    def is_probability_treatment(self):
        return self.session_treatment == "cp"

    @property
    def is_value_treatment(self):
        return self.session_treatment == "cv"

    @property
    def selected_value_text(self):
        return "Selected Value" if self.is_value_treatment else "Selected Probability"

    @property
    def session_treatment(self):
        return self.subsession.session.config["treatment"]

    @property
    def min_signal(self):
        return self.signal - self.epsilon

    @property
    def max_signal(self):
        return self.signal + self.epsilon

    @property
    def lottery_max_value(self):
        if self.is_probability_treatment:
            return self.fixed_value
        else:
            return self.beta
