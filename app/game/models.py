import enum
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Union
from app.store.database.sqlalchemy_base import db
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
    wins: int
    loss: int


class UserModel(db):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    vk_id = db.Column(Integer, unique=True, nullable=False)
    user_name = db.Column(String, nullable=False)
    created_at = db.Column(DateTime, server_default="now()")
    wins = db.Column(Integer, server_default=0)
    loss = db.Column(Integer, server_default=0)

    def to_dict(self):
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


class Player(db):
    __tablename__ = "player"

    id = db.Column(Integer, primary_key=True)
    user_id = db.Column(
        Integer,
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
    )
    game_id = db.Column(
        Integer, ForeignKey("game.id", ondelete="CASCADE"), nullable=False
    )
    amount = db.Column(Integer, nullable=False, server_default=500)
    hand = db.Column(JSONB, server_default="{}")
    bid = db.Column(Integer, nullable=False, server_default=10)
    status = db.Column(Enum(PlayerStatus))


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
    state: dict
    current_player: int
    finished_at: Union[None, datetime] = None


class GameModel(db.Model):
    __tablename__ = "game"

    id = db.Column(Integer, primary_key=True)
    chat_id = db.Column(Integer, nullable=False)
    created_at = db.Column(DateTime, server_default="now()")
    finished_at = db.Column(DateTime, server_default=None)
    state = db.Column(Enum(GameState))
    current_player = db.Column(Integer, ForeignKey("user.vk_id"))

    def to_dct(self) -> Game:
        return Game(
            id=self.id,
            chat_id=self.chat_id,
            state=self.state,
            current_player=self.current_player,
            finished_at=self.finished_at,
        )

class GameStats(db):
    __tablename__ = "game_stats"

    game_id = db.Column(Integer, ForeignKey("game.id"))
    wins = db.Column(Integer, server_default=0)
    loss = db.Column(Integer, server_default=0)
    draw = db.Column(Integer, server_default=0)
    income = db.Column(Integer, server_default=0)