from app.store.bot.dataclassess import Message
from .state import StateProcessor
from app.game.models import GameState


@StateProcessor.register_handler(GameState.initial_trigger)
async def initial_trigger_handler(message: Message, func):
    print(message, func)
    await func(message)


@StateProcessor.register_handler(GameState.start_trigger)
async def start_trigger_handler(message: Message, func):
    await func(message)


@StateProcessor.register_handler(GameState.menu_selection)
async def menu_selection_handler(message: Message, func):
    await func(message)


@StateProcessor.register_handler(GameState.number_of_players)
async def number_of_players_handler(message: Message, func):
    await func(message)


@StateProcessor.register_handler(GameState.player_accession)
async def player_accession_handler(message: Message, func):
    await func(message)


@StateProcessor.register_handler(GameState.wait_for_bid)
async def wait_for_bid_handler(message: Message, func):
    await func(message)


@StateProcessor.register_handler(GameState.action_selection)
async def action_selection_handler(message: Message, func):
    await func(message)


@StateProcessor.register_handler(GameState.continue_or_leave)
async def continue_or_leave_handler(message: Message, func):
    await func(message)
