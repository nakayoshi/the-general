from datetime import datetime
from enum import Enum
from typing import Any

from discord import Embed
from discord.abc import User


class NoActionError(Exception):
    pass


class ActionData(Enum):
    create = ("作成", 0x5CB85C)
    delete = ("削除", 0xD9534F)

    def __init__(self, text, color):
        self.text = text
        self.color = color


class ServerLogImpl:
    @classmethod
    def create_log_embed(cls, log_type: str, *args, **kwargs) -> Any:
        if (handler := getattr(cls, "_" + log_type, None)) is None:
            raise NoActionError()
        return handler(*args, **kwargs)

    @classmethod
    def _channel(
        cls, action: str, user: User, channel_name: str, created_at: datetime
    ) -> Embed:
        data = ActionData[action]
        embed = Embed(
            title=f"チャンネルが{data.text}されました", color=data.color, timestamp=created_at
        )
        embed.set_author(name=user.name, icon_url=user.avatar_url)
        embed.add_field(name="チャンネル", value=channel_name, inline=True)
        return embed
