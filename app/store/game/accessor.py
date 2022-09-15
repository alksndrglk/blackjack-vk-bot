from ctypes import Union
from app.base.base_accessor import BaseAccessor
from app.game.models import GameModel, PlayerModel, UserModel, User
from app.store.vk_api.dataclasses import VkUser
from sqlalchemy import select, and_
from sqlalchemy.orm import joinedload


class BlackJackAccessor(BaseAccessor):
    async def get_game(self, chat_id: int):
        async with self.app.database.session() as session:
            result = await session.execute(
                select(GameModel)
                .where(
                    and_(GameModel.chat_id == chat_id, GameModel.finished_at == None)
                )
                .options(joinedload(GameModel.players))
            )

        obj: Union[GameModel, None] = result.scalar()
        if obj is None:
            return

        return obj.to_dct()

    async def create_game(self, peer_id: int, chat_members: list[VkUser]):
        users = self.user_registration(chat_members)
        game = GameModel(
            chat_id=peer_id, players=[PlayerModel(user_id=u.id) for u in users]
        )
        async with self.app.database.session() as session:
            async with session.begin():
                session.add_all(game)

    async def user_registration(self, chat_members: list[VkUser]):
        users = [
            UserModel(vk_id=member.vk_id, user_name=member.user_name)
            for member in chat_members
        ]
        async with self.app.database.session() as session:
            async with session.begin():
                session.add_all(users)
        return [u.to_dct() for u in users]

    async def update_game(self):
        pass

    async def update_player(self):
        pass

    async def update_user(self):
        pass
