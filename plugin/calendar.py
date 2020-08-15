from discord.ext.commands import Bot, Cog, Context, command

from logic.calendar import GoogleCalendarImpl, Event


class Calendar(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @command()
    async def add_event(
        self,
        ctx: Context,
        title: str,
        date: str,
        start_time: str,
        end_time: str,
        location: str,
    ) -> None:
        calendar = GoogleCalendarImpl()
        new_event = Event(title, date, start_time, end_time, location)
        calendar.add_event(new_event)
        await ctx.send("Success!")


def setup(bot):
    bot.add_cog(Calendar(bot))
