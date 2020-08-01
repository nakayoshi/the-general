from os import getenv

from discord.ext import commands

bot = commands.Bot(command_prefix="!")
token = getenv("DISCORD_BOT_TOKEN")

bot.run(token)
