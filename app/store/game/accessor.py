from ctypes import Union
from dataclasses import asdict
from datetime import datetime
from typing import Optional
from app.base.base_accessor import BaseAccessor
from app.store.database import db
from app.game.models import Game, GameModel, GameState, PlayerModel, UserModel, User
from sqlalchemy import select, and_
from sqlalchemy.orm import joinedload
from sqlalchemy.dialects.postgresql import insert


class UserRegistrationFailed(Exception):
    pass


class BlackJackAccessor(BaseAccessor):
    async def get_game(self, chat_id: int) -> Optional[Game]:
        async with self.app.database.session() as session:
            result = await session.execute(
                select(GameModel)
                .where(
                    and_(GameModel.chat_id == chat_id, GameModel.finished_at == None)
                )
                .options(joinedload(GameModel.players))
            )

        obj: Union[GameModel, None] = result.scalar()
        self.logger.info(obj)
        if obj is None:
            return None
        return obj.to_dct()

    async def create_game(self, peer_id: int):
        print("creating game")
        users = await self.user_registration(peer_id)
        print(users)
        self.logger.info(users)
        if not users:
            return UserRegistrationFailed()
        game = GameModel(
            chat_id=peer_id,
            state=GameState.wait_for_bid.name,
            players=[PlayerModel(user_id=u.id) for u in users],
        )
        self.logger.info(game)
        async with self.app.database.session() as session:
            async with session.begin():
                session.add(game)

    async def user_registration(self, peer_id: int) -> list[User]:
        chat_members = await self.app.store.vk_api.get_conversation_members(peer_id)
        async with self.app.database.session() as session:
            async with session.begin():
                statement = insert(UserModel).values(
                    [
                        {
                            "vk_id": member.vk_id,
                            "user_name": member.user_name,
                        }
                        for member in chat_members
                    ]
                )
                result = await session.execute(
                    statement.on_conflict_do_update(
                        index_elements=[UserModel.vk_id],
                        set_={"created_at": datetime.now()},
                    ).returning(UserModel)
                )
        return [User(*u) for u in result]

    async def update_game(self):
        pass

    async def update_player(self):
        pass

    async def update_user(self):
        pass
