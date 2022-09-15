from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, Union


@dataclass
class UpdateObject:
    id: int
    peer_id: int
    user_id: int
    body: str
    action: dict = field(default_factory=dict)
    payload: dict = field(default_factory=dict)
    obj: dict = field(default_factory=dict)


@dataclass
class Update:
    type: str
    object: UpdateObject


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
