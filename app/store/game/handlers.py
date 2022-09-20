import asyncio
from datetime import datetime

from app.store.game.accessor import UserRegistrationFailed
from .gameplay import (
    handle_bidding,
    handle_deck_creation,
    handle_stand,
    handle_hit,
    handle_double,
    handle_check_results,
    inform_players,
)
from app.store import Store
from app.store.vk_api.dataclasses import Message, Payload, Update
from .state import StateProcessor
from app.game.models import Game, GameState
from app.player.models import Player, PlayerStatus
from .keyboards import (
    GREETING,
    BID,
    DECISION_MAKING,
    NUMBER_PLAYERS,
    REGISTER_PLAYER,
)
from .const import (
    GREETING_MESSAGE,
    ADD_TO_CHAT_EVENT,
    INVITATION_TO_BID,
)


@StateProcessor.register_handler(GameState.initial_trigger)
async def initial_trigger_handler(store: Store, game: Game, update: Update):
    if update.object.action == ADD_TO_CHAT_EVENT and game is None:
        await store.vk_api.send_message(
            Message(update.object.peer_id, GREETING_MESSAGE, keyboard=GREETING)
        )


@StateProcessor.register_handler(GameState.start_trigger)
async def start_trigger_handler(store: Store, game: Game, update: Update):
    if update.object.payload == Payload(command="greeting"):
        answ_msg, msg, keyboard = (
            "Добро пожаловать",
            "Выберите количество игроков за столом",
            NUMBER_PLAYERS,
        )
        result = await store.game.create_game(update.object.peer_id)
        if isinstance(result, UserRegistrationFailed):
            answ_msg, msg, keyboard = (
                "Ошибка при регистрации игроков",
                "Предоставьте боту права администратора",
                GREETING,
            )
        await store.vk_api.send_answer(update.object, answ_msg)
        await store.vk_api.send_message(
            Message(update.object.peer_id, msg, keyboard=keyboard)
        )


@StateProcessor.register_handler(GameState.menu_selection)
async def menu_selection_handler(store: Store, game: Game, update: Update):
    pass


@StateProcessor.register_handler(GameState.number_of_players)
async def number_of_players_handler(store: Store, game: Game, update: Update):
    game.players_num = int(update.object.payload.command)
    game.state = GameState.player_accession
    try:
        await store.game.update_game(game)
    except Exception as e:
        print(e)
    await store.vk_api.send_answer(
        update.object, f"Игроков за столом {game.players_num}"
    )
    await store.vk_api.send_message(
        Message(
            update.object.peer_id, "Приглашаем всех желающих", keyboard=REGISTER_PLAYER
        )
    )


@StateProcessor.register_handler(GameState.player_accession)
async def player_accession_handler(store: Store, game: Game, update: Update):
    if update.object.payload == Payload(command="register"):
        await store.game.register_player(game, update.object.user_id)
    if update.object.payload == Payload(command="unregister"):
        await store.game.unregister_player(game, update.object.user_id)
    msg = "Игроки набираются"
    tasks = []
    if game.players_num == len(game.players):
        msg = "Стол заполнен. Приступим к игре."
        game.state = GameState.wait_for_bid
        tasks.append(store.game.update_game(game))
        tasks.append(
            store.vk_api.send_message(
                Message(update.object.peer_id, INVITATION_TO_BID, keyboard=BID)
            )
        )

    await asyncio.gather(*tasks, store.vk_api.send_answer(update.object, msg))


@StateProcessor.register_handler(GameState.wait_for_bid)
async def wait_for_bid_handler(store: Store, game: Game, update: Update):
    await handle_bidding(store, game, update)
    players_ready = list(
        filter(lambda x: x.status == PlayerStatus.WAITING, game.players)
    )
    if len(players_ready) == len(game.players):
        await handle_deck_creation(store, game)


@StateProcessor.register_handler(GameState.action_selection)
async def action_selection_handler(store: Store, game: Game, update: Update):
    player_id = update.object.user_id
    player = list(filter(lambda x: x.user.vk_id == player_id, game.players))
    if not player:
        msg = "Вы не играете за этим столом"
        await store.vk_api.send_answer(update.object, msg)
        return
    player = player[-1]
    message = {"double": handle_double, "stand": handle_stand, "hit": handle_hit}[
        update.object.payload.command
    ](player, game)
    await asyncio.gather(
        store.vk_api.send_answer(update.object, message),
        store.game.update_player(player),
        inform_players(
            store.vk_api.send_message, game, "", keyboard=DECISION_MAKING, blind=True
        ),
    )
    players_ready = list(filter(lambda x: x.status == PlayerStatus.STAND, game.players))
    if len(players_ready) == len(game.players):
        await handle_check_results(store, game)


@StateProcessor.register_handler(GameState.continue_or_leave)
async def continue_or_leave_handler(store: Store, game: Game, update: Update):
    if update.object.payload == Payload(command="continue"):
        update.object.payload = Payload(command="greeting")
        await start_trigger_handler(store, None, update)
