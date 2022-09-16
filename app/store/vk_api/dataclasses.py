from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, Union


@dataclass
class Payload:
    command: str

    @classmethod
    def from_dict(cls, data: dict) -> Payload:
        return cls(command=data.get("command"))


@dataclass
class Action:
    type_: str
    member_id: int

    @classmethod
    def from_dict(cls, data: dict) -> Action:
        return cls(type_=data.get("type"), member_id=data.get("member_id"))


@dataclass
class UpdateMessageObject:
    peer_id: int
    user_id: int
    body: str
    action: Action

    @classmethod
    def from_dict(cls, data: dict) -> Action:
        msg = data.get("message")
        return cls(
            peer_id=msg.get("peer_id"),
            user_id=msg.get("from_id"),
            body=msg.get("text"),
            action=Action.from_dict(msg.get("action", {})),
        )


@dataclass
class UpdateEventObject:
    peer_id: int
    user_id: int
    event_id: str
    payload: Payload

    @classmethod
    def from_dict(cls, data: dict) -> Action:
        return cls(
            peer_id=data.get("peer_id"),
            user_id=data.get("user_id"),
            event_id=data.get("event_id"),
            payload=Payload.from_dict(data.get("payload", {})),
        )


@dataclass
class Update:
    type_: str
    object: Union[UpdateMessageObject, UpdateEventObject]

    upd_factory = {
        "message_new": UpdateMessageObject,
        "message_event": UpdateEventObject,
    }

    @classmethod
    def from_dict(cls, data: dict) -> Update:
        upd_type = data.get("type")
        obj_cls = cls.upd_factory.get(upd_type)
        if obj_cls is None:
            return
        return cls(type_=upd_type, object=obj_cls.from_dict(data.get("object")))


@dataclass
class Message:
    # user_id: int
    peer_id: int
    text: str
    keyboard: dict["str", Union[bool, list]] = field(default_factory=dict)


@dataclass
class VkUser:
    vk_id: int
    user_name: str

    @classmethod
    def from_profile(cls, profile: dict[str, Union[str, int]]) -> VkUser:
        return cls(
            vk_id=profile.get("id"),
            user_name=" ".join(
                [
                    profile.get("first_name"),
                    profile.get("last_name"),
                ]
            ),
        )
