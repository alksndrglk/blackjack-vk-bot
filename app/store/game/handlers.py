from state import States


@States.register_handler("initial_trigger")
async def initial_trigger_handler():
    pass


@States.register_handler("start_trigger")
async def start_trigger_handler():
    pass


@States.register_handler("menu_selection")
async def menu_selection_handler():
    pass


@States.register_handler("number_of_players")
async def number_of_players_handler():
    pass


@States.register_handler("player_accession")
async def player_accession_handler():
    pass


@States.register_handler("wait_for_bid")
async def wait_for_bid_handler():
    pass


@States.register_handler("action_selection")
async def action_selection_handler():
    pass


@States.register_handler("continue_or_leave")
async def continue_or_leave_handler():
    pass
