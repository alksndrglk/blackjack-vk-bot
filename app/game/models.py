from collections import defaultdict
import enum
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Union
from app.store.database.sqlalchemy_base import db
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    Integer,
    String,
    Enum,
    DateTime,
    ForeignKey,
)
from sqlalchemy.dialects.postgresql import JSONB


@dataclass
class User:
    id: int
    vk_id: int
    user_name: str
    created_at: datetime
    wins: int
    loss: int



class UserModel(db):
    __tablename__ = "bljc_user"

    id = Column(Integer, primary_key=True)
    vk_id = Column(Integer, unique=True, nullable=False)
    user_name = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now())
    wins = Column(Integer, default=0)
    loss = Column(Integer, default=0)

    def to_dct(self):
        return User(
            id=self.id,
            vk_id=self.vk_id,
            user_name=self.user_name,
            wins=self.wins,
            loss=self.loss,
        )


class PlayerStatus(enum.Enum):
    BETS = enum.auto()
    HIT = enum.auto()
    WIN = enum.auto()
    BLACKJACK = enum.auto()
    WAITING = enum.auto()
    LOSED = enum.auto()
    DRAW = enum.auto()
    QUITED = enum.auto()


@dataclass
class Player:
    id: int
    user_id: int
    game_id: int
    amount: int
    hand: dict
    bid: int
    status: str


class PlayerModel(db):
    __tablename__ = "player"

    id = Column(Integer, primary_key=True)
    user_id = Column(
        Integer,
        ForeignKey("bljc_user.id", ondelete="CASCADE"),
        nullable=False,
    )
    game_id = Column(Integer, ForeignKey("game.id", ondelete="CASCADE"), nullable=False)
    amount = Column(Integer, nullable=False, default=500)
    hand = Column(JSONB, default="{}")
    bid = Column(Integer, nullable=False, default=10)
    status = Column(Enum(PlayerStatus))

    def to_dct(self) -> Player:
        return Player(
            id=self.id,
            user_id=self.user_id,
            game_id=self.game_id,
            amount=self.amount,
            hand=self.hand,
            bid=self.bid,
            status=self.status,
        )


class GameState(enum.Enum):
    initial_trigger = enum.auto()
    start_trigger = enum.auto()
    menu_selection = enum.auto()
    number_of_players = enum.auto()
    player_accession = enum.auto()
    wait_for_bid = enum.auto()
    action_selection = enum.auto()
    continue_or_leave = enum.auto()


@dataclass
class Game:
    id: Optional[int]
    chat_id: int
    state: int
    current_player: int
    finished_at: Union[None, datetime] = None
    players: list[Player] = field(default_factory=list)


class GameModel(db):
    __tablename__ = "game"

    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=func.now())
    finished_at = Column(DateTime, default=None)
    state = Column(Enum(GameState))
    current_player = Column(Integer, ForeignKey("bljc_user.vk_id"))
    players = relationship("PlayerModel")

    def to_dct(self) -> Game:
        return Game(
            id=self.id,
            chat_id=self.chat_id,
            state=self.state,
            current_player=self.current_player,
            finished_at=self.finished_at,
            players=[pl.to_dct() for pl in self.players],
        )


class GameStats(db):
    __tablename__ = "game_stats"

    id = Column(Integer, primary_key=True)
    game_id = Column(Integer, ForeignKey("game.id"))
    wins = Column(Integer, default=0)
    loss = Column(Integer, default=0)
    draw = Column(Integer, default=0)
    income = Column(Integer, default=0)
