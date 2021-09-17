import discord
from discord.ext import commands
from discord_slash import SlashCommand
from utilities.config import token, bot_info
from utilities.traceback_own import traceback_maker

try:
    bot = commands.Bot(
        command_prefix=bot_info["prefix"],
        help_command=None,
        intents=discord.Intents.default(),
    )

    slash = SlashCommand(bot, sync_commands=True, sync_on_cog_reload=True)

    bot.load_extension("cogs.presence")
    bot.load_extension("cogs.slash.admin")
    bot.load_extension("cogs.slash.minecraft")

    print("Running...")
    bot.run(token)
except Exception as _error:
    print(traceback_maker(_error, False))
