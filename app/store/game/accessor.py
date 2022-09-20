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
)
from app.player.models import Player, PlayerModel, PlayerStatus
from app.user.models import User, UserModel
from sqlalchemy import select, and_, update, delete
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
        return obj.to_dct()

    async def create_game(self, peer_id: int):
        users = await self.user_registration(peer_id)
        self.logger.info(users)
        if not users:
            return UserRegistrationFailed()
        game = GameModel(
            chat_id=peer_id,
            state=GameState.number_of_players.name,
            stats=[GameStatsModel()],
        )
        async with self.app.database.session() as session:
            async with session.begin():
                session.add(game)

    async def register_player(self, game: Game, user_id: int):
        async with self.app.database.session() as session:
            async with session.begin():
                statement = insert(PlayerModel).values(
                    {
                        "user_id": user_id,
                        "game_id": game.id,
                        "status": PlayerStatus.BETS,
                    }
                )
                result = await session.execute(
                    statement.on_conflict_do_nothing().returning(PlayerModel)
                )
        obj = result.fetchone()
        if obj is None:
            return
        try:
            game.players.append(Player(*obj))
        except Exception as e:
            print(e)

    async def unregister_player(self, game: Game, user_id: int):
        async with self.app.database.session() as session:
            async with session.begin():
                statement = delete(PlayerModel).where(
                    and_(PlayerModel.user_id == user_id, PlayerModel.game_id == game.id)
                )
                await session.execute(statement)
        game.players = list(filter(lambda x: x.user_id != user_id, game.players))

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
                            "state": game.state.name,
                            "current_player": game.current_player,
                            "hand": json.dumps(game.hand),
                            "finished_at": game.finished_at,
                            "players_num": game.players_num,
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
                            "amount": user.amount,
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

    async def list_users(self, limit, offset) -> Optional[list[User]]:
        query = select(UserModel)
        if limit:
            query = query.limit(limit)
        if offset:
            query = query.offset(offset)
        async with self.app.database.session() as session:
            result = await session.execute(query)

        obj: Union[GameModel, None] = result.scalars()
        self.logger.info(obj)
        if obj is None:
            return None
        return [u.to_dct() for u in obj]

    async def list_games(self, limit, offset) -> Optional[list[Game]]:
        query = (
            select(GameModel)
            .options(joinedload(GameModel.players).subqueryload(PlayerModel.user))
            .options(joinedload(GameModel.stats))
        )
        if limit:
            query = query.limit(limit)
        if offset:
            query = query.offset(offset)
        async with self.app.database.session() as session:
            result = await session.execute(query)

        obj: Union[GameModel, None] = result.scalars().unique()
        self.logger.info(obj)
        if obj is None:
            return None
        return [u.to_dct() for u in obj]

    async def list_players(self, limit, offset) -> Optional[list[Player]]:
        print(limit, offset)
        query = select(PlayerModel).options(joinedload(PlayerModel.user))
        if limit:
            query = query.limit(limit)
        if offset:
            query = query.offset(offset)
        async with self.app.database.session() as session:
            result = await session.execute(query)

        obj: Union[PlayerModel, None] = result.scalars()
        self.logger.info(obj)
        if obj is None:
            return None
        return [u.to_dct() for u in obj]

    async def get_user(self, user_id: int) -> Optional[User]:
        async with self.app.database.session() as session:
            async with session.begin():
                result = await session.execute(
                    select(UserModel).where(UserModel.vk_id == user_id)
                )

        obj: Union[UserModel, None] = result.scalar()
        self.logger.info(obj)
        if obj is None:
            return None
        return obj.to_dct()

    async def get_player(self, user_id: int) -> Optional[Player]:
        async with self.app.database.session() as session:
            async with session.begin():
                result = await session.execute(
                    select(PlayerModel).where(PlayerModel.user_id == user_id)
                )

        obj: Union[UserModel, None] = result.scalar()
        self.logger.info(obj)
        if obj is None:
            return None
        return obj.to_dct()
