from os import getenv

from discord.ext import commands
import discord

# bot = commands.Bot(command_prefix="!")
token = getenv("DISCORD_BOT_TOKEN")
INITIAL_PLUGINS = ["plugin.echo", "plugin.calendar"]

# bot.run(token)
class TheGeneralBot(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(command_prefix=commands.when_mentioned_or("!"), **kwargs)
        for cog in INITIAL_PLUGINS:
            try:
                self.load_extension(cog)
                print(f"loaded {cog}")
            except Exception as exc:
                print(
                    f"Could not load extension {cog} due to {exc.__class__.__name__}: {exc}"
                )


bot = TheGeneralBot()
bot.run(token)
