import discord
from discord.ext import commands
from discord_slash import SlashCommand
from utilities.config import config
from utilities.traceback_own import traceback_maker
import logging

extensions = ["cogs.slash.admin", "cogs.slash.minecraft", "cogs.presence"]


discord_logger = logging.getLogger("discord")
discord_logger.setLevel(logging.CRITICAL)
log = logging.getLogger()
log.setLevel(logging.INFO)
handler = logging.FileHandler(filename="mcwatch.log", encoding="utf-8", mode="w")
log.addHandler(handler)


bot = commands.Bot(
    command_prefix="/",
    help_command=None,
    intents=discord.Intents.default(),
)


@bot.event
async def on_ready():
    print("Logged in as:")
    print(f"Username: {bot.user.name}")
    print(f"ID: {bot.user.id}")
    print("Running...")
    print("------")


def main():
    _config = config.read_config()
    slash = SlashCommand(
        bot,
        debug_guild=_config["bot"]["guild_id"],
        sync_commands=True,
        sync_on_cog_reload=True,
    )

    for cog in extensions:
        try:
            bot.load_extension(cog)
        except Exception as _error:
            print(traceback_maker(_error, False))

    bot.run(_config["bot"]["token"])
    handlers = log.handlers[:]
    for handler in handlers:
        handler.close()
        log.removeHandler(handler)


if __name__ == "__main__":
    main()
