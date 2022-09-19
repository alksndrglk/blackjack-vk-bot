from __future__ import annotations
import enum
from dataclasses import dataclass
import json
from typing import Optional
from unittest import result
from app.store.database.sqlalchemy_base import db

from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    Integer,
    Enum,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import JSONB

from app.user.models import User


class PlayerStatus(enum.Enum):
    BETS = enum.auto()
    HIT = enum.auto()
    STAND = enum.auto()
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
    hand: dict
    bid: int
    status: str
    user: Optional[User] = None

    def show_hand(self, show_results: bool = False):
        results = ""
        if show_results:
            status_emoji = {
                PlayerStatus.WIN: "💰🤑",
                PlayerStatus.LOSED: "😢",
                PlayerStatus.DRAW: "🤷🏿‍♂️",
            }
            results = f"Счет:{self.user.amount} {status_emoji[self.status]}"
        return f"{self.user.user_name} {self.hand['hand']} --> ({self.hand['value']}) {results}"


class PlayerModel(db):
    __tablename__ = "player"

    id = Column(Integer, primary_key=True)
    user_id = Column(
        Integer,
        ForeignKey("bljc_user.vk_id", ondelete="CASCADE"),
        nullable=False,
    )
    game_id = Column(Integer, ForeignKey("game.id", ondelete="CASCADE"), nullable=False)
    hand = Column(JSONB, default="{}")
    bid = Column(Integer, nullable=False, default=10)
    status = Column(Enum(PlayerStatus))
    user = relationship("UserModel", lazy="subquery")
    __table_args__ = (UniqueConstraint("user_id", "game_id", name="us_ga_id"),)

    def to_dct(self) -> Player:
        return Player(
            id=self.id,
            user_id=self.user_id,
            game_id=self.game_id,
            hand=json.loads(self.hand),
            bid=self.bid,
            status=self.status,
            user=self.user.to_dct(),
        )
