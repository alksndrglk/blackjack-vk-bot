from app.store.vk_api.dataclasses import Action
from app.web.app import app


GREETING_MESSAGE = """
Добро пожаловать в Чат-Бота БлэкДжек

Цель игры — набрать 21 очко или близкую к этому сумму. Если игрок набирает сумму очков, превышающую 21, то его ставка проигрывает. 
Если сумма очков на картах дилера больше, чем 21, то все ставки, оставшиеся в игре, выигрывают.

Игроки, набравшие сумму очков большую, чем дилер, выигрывают, их ставки оплачиваются 1:1.
Игроки, набравшие сумму очков меньшую, чем дилер, проигрывают.
Если сумма очков игрока равна сумме очков дилера, то объявляется «ничья» или Stay: ставка игрока не выигрывает и не проигрывает.

«БЛЭКДЖЕК»

Это комбинация на первых двух картах с раздачи, дающая в сумме 21 очко (туз и десять или туз и «картинка»). При этом ставки игрока оплачиваются 3:2, если у дилера нет такой же комбинации. «Блэкджек» выигрывает у любой другой комбинации карт, включая комбинации с суммой, равной 21 очку.



Минимальная ставка 10 $ 
Начальный банк 1000 $
Успехов
"""
INVITATION_TO_BID = "Делайте ставки господа"

PLAYER_HAND = "У {} на руках {}"

PLAYER_BID = "{} поставил {}"
PLAYER_CANCEL = "{} оменил ставку"

BYE_MESSAGE = "{} покинул стол, до встречи"

ADD_TO_CHAT_EVENT = Action(
    type_="chat_invite_user",
    member_id=-app.config.bot.group_id,
)
