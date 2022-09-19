from __future__ import annotations
import enum
from dataclasses import dataclass, field
from datetime import datetime
import json
from typing import Union
from app.store.database.sqlalchemy_base import db
from sqlalchemy.sql import func

from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    Integer,
    Enum,
    DateTime,
    ForeignKey,
)
from sqlalchemy.dialects.postgresql import JSONB

from app.player.models import Player


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
    id: int
    chat_id: int
    state: int
    current_player: int
    players_num: int
    hand: dict
    stats: GameStats
    finished_at: Union[None, datetime] = None
    players: list[Player] = field(default_factory=list)

    def show_hand(self, blind: bool):
        hand = self.hand["hand"]
        value = self.hand["value"]
        if blind:
            hand = hand.split()[0] + "❔❔"
            value = ""
        return f"Дилер {hand} {value}"


class GameModel(db):
    __tablename__ = "game"

    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=func.now())
    finished_at = Column(DateTime, default=None)
    state = Column(Enum(GameState))
    hand = Column(JSONB, default="{}")
    current_player = Column(Integer, ForeignKey("bljc_user.vk_id"))
    players_num = Column(Integer, default=1)
    players = relationship("PlayerModel")
    stats = relationship("GameStatsModel")

    def to_dct(self) -> Game:
        return Game(
            id=self.id,
            chat_id=self.chat_id,
            state=self.state,
            current_player=self.current_player,
            players_num=self.players_num,
            finished_at=self.finished_at,
            hand=json.loads(self.hand),
            players=[pl.to_dct() for pl in self.players],
            stats=self.stats[-1].to_dct(),
        )


@dataclass
class GameStats:
    id: int
    game_id: int
    wins: int
    loss: int
    draw: int
    income: int


class GameStatsModel(db):
    __tablename__ = "game_stats"

    id = Column(Integer, primary_key=True)
    game_id = Column(Integer, ForeignKey("game.id", ondelete="CASCADE"), nullable=False)
    wins = Column(Integer, default=0)
    loss = Column(Integer, default=0)
    draw = Column(Integer, default=0)
    income = Column(Integer, default=0)

    def to_dct(self):
        return GameStats(
            id=self.id,
            game_id=self.id,
            wins=self.wins,
            loss=self.loss,
            draw=self.draw,
            income=self.income,
        )
