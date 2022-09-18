GREETING = {
    "one_time": True,
    "buttons": [
        [
            {
                "action": {
                    "type": "callback",
                    "payload": '{"command": "start"}',
                    "label": "Старт",
                },
                "color": "positive",
            },
        ]
    ],
}


BID = {
    "one_time": True,
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
    "one_time": True,
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
    "one_time": True,
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
