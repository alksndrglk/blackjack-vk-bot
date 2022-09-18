from datetime import datetime
import json
from os import stat
from typing import Optional, Union
from app.base.base_accessor import BaseAccessor
from app.game.models import (
    Game,
    GameModel,
    GameState,
    GameStats,
    GameStatsModel,
    Player,
    PlayerModel,
    PlayerStatus,
    UserModel,
    User,
)
from sqlalchemy import select, and_, update
from sqlalchemy.orm import joinedload, subqueryload
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
                .options(joinedload(GameModel.players).subqueryload(PlayerModel.user))
                .options(joinedload(GameModel.stats))
            )

        obj: Union[GameModel, None] = result.scalar()
        self.logger.info(obj)
        if obj is None:
            return None
        try:
            return obj.to_dct()
        except Exception as e:
            print(e)

    async def create_game(self, peer_id: int):
        users = await self.user_registration(peer_id)
        self.logger.info(users)
        if not users:
            return UserRegistrationFailed()
        game = GameModel(
            chat_id=peer_id,
            state=GameState.wait_for_bid.name,
            players=[
                PlayerModel(user_id=u.id, status=PlayerStatus.BETS) for u in users
            ],
            stats=[GameStatsModel()],
        )
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

    async def update_game(self, game: Game):
        async with self.app.database.session() as session:
            async with session.begin():
                statement = (
                    update(GameModel)
                    .where(GameModel.id == game.id)
                    .values(
                        {
                            "state": game.state,
                            "current_player": game.current_player,
                            "hand": json.dumps(game.hand),
                            "finished_at": game.finished_at,
                        }
                    )
                )
                await session.execute(statement)
        self.logger.info(f"updating game: {game}")

    async def update_player(self, player: Player):
        async with self.app.database.session() as session:
            async with session.begin():
                statement = (
                    update(PlayerModel)
                    .where(PlayerModel.id == player.id)
                    .values(
                        {
                            "amount": player.amount,
                            "hand": json.dumps(player.hand),
                            "bid": player.bid,
                            "status": player.status,
                        }
                    )
                )
                await session.execute(statement)
        self.logger.info(f"updating player: {player}")

    async def update_user(self, user: User):
        async with self.app.database.session() as session:
            async with session.begin():
                statement = (
                    update(UserModel)
                    .where(UserModel.id == user.id)
                    .values(
                        {
                            "wins": user.wins,
                            "loss": user.loss,
                        }
                    )
                )
                await session.execute(statement)
        self.logger.info(f"updating user: {user}")

    async def update_game_stats(self, game_stats: GameStats):
        async with self.app.database.session() as session:
            async with session.begin():
                statement = (
                    update(GameStatsModel)
                    .where(GameStatsModel.id == game_stats.id)
                    .values(
                        {
                            "wins": game_stats.wins,
                            "loss": game_stats.loss,
                            "draw": game_stats.draw,
                            "income": game_stats.income,
                        }
                    )
                )
            await session.execute(statement)
        self.logger.info(f"updating game_stats: {game_stats}")
