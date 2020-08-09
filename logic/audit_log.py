from enum import Enum
from datetime import timezone, timedelta

from discord import Embed


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
    def create_log_embed(cls, log_type, *args, **kwargs):
        if not (handler := getattr(cls, "_" + log_type)):
            raise NoActionError()
        return handler(*args, **kwargs)

    @classmethod
    def _channel(cls, action: str, user, channel_name, created_at):
        data = ActionData[action]
        JST = timezone(timedelta(hours=+9), "JST")

        embed = Embed(title=f"チャンネルが{data.text}されました", color=data.color)
        embed.set_author(name=user.name, icon_url=user.avatar_url)
        embed.add_field(name="チャンネル", value=channel_name, inline=True)
        embed.add_field(
            name="タイムスタンプ",
            value=created_at.replace(tzinfo=JST).isoformat(" ", timespec="seconds"),
            inline=True,
        )
        return embed
