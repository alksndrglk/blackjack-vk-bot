import asyncio
from datetime import datetime
from .gameplay import (
    handle_bidding,
    handle_deck_creation,
    handle_stand,
    handle_hit,
    handle_double,
    handle_check_results,
)
from app.store import Store
from app.store.game.accessor import UserRegistrationFailed
from app.store.vk_api.dataclasses import Message, Payload, Update
from .state import StateProcessor
from app.game.models import Game, GameState, PlayerStatus
from .keyboards import GREETING, BID, DECISION_MAKING, END
from .const import (
    GREETING_MAESSAGE,
    PLAYER_HAND,
    PLAYER_BID,
    BYE_MESSAGE,
    ADD_TO_CHAT_EVENT,
    INVITATION_TO_BID,
)


@StateProcessor.register_handler(GameState.initial_trigger)
async def initial_trigger_handler(store: Store, game: Game, update: Update):
    if update.object.action == ADD_TO_CHAT_EVENT and game is None:
        await store.vk_api.send_message(
            Message(update.object.peer_id, GREETING_MAESSAGE, keyboard=GREETING)
        )


@StateProcessor.register_handler(GameState.start_trigger)
async def start_trigger_handler(store: Store, game: Game, update: Update):
    if update.object.payload == Payload(command="start"):
        answ_msg, msg, keyboard = "Игра начинается", INVITATION_TO_BID, BID
        game = await store.game.create_game(update.object.peer_id)
        if isinstance(game, UserRegistrationFailed):
            answ_msg, msg, keyboard = (
                "Ошибка регистрации",
                "Предоставьте боту права администратора!",
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
    pass


@StateProcessor.register_handler(GameState.player_accession)
async def player_accession_handler(store: Store, game: Game, update: Update):
    pass


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
    player = list(filter(lambda x: x.user.vk_id == player_id, game.players))[-1]
    {"double": handle_double, "stand": handle_stand, "hit": handle_hit}[
        update.object.payload.command
    ](player, game)
    await asyncio.gather(
        store.vk_api.send_answer(
            update.object, f"{player.user.user_name} {update.object.payload.command}"
        ),
        store.game.update_player(player),
    )
    players_ready = list(filter(lambda x: x.status == PlayerStatus.STAND, game.players))
    if len(players_ready) == len(game.players):
        await handle_check_results(store, game)


@StateProcessor.register_handler(GameState.continue_or_leave)
async def continue_or_leave_handler(store: Store, game: Game, update: Update):
    game.finished_at = datetime.now()
    update.object.payload = Payload(command="start")
    await asyncio.gather(
        start_trigger_handler(store, None, update), store.game.update_game(game)
    )
