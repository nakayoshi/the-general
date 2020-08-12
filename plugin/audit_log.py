from os import getenv
from typing import Optional

from discord import AuditLogEntry, TextChannel
from discord.abc import GuildChannel
from discord.ext.commands import Bot, Cog

from logic.audit_log import ServerLogImpl


class ServerLog(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    async def _send_log(self, channel, action):
        log_channel: TextChannel = await self.bot.fetch_channel(
            int(getenv("LOG_CHANNEL"))
        )

        ignore_category_id: Optional[str] = getenv("IGNORE_CATEGORY")
        if ignore_category_id and int(ignore_category_id) == channel.category.id:
            return

        log_entry_list = await channel.guild.audit_logs(limit=1).flatten()
        log_entry: AuditLogEntry = log_entry_list[0]
        if log_entry.user.bot:
            return

        channel_name = channel.name if action == "delete" else channel.mention
        embed = ServerLogImpl.create_log_embed(
            "channel",
            action,
            log_entry.user,
            channel_name,
            created_at=log_entry.created_at,
        )

        await log_channel.send(embed=embed)

    @Cog.listener()
    async def on_guild_channel_delete(self, channel: GuildChannel) -> None:
        await self._send_log(channel, "delete")

    @Cog.listener()
    async def on_guild_channel_create(self, channel: GuildChannel) -> None:
        await self._send_log(channel, "create")


def setup(bot):
    bot.add_cog(ServerLog(bot))
