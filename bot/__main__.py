import os

import discord

from bot import Bot, config

TOKEN = os.getenv("BOT_TOKEN")
PREFIX = config.COMMAND_PREFIX

intents = discord.Intents.all()
intents.presences = False

bot = Bot(
    version="0.0.1",
    command_prefix=PREFIX,
    intents=intents,
    activity=discord.Game(name=f"Call me with {PREFIX}help"),
    case_insensitive=True,
    owner_ids=config.devs,
    heartbeat_timeout=150.0,
)

if __name__ == "__main__":
    bot.run(TOKEN)
