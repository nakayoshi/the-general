from discord.ext.commands import Bot
from discord.ext.commands import Cog
from discord.ext.commands import Context
from discord.ext.commands import command
from logic.calendar import CalendarImpl

class Calendar(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot


    @command()
    async def add_event(self, ctx: Context, arg: str) -> None:
        result = CalendarImpl.add_event(arg)
        await ctx.send(result)

def setup(bot):
    bot.add_cog(Calendar(bot))
