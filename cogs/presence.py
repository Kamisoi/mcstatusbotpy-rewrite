import discord
from discord.ext import commands, tasks
from utilities.config import config
from utilities.gamedata import MinecraftProvider
from utilities.traceback_own import traceback_maker

try:
    _cfg = config.read_config()
    _server = MinecraftProvider(name=_cfg["server"]["ip"], port=_cfg["server"]["port"])
except Exception as _error:
    print(traceback_maker(_error, False))


class PresenceUpdater(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.update_presence.start()

    def cog_unload(self):
        self.update_presence.cancel()

    async def on_ready(self):
        try:
            await self.bot.change_presence(
                status=discord.Status.dnd,
                activity=discord.Activity(
                    type=discord.ActivityType.listening,
                    name=_cfg["messages"]["activities"]["connecting"],
                ),
            )
        except Exception as _error:
            print(traceback_maker(_error, False))

    @tasks.loop(seconds=30)
    async def update_presence(self):
        try:
            _data = _server.player_count()
            if _data["online"] == 0:
                await self.bot.change_presence(
                    status=discord.Status.idle,
                    activity=discord.Activity(
                        type=discord.ActivityType.watching,
                        name=_cfg["messages"]["activities"]["idle"],
                    ),
                )
            elif _data["online"] != 0:
                await self.bot.change_presence(
                    status=discord.Status.online,
                    activity=discord.Game(
                        name=_cfg["messages"]["activities"]["online"].format(**_data)
                    ),
                )
        except Exception as _error:
            try:
                await self.bot.change_presence(
                    status=discord.Status.dnd,
                    activity=discord.Activity(
                        type=discord.ActivityType.listening,
                        name=_cfg["messages"]["activities"]["invalid"],
                    ),
                )
                print(traceback_maker(_error, False))
            except Exception as _error:
                print(traceback_maker(_error, False))

    @update_presence.before_loop
    async def before_update(self):
        try:
            await self.bot.wait_until_ready()
            await self.bot.change_presence(
                status=discord.Status.dnd,
                activity=discord.Activity(
                    type=discord.ActivityType.listening,
                    name=_cfg["messages"]["activities"]["connecting"],
                ),
            )
        except Exception as _error:
            print(traceback_maker(_error, False))


def setup(bot):
    bot.add_cog(PresenceUpdater(bot))
