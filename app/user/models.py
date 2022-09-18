from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from app.store.database.sqlalchemy_base import db
from sqlalchemy.sql import func

from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
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
            created_at=self.created_at,
            wins=self.wins,
            loss=self.loss,
        )
