GREETING = {
    "one_time": False,
    "buttons": [
        [
            {
                "action": {
                    "type": "callback",
                    "payload": '{"command": "greeting"}',
                    "label": "Начать",
                },
                "color": "positive",
            },
        ]
    ],
}

REGISTER_PLAYER = {
    "one_time": False,
    "buttons": [
        [
            {
                "action": {
                    "type": "callback",
                    "payload": '{"command": "register"}',
                    "label": "Регистрация",
                },
                "color": "positive",
            },
            {
                "action": {
                    "type": "callback",
                    "payload": '{"command": "unregister"}',
                    "label": "Отмена",
                },
                "color": "negative",
            },
        ]
    ],
}


NUMBER_PLAYERS = {
    "one_time": False,
    "buttons": [
        [
            {
                "action": {
                    "type": "callback",
                    "payload": '{"command": "1"}',
                    "label": "1",
                },
                "color": "primary",
            },
            {
                "action": {
                    "type": "callback",
                    "payload": '{"command": "2"}',
                    "label": "2",
                },
                "color": "primary",
            },
            {
                "action": {
                    "type": "callback",
                    "payload": '{"command": "3"}',
                    "label": "3",
                },
                "color": "primary",
            },
            {
                "action": {
                    "type": "callback",
                    "payload": '{"command": "4"}',
                    "label": "4",
                },
                "color": "primary",
            },
            {
                "action": {
                    "type": "callback",
                    "payload": '{"command": "5"}',
                    "label": "5",
                },
                "color": "primary",
            },
        ],
    ],
}


BID = {
    "one_time": False,
    "buttons": [
        [
            {
                "action": {
                    "type": "callback",
                    "payload": '{"command": "bid_10"}',
                    "label": "10",
                },
                "color": "primary",
            },
            {
                "action": {
                    "type": "callback",
                    "payload": '{"command": "bid_20"}',
                    "label": "20",
                },
                "color": "primary",
            },
            {
                "action": {
                    "type": "callback",
                    "payload": '{"command": "bid_50"}',
                    "label": "50",
                },
                "color": "primary",
            },
            {
                "action": {
                    "type": "callback",
                    "payload": '{"command": "bid_100"}',
                    "label": "100",
                },
                "color": "primary",
            },
        ],
        [
            {
                "action": {
                    "type": "callback",
                    "payload": '{"command": "bid_cancel"}',
                    "label": "Отмена",
                },
                "color": "primary",
            },
            {
                "action": {
                    "type": "callback",
                    "payload": '{"command": "finished_bidding"}',
                    "label": "Ставка",
                },
                "color": "positive",
            },
        ],
    ],
}

DECISION_MAKING = {
    "one_time": False,
    "buttons": [
        [
            {
                "action": {
                    "type": "callback",
                    "payload": '{"command": "double"}',
                    "label": "Удвоить",
                },
                "color": "secondary",
            },
            {
                "action": {
                    "type": "callback",
                    "payload": '{"command": "hit"}',
                    "label": "Ещё",
                },
                "color": "positive",
            },
        ],
        [
            {
                "action": {
                    "type": "callback",
                    "payload": '{"command": "stand"}',
                    "label": "Хватит",
                },
                "color": "primary",
            },
        ],
    ],
}

END = {
    "one_time": False,
    "buttons": [
        [
            {
                "action": {
                    "type": "callback",
                    "payload": '{"command": "leave"}',
                    "label": "Закончить",
                },
                "color": "primary",
            },
            {
                "action": {
                    "type": "callback",
                    "payload": '{"command": "continue"}',
                    "label": "Играть Заново",
                },
                "color": "positive",
            },
        ]
    ],
}
