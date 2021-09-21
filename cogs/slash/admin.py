from discord import Embed
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option
import rcon
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

    async def whitelist(self, ctx, cmd, arg: str = ""):
        try:
            _host, _port = config.hostname
            if cmd == "list":
                _response = await rcon.rcon(
                    "whitelist",
                    cmd,
                    host=_host,
                    port=config.server["rcon_port"],
                    passwd=config.server["rcon_password"],
                )
            else:
                _response = await rcon.rcon(
                    "whitelist",
                    cmd,
                    arg,
                    host=_host,
                    port=config.server["rcon_port"],
                    passwd=config.server["rcon_password"],
                )
            await ctx.send(
                embed=Embed(title="Console responded:", color=0x2DA8CE)
                .add_field(name="\u202D", value=f"```{_response}```")
                .set_thumbnail(
                    url="https://ik.imagekit.io/zg1ibtq0dje/console_QE-2xKxAE3f.png?updatedAt=1632240690003"
                )
            )
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
        name="whitelist",
        description="Add user to bot's server whitelist.",
        guild_ids=config.guild_ids,
        options=[
            create_option(
                name="command",
                description="Choose action on whitelist",
                option_type=3,
                required=True,
                choices=[
                    create_choice(name="list", value="list"),
                    create_choice(name="add", value="add"),
                    create_choice(name="remove", value="remove"),
                ],
            ),
            create_option(
                name="player",
                description="Insert nickname or UUID of player.",
                option_type=3,
                required=False,
            ),
        ],
    )
    @commands.has_any_role(*config.bot_info["permitted_ranks"])
    async def _whitelist_operations(self, ctx: SlashContext, command, player: str = ""):
        await ctx.defer()
        try:
            await self.whitelist(ctx=ctx, cmd=command, arg=player)
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
