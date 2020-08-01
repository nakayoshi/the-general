from discord.ext.commands import Bot
from discord.ext.commands import Cog
from discord.ext.commands import Context
from discord.ext.commands import command
from logic.echo import EchoImpl

class Echo(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot


    @command()
    async def echo(self, ctx: Context, arg: str) -> None:
        result = EchoImpl.echo(arg)
        await ctx.send(result)

    @command()
    async def echo_reversed(self, ctx: Context, arg: str) -> None:
        result = EchoImpl.echo_reversed(arg)
        await ctx.send(result)
