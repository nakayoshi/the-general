from discord.ext.commands import Bot, Cog, Context, command

from logic.calendar import CalendarImpl


class Calendar(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @command()
    async def add_event(
        self,
        ctx: Context,
        title: str,
        date: str,
        starttime: str,
        endtime: str,
        location: str,
    ) -> None:
        CalendarImpl.add_event(title, date, starttime, endtime, location)
        await ctx.send("Success!")


def setup(bot):
    bot.add_cog(Calendar(bot))
