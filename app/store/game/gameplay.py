import asyncio
from datetime import datetime
from typing import Callable, Union
from app.game.models import Game, GameState
from app.player.models import Player, PlayerStatus
from app.store import Store
from app.store.game.keyboards import DECISION_MAKING, END
from app.store.vk_api.dataclasses import Message, Update
from .deck import Card, GamingDecks, create_deck


async def handle_bidding(store: Store, game: Game, update: Update):
    player_id = update.object.user_id
    player = list(filter(lambda x: x.user.vk_id == player_id, game.players))
    msg = "Вы не играете за этим столом"
    tasks = []
    if player:
        player = player[-1]
        if update.object.payload.command.startswith("bid_"):
            msg = handle_player_bid(player, update)
        else:
            msg = handle_player_finished_biding(player)

        if msg:
            tasks.append(store.game.update_player(player))
    tasks.append(store.vk_api.send_answer(update.object, msg))
    await asyncio.gather(*tasks)


def handle_player_bid(player: Player, update: Update):
    if player.status != PlayerStatus.BETS:
        return f"{player.user.user_name} ждем других игроков за столом"
    try:
        bid = int(update.object.payload.command.split("_")[-1]) + player.bid
        warn_msg = ""
        if bid > player.user.amount:
            bid = player.user.amount
            warn_msg = f"Ставка не может быть больше {player.user.amount}\n"
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
    create_deck(game.id)
    [get_card(2, game.id, pl) for pl in game.players]
    get_card(2, game.id, game)

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
    func: Callable,
    game: Game,
    text: str,
    keyboard: dict,
    blind=False,
    show_results=False,
):
    dealer_hand = game.show_hand(blind)
    players_hand = "\n".join(u.show_hand(show_results) for u in game.players)
    await func(
        Message(
            peer_id=game.chat_id,
            text=f"{text} \n{dealer_hand}\n{players_hand}",
            keyboard=keyboard,
        )
    )


def get_card(value: int, game_id: int, reciever: Union[Game, Player]):
    deck = GamingDecks.get_deck(game_id)
    for _ in range(value):
        try:
            card = deck.pop()
        except IndexError:
            deck = create_deck(game_id)
            card = deck.pop()

        reciever.hand["hand"] = reciever.hand.get("hand", "") + str(card)
        reciever.hand["value"] = reciever.hand.get("value", 0) + card.value


def handle_stand(player: Player, game: Game):
    player.status = PlayerStatus.STAND
    return f"{player.user.user_name} не берет карты"


def handle_double(player: Player, game: Game):
    if player.status != PlayerStatus.STAND:
        player.status = PlayerStatus.HIT
        msg = handle_hit(player, game)
        if player.bid * 2 <= player.user.amount:
            player.bid *= 2
            return f"{msg} и делает удвоение ставки"
        return f"{msg}, слишком мало денег для удвоения"


def handle_hit(player: Player, game: Game):
    if player.status != PlayerStatus.STAND:
        player.status = PlayerStatus.HIT
        get_card(1, game.id, player)
        if player.hand["value"] >= 21:
            player.status = PlayerStatus.STAND
        return f"{player.user.user_name} берет еще карту"


def handle_dealer_hit(game: Game):
    while game.hand["value"] < 17:
        get_card(1, game.id, game)


async def handle_check_results(store: Store, game: Game):
    handle_dealer_hit(game)
    [score(game, player) for player in game.players]
    await inform_players(
        store.vk_api.send_message, game, "Результаты:", END, show_results=True
    ),
    game.state = GameState.continue_or_leave
    game.finished_at = datetime.now()
    tasks = [
        store.game.update_game(game),
        store.game.update_game_stats(game.stats),
        *[store.game.update_player(player) for player in game.players],
        *[store.game.update_user(player.user) for player in game.players],
    ]
    await asyncio.gather(*tasks, return_exceptions=True)


def score(game: Game, player: Player):
    player_hand, game_hand = player.hand["value"], game.hand["value"]
    player_win = (player_hand > game_hand or game_hand > 21) and player_hand <= 21
    dealer_win = (player_hand < game_hand or player_hand > 21) and game_hand <= 21
    draw = player_hand == game_hand

    if player_win:
        player.status = PlayerStatus.WIN
        player.user.amount += player.bid * 2
        player.user.wins += 1
        game.stats.loss += 1
        game.stats.income -= player.bid
    if dealer_win:
        player.status = PlayerStatus.LOSED
        player.user.amount -= player.bid
        player.user.loss += 1
        game.stats.wins += 1
        game.stats.income += player.bid * 2
    if draw:
        player.status = PlayerStatus.DRAW
        # player.user.amount += player.bid
        game.stats.draw += 1
    player.bid = 10
