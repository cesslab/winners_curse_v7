import os
import pandas as pd
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy_utils.types.choice import ChoiceType

# class DBWrapper():
#     db: sqlalchemy.orm.Session =

engine = create_engine(os.getenv("DATABASE_URL"))
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class Phase:
    BID_PHASE = 'bid'
    QUESTION_PHASE = 'question'
    VALUATION_PHASE = 'valuation'


class PlayerBidHistory(Base):
    PHASES = [(Phase.BID_PHASE, 'Bid'), (Phase.QUESTION_PHASE, 'Question'), (Phase.VALUATION_PHASE, 'Valuation')]
    __tablename__ = "player_bid_history"
    id = Column(Integer, primary_key=True)
    bid_history_id = Column(Integer, ForeignKey("bid_history.id"), nullable=False)
    bid_history = relationship("BidHistory", back_populates="player_bid_histories")
    lottery_order = Column(Integer, nullable=False)
    lottery_round_number = Column(Integer, nullable=False)
    session_id = Column(Integer, nullable=False)
    participant_id = Column(Integer, nullable=False)
    phase = Column(ChoiceType(PHASES))

    def __repr__(self):
        return f"""
            <PlayerBidHistory(
                bid_history_id={self.bid_history_id}, lottery_oder={self.lottery_order} lottery_round_number={self.lottery_round_number},
                session_id={self.session_id}, participant_id={self.participant_id}, phase={self.phase})>"""

    @staticmethod
    def get_player_bid_history(
        session_id, lottery_round_number, lottery_order, participant_id, phase
    ):
        player_bid_history = (
            session.query(PlayerBidHistory)
            .filter(PlayerBidHistory.session_id == session_id)
            .filter(PlayerBidHistory.lottery_round_number == lottery_round_number)
            .filter(PlayerBidHistory.lottery_order == lottery_order)
            .filter(PlayerBidHistory.participant_id == participant_id)
            .filter(PlayerBidHistory.phase == phase)
            .first()
        )
        return player_bid_history

    @staticmethod
    def create_db():
        if not engine.dialect.has_table(engine, "player_bid_history"):
            Base.metadata.create_all(engine)

    @staticmethod
    def add_bid_history(
        session_id,
        lottery_round_number,
        participant_id,
        lottery_id,
        lottery_order,
        treatment_code,
        phase,
    ):
        unused_bid_histories = BidHistory.get_unused_bid_histories(
            lottery_id, treatment_code, session_id, participant_id
        )

        bid_history = unused_bid_histories[0]

        player_bid_history = PlayerBidHistory(
            lottery_round_number=lottery_round_number,
            participant_id=participant_id,
            session_id=session_id,
            bid_history=bid_history,
            lottery_order=lottery_order,
            phase=phase
        )
        session.add(player_bid_history)
        bid_history.times_used += 1
        session.commit()


def close_db():
    session.close()


class BidHistory(Base):
    __tablename__ = "bid_history"
    id = Column(Integer, primary_key=True)
    times_used = Column(Integer, nullable=False)
    session_id = Column(Integer, nullable=False)
    # lotteryId
    lottery_id = Column(Integer, nullable=False)
    # treatment
    treatment_code = Column(String, nullable=False)
    # round
    part_round_number = Column(Integer, nullable=False)
    # groupInRound
    group_id = Column(Integer, nullable=False)
    # playerInGroup
    player_id = Column(Integer, nullable=False)
    # subject
    participant_id = Column(Integer, nullable=False)
    bid = Column(Integer, nullable=False)
    signal = Column(Integer, nullable=False)
    alpha = Column(Integer, nullable=False)
    beta = Column(Integer, nullable=False)
    epsilon = Column(Integer, nullable=False)
    # vLotto
    ticket_value_before = Column(Integer, nullable=False)
    # pLotto
    ticket_probability = Column(Integer, nullable=False)
    # fix (c)
    fixed_value = Column(Integer, nullable=False)
    # ticket
    ticket_value_after = Column(Integer, nullable=False)
    # winBid
    highest_bid = Column(Integer, nullable=False)
    player_bid_histories = relationship("PlayerBidHistory", back_populates="bid_history")

    @staticmethod
    def get_bid_history(bid_history_id):
        return session.query(BidHistory).filter(BidHistory.id == bid_history_id).first()

    def __repr__(self):
        return f"""
            <BidHistory(
                times_used={self.times_used}, session_id={self.session_id}, lottery_id={self.lottery_id},
                treatment_code={self.treatment_code}, part_round_number={self.part_round_number},
                group_id={self.group_id}, player_id={self.player_id},
                participant_id={self.participant_id}, bid={self.bid}, signal={self.signal},
                alpha={self.alpha}, self, beta={self.beta}, epsilon={self.epsilon},
                ticket_value_before={self.ticket_value_before},
                ticket_probability={self.ticket_probability},
                fixed_value={self.fixed_value}, ticket_value_after={self.ticket_value_after},
                highest_bid={self.highest_bid})>"""

    @staticmethod
    def get_unused_bid_histories(
        lottery_id, treatment_code, session_id, participant_id
    ):
        usable_bid_histories = (
            session.query(BidHistory)
            .filter(BidHistory.lottery_id == lottery_id)
            .filter(BidHistory.treatment_code == treatment_code)
            .filter(
                BidHistory.id.notin_(
                    session.query(PlayerBidHistory.bid_history_id)
                    .filter(PlayerBidHistory.session_id == session_id)
                    .filter(PlayerBidHistory.participant_id == participant_id)
                )
            )
            .order_by(BidHistory.times_used.asc())
        )

        usable_bid_histories = usable_bid_histories.all()

        return usable_bid_histories

    @staticmethod
    def get_treatment_lottery_bid_histories(lottery_id, treatment_code):
        return (
            session.query(BidHistory)
            .filter(BidHistory.lottery_id == lottery_id)
            .filter(BidHistory.treatment_code == treatment_code)
            .order_by(BidHistory.times_used.desc())
        )

    @staticmethod
    def excel_to_db():
        if not engine.dialect.has_table(engine, "bid_history"):
            Base.metadata.create_all(engine)

        num_rows = session.query(BidHistory).count()
        if num_rows == 0:
            print(f"Creating bid_history table and rows using PrepDataAuctions-3.xls")
            file_name = os.path.join(
                os.path.dirname(os.path.dirname(__file__)), "PrepDataAuctions-3.xls"
            )
            df = pd.read_excel(
                file_name,
                converters={
                    "numSession": int,
                    "lotteryid": int,
                    "treatment": str,
                    "round": int,
                    "groupInRound": int,
                    "playerInGroup": int,
                    "subject": int,
                    "bid": int,
                    "signal": int,
                    "alpha": int,
                    "beta": int,
                    "epsilon": int,
                    "vLotto": int,
                    "pLotto": float,
                    "fix": int,
                    "ticket": int,
                    "winBid": int,
                },
            )
            df = df.filter(
                [
                    "numSession",
                    "lotteryid",
                    "treatment",
                    "round",
                    "groupInRound",
                    "playerInGroup",
                    "subject",
                    "bid",
                    "signal",
                    "alpha",
                    "beta",
                    "epsilon",
                    "vLotto",
                    "pLotto",
                    "fix",
                    "ticket",
                    "winBid",
                ]
            )
            df.dropna(inplace=True)
            for index, row in df.iterrows():
                bid_history = BidHistory(
                    times_used=0,
                    session_id=row["numSession"],
                    lottery_id=row["lotteryid"],
                    treatment_code=row["treatment"],
                    part_round_number=row["round"],
                    group_id=row["groupInRound"],
                    player_id=row["playerInGroup"],
                    participant_id=row["subject"],
                    bid=row["bid"],
                    signal=row["signal"],
                    alpha=row["alpha"],
                    beta=row["beta"],
                    epsilon=row["epsilon"],
                    ticket_value_before=row["vLotto"],
                    ticket_probability=row["pLotto"],
                    fixed_value=row["fix"],
                    ticket_value_after=row["ticket"],
                    highest_bid=row["winBid"],
                )
                session.add(bid_history)
            session.commit()
            print(f"Records added: {session.query(BidHistory).count()}")
        else:
            print(f"Skipped bid_history table creation. {num_rows} rows already exist.")
