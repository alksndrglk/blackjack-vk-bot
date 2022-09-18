import asyncio
from typing import Callable, Union
from app.game.models import Game, GameState, Player, PlayerStatus
from app.store import Store
from app.store.game.keyboards import DECISION_MAKING, END
from app.store.vk_api.dataclasses import Message, Update
from .deck import Card, GamingDecks, create_deck


async def handle_bidding(store: Store, game: Game, update: Update):
    player_id = update.object.user_id
    player = list(filter(lambda x: x.user.vk_id == player_id, game.players))[-1]
    if update.object.payload.command.startswith("bid_"):
        msg = handle_player_bid(player, update)
    else:
        msg = handle_player_finished_biding(player)

    tasks = []
    if msg:
        tasks.append(store.vk_api.send_answer(update.object, msg))
        tasks.append(store.game.update_player(player))
        await asyncio.gather(*tasks)


def handle_player_bid(player: Player, update: Update):
    if player.status != PlayerStatus.BETS:
        return f"{player.user.user_name} ждем других игроков за столом"
    try:
        bid = int(update.object.payload.command.split("_")[-1]) + player.bid
        warn_msg = ""
        if bid > player.amount:
            bid = player.amount
            warn_msg = f"Ставка не может быть больше {player.amount}\n"
        bid_msg = f"{warn_msg}{player.user.user_name} сделал ставку: {bid}"
    except:
        bid = 10
        bid_msg = f"{player.user.user_name} отменил ставку"
    player.bid = bid
    return bid_msg


def handle_player_finished_biding(player: Player):
    if player.status != PlayerStatus.BETS:
        return f"{player.user.user_name} ждем других игроков за столом"
    player.status = PlayerStatus.WAITING
    return f"{player.user.user_name} готов"


async def handle_deck_creation(store: Store, game: Game):
    deck = create_deck(game_id=game.chat_id)
    [get_card(2, deck, pl) for pl in game.players]
    get_card(2, deck, game)

    tasks = [
        store.game.update_game(game),
        *[store.game.update_player(pl) for pl in game.players],
        inform_players(
            store.vk_api.send_message,
            game,
            "Приступаем к раздаче:",
            DECISION_MAKING,
            blind=True,
        ),
    ]
    game.state = GameState.action_selection
    await asyncio.gather(*tasks)


async def inform_players(
    func: Callable, game: Game, text: str, keyboard: dict, blind=False
):
    dealer_hand = game.show_hand(blind)
    players_hand = "\n".join(u.show_hand() for u in game.players)
    await func(
        Message(
            peer_id=game.chat_id,
            text=f"{text} \n{dealer_hand}\n{players_hand}",
            keyboard=keyboard,
        )
    )


def get_card(value: int, deck: list[Card], reciever: Union[Game, Player]):
    for _ in range(value):
        card = deck.pop()
        reciever.hand["hand"] = reciever.hand.get("hand", "") + str(card)
        reciever.hand["value"] = reciever.hand.get("value", 0) + card.value


def handle_stand(player: Player, game: Game):
    player.status = PlayerStatus.STAND


def handle_double(player: Player, game: Game):
    player.status = PlayerStatus.HIT
    player.bid *= 2
    handle_hit(player, game)


def handle_hit(player: Player, game: Game):
    get_card(1, GamingDecks.get_deck(game.id), player)


def handle_dealer_hit(game: Game):
    while game.hand["value"] < 17:
        get_card(1, GamingDecks.get_deck(game.chat_id), game)


async def handle_check_results(store: Store, game: Game):
    handle_dealer_hit(game)
    [score(game, player) for player in game.players]
    game.state = GameState.continue_or_leave
    tasks = [
        store.game.update_game(game),
        store.game.update_game_stats(game.stats),
        * [store.game.update_player(player) for player in game.players],
        *[store.game.update_user(player.user) for player in game.players],
        inform_players(store.vk_api.send_message, game, "Результаты:", END),
    ]
    await asyncio.gather(*tasks)


def score(game: Game, player: Player):
    player_hand, game_hand = player.hand["value"], game.hand["value"]
    player_win = (player_hand > game_hand or game_hand > 21) and player_hand <= 21
    dealer_win = (player_hand < game_hand or player_hand > 21) and game_hand <= 21
    draw = player_hand == game_hand

    if player_win:
        player.status = PlayerStatus.WIN
        player.amount += player.bid * 2
        player.user.wins += 1
        game.stats.loss += 1
        game.stats.income += player.bid * 2
    if dealer_win:
        player.status = PlayerStatus.LOSED
        player.amount -= player.bid * 2
        player.user.loss += 1
        game.stats.wins += 1
        game.stats.income -= player.bid * 2
    if draw:
        player.status = PlayerStatus.DRAW
        player.amount += player.bid
        game.stats.draw += 1
    player.bid = 10