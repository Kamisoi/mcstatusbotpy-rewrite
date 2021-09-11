import discord
from discord.ext import commands, tasks
import utilities.config
from utilities.gamedata import MinecraftProvider
from utilities.traceback_own import traceback_maker


class PresenceUpdater(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = utilities.config
        self.update_presence.start()

    def cog_unload(self):
        self.update_presence.cancel()

    async def on_ready(self):
        try:
            await self.bot.change_presence(
                status=discord.Status.dnd,
                activity=discord.Activity(
                    type=discord.ActivityType.listening,
                    name=self.config.messages["connecting"],
                ),
            )
        except Exception as _error:
            print(traceback_maker(_error, False))

    @tasks.loop(seconds=utilities.config.bot_info["refreshrate"])
    async def update_presence(self):
        try:
            _srv = MinecraftProvider(self.config.server["ip"], self.config.server["port"])
            _data = _srv.player_count()
            if _data["online"] == 0:
                await self.bot.change_presence(
                    status=discord.Status.idle,
                    activity=discord.Activity(
                        type=discord.ActivityType.watching,
                        name=self.config.messages["idle"],
                    ),
                )
            elif _data["online"] != 0:
                await self.bot.change_presence(
                    status=discord.Status.online,
                    activity=discord.Game(
                        name=self.config.messages["online"].format(**_data)
                    ),
                )
        except Exception as _error:
            try:
                await self.bot.change_presence(
                    status=discord.Status.dnd,
                    activity=discord.Activity(
                        type=discord.ActivityType.listening,
                        name=self.config.messages["invalid"],
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
                    name=self.config.messages["connecting"],
                ),
            )
        except Exception as _error:
            print(traceback_maker(_error, False))


def setup(bot):
    bot.add_cog(PresenceUpdater(bot))
