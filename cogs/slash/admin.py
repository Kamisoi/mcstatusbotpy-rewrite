from discord import Embed
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
import utilities.config as config
from utilities.traceback_own import traceback_maker


class AdminCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_subcommand(
        base="admin",
        name="ping",
        description="Bot ping to Discord services",
        guild_ids=config.guild_ids,
    )
    @commands.has_any_role(*config.bot_info["permitted_ranks"])
    async def ping_slash(self, ctx: SlashContext):
        try:
            embed = Embed(title=f"Ping {round(self.bot.latency * 1000)}ms")
            await ctx.send(embed=embed)
        except Exception as _error:
            try:
                await ctx.send(
                    embed=Embed(title="Error has occured!", color=0xCD2D2D).add_field(
                        name="\u202D", value=f"{traceback_maker(_error)}"
                    )
                )
            except Exception as _error:
                print(traceback_maker(_error, False))

    @cog_ext.cog_subcommand(
        base="admin",
        subcommand_group="change",
        name="username",
        description="Change bot's username",
        guild_ids=config.guild_ids,
    )
    @commands.has_any_role(*config.bot_info["permitted_ranks"])
    async def change_username(self, ctx: SlashContext, username):
        try:
            await self.bot.user.edit(username=username)
            await ctx.send(f"Changed username to: **{username}**")
        except Exception as _error:
            try:
                await ctx.send(
                    embed=Embed(title="Error has occured!", color=0xCD2D2D).add_field(
                        name="\u202D", value=f"{traceback_maker(_error)}"
                    )
                )
            except Exception as _error:
                print(traceback_maker(_error, advance=False))

    @cog_ext.cog_subcommand(
        base="admin",
        subcommand_group="change",
        name="nickname",
        description="Change bot's nickname",
        guild_ids=config.guild_ids,
    )
    @commands.has_any_role(*config.bot_info["permitted_ranks"])
    async def change_nickname(self, ctx: SlashContext, nickname):
        try:
            await ctx.guild.me.edit(nick=nickname)
            await ctx.send(f"Changed nickname to: **{nickname}**")
        except Exception as _error:
            try:
                await ctx.send(
                    embed=Embed(title="Error has occured!", color=0xCD2D2D).add_field(
                        name="\u202D", value=f"{traceback_maker(_error)}"
                    )
                )
            except Exception as _error:
                print(traceback_maker(_error, advance=False))


def setup(bot):
    bot.add_cog(AdminCommands(bot))
