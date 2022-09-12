from state import StateProcessor, GameState


@StateProcessor.register_handler(GameState.initial_trigger)
async def initial_trigger_handler():
    pass


@StateProcessor.register_handler(GameState.start_trigger)
async def start_trigger_handler():
    pass


@StateProcessor.register_handler(GameState.menu_selection)
async def menu_selection_handler():
    pass


@StateProcessor.register_handler(GameState.number_of_players)
async def number_of_players_handler():
    pass


@StateProcessor.register_handler(GameState.player_accession)
async def player_accession_handler():
    pass


@StateProcessor.register_handler(GameState.wait_for_bid)
async def wait_for_bid_handler():
    pass


@StateProcessor.register_handler(GameState.action_selection)
async def action_selection_handler():
    pass


@StateProcessor.register_handler(GameState.continue_or_leave)
async def continue_or_leave_handler():
    pass
