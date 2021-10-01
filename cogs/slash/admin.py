from discord import Embed
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option
from os import listdir
import rcon
from utilities.config import config
from utilities.traceback_own import traceback_maker

try:
    _cfg = config.read_config()
    _base_command = f"{_cfg['bot']['command_name'].lower().replace(' ', '_')}-admin"
    _ranks = _cfg["bot"]["permitted_ranks"]
except Exception as _error:
    print(traceback_maker(_error, False))


class AdminCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_subcommand(
        base=_base_command,
        name="ping",
        description="Bot ping to Discord services",
    )
    @commands.has_any_role(*_ranks)
    async def ping_slash(self, ctx: SlashContext):
        try:
            await ctx.send(
                embed=Embed(title=f"Ping {round(self.bot.latency * 1000)}ms")
            )
        except Exception as _error:
            try:
                await ctx.send(
                    embed=Embed(title="Error has occured!", color=0xCD2D2D).add_field(
                        name="\u202D", value=f"{traceback_maker(_error)}"
                    )
                )
            except Exception as _error:
                print(traceback_maker(_error, False))

    async def whitelist(self, ctx, cmd: str, arg: str = ""):
        try:
            _cfg = await config.async_read_config()
            _hostname = config.srv_lookup(_cfg["server"]["ip"])
            if cmd == "list":
                _response = await rcon.rcon(
                    "whitelist",
                    cmd,
                    host=_hostname[0],
                    port=_cfg["server"]["rcon_port"],
                    passwd=_cfg["server"]["rcon_password"],
                )
            else:
                _response = await rcon.rcon(
                    "whitelist",
                    cmd,
                    arg,
                    host=_hostname[0],
                    port=_cfg["server"]["rcon_port"],
                    passwd=_cfg["server"]["rcon_password"],
                )
            await ctx.send(
                embed=Embed(title="Console:", color=0x2DA8CE)
                .add_field(name="\u202D", value=f"```{_response}```")
                .set_thumbnail(
                    url="https://ik.imagekit.io/zg1ibtq0dje/console_QE-2xKxAE3f.png?updatedAt=1632240690003"
                )
            )
        except Exception as _error:
            try:
                await ctx.send(
                    embed=Embed(title="Error has occured!", color=0xCD2D2D).add_field(
                        name="\u202D", value=f"{traceback_maker(_error, advance=False)}"
                    )
                )
            except Exception as _error:
                print(traceback_maker(_error, advance=False))

    @cog_ext.cog_subcommand(
        base=_base_command,
        name="whitelist",
        description="Add user to bot's server whitelist.",
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
    @commands.has_any_role(*_ranks)
    async def _whitelist_operations(self, ctx, command, player: str = ""):
        await ctx.defer()
        await self.whitelist(ctx=ctx, cmd=command, arg=player)

    async def _change_avatar(self, ctx, url: str = ""):
        try:
            _avatar = await config.get_image(url=url)
            await self.bot.user.edit(avatar=_avatar)
            await ctx.send(
                embed=Embed(title="Changed avatar to:", color=0xFC64A4).set_image(
                    url=url
                )
            )
        except Exception as _error:
            try:
                await ctx.send(
                    embed=Embed(title="Error has occured!", color=0xCD2D2D).add_field(
                        name="\u202D", value=f"{traceback_maker(_error, advance=False)}"
                    )
                )
            except Exception as _error:
                print(traceback_maker(_error, advance=False))

    async def _change_username(self, ctx, username: str):
        try:
            _before_edit_username = self.bot.user.name
            await self.bot.user.edit(username=username)
            await ctx.send(
                embed=Embed(title="Changed username", color=0xFC64A4).add_field(
                    name="\u202D",
                    value=f"Changed from **{_before_edit_username}** to **{username}**",
                )
            )
        except Exception as _error:
            try:
                await ctx.send(
                    embed=Embed(title="Error has occured!", color=0xCD2D2D).add_field(
                        name="\u202D", value=f"{traceback_maker(_error, advance=False)}"
                    )
                )
            except Exception as _error:
                print(traceback_maker(_error, advance=False))

    async def _change_nickname(self, ctx, nickname: str):
        try:
            await ctx.guild.me.edit(nick=nickname)
            await ctx.send(
                embed=Embed(title="Changed nickname", color=0xFC64A4).add_field(
                    name="\u202D",
                    value=f"Changed to **{nickname}**",
                )
            )
        except Exception as _error:
            try:
                await ctx.send(
                    embed=Embed(title="Error has occured!", color=0xCD2D2D).add_field(
                        name="\u202D", value=f"{traceback_maker(_error, advance=False)}"
                    )
                )
            except Exception as _error:
                print(traceback_maker(_error, advance=False))

    @cog_ext.cog_subcommand(
        base=_base_command,
        name="update",
        description="Update bot's Discord",
        options=[
            create_option(
                name="part",
                description="Choose what to update",
                option_type=3,
                required=True,
                choices=[
                    create_choice(name="avatar", value="avatar"),
                    create_choice(name="nickname", value="nickname"),
                    create_choice(name="username", value="username"),
                ],
            ),
            create_option(
                name="data", description="Change to what?", option_type=3, required=True
            ),
        ],
    )
    @commands.has_any_role(*_ranks)
    async def _update_bot(self, ctx: SlashContext, part: str = "", data: str = ""):
        if part == "avatar":
            await self._change_avatar(ctx=ctx, url=data)
        if part == "username":
            await self._change_username(ctx=ctx, username=data)
        if part == "nickname":
            await self._change_nickname(ctx=ctx, nickname=data)

    @cog_ext.cog_subcommand(
        base=_base_command,
        name="config",
        description="Edit bot's config.json within Discord.",
        options=[
            create_option(
                name="key",
                description="Choose what to update",
                option_type=3,
                required=True,
                choices=[
                    create_choice(name="Command base", value="bot, command_name"),
                    create_choice(name="Server's IP", value="server, ip"),
                    create_choice(name="Server's port", value="server, port"),
                    create_choice(name="RCON Password", value="server, rcon_password"),
                    create_choice(name="RCON Port", value="server, rcon_port"),
                    create_choice(name="Modpack's URL", value="pack, url"),
                    create_choice(name="Modpack's Icon URL", value="pack, icon"),
                    create_choice(name="Modpack's name", value="pack, name"),
                    create_choice(name="Modpack's version", value="pack, version"),
                ],
            ),
            create_option(
                name="data",
                description="Change to what?",
                option_type=3,
                required=True,
            ),
        ],
    )
    @commands.has_any_role(*_ranks)
    async def _update_config_bot(self, ctx: SlashContext, key: str, data: str = ""):
        _main_key, _seconadry_key = key.split(", ")
        _placeholder_config = await config.async_read_config()
        config.write_config(_main_key, _seconadry_key, data)
        await ctx.send(
            embed=Embed(title="Changed config values!", color=0x83C183)
            .set_thumbnail(
                url="https://ik.imagekit.io/zg1ibtq0dje/config_6a526hoda.png?updatedAt=1633111496644"
            )
            .add_field(
                name="From:",
                value=f"```py\n'{_main_key.capitalize()}' '{_seconadry_key}': {_placeholder_config[_main_key][_seconadry_key]}\n```",
                inline=True,
            )
            .add_field(
                name="To:",
                value=f"```py\n'{_main_key.capitalize()}' '{_seconadry_key}': {data}\n```",
                inline=True,
            )
        )

    @cog_ext.cog_subcommand(
        base=_base_command,
        name="reload",
        description="Reload extensions.",
        options=[
            create_option(
                name="extension",
                description="Choose what to update",
                option_type=3,
                required=True,
                choices=[
                    create_choice(name="Game commands", value="cogs.slash.minecraft"),
                    create_choice(name="Admin", value="cogs.slash.admin"),
                    create_choice(name="Presence", value="cogs.presence"),
                    create_choice(name="All", value="cogs.all"),
                ],
            )
        ],
    )
    @commands.has_any_role(*_ranks)
    async def _reload(self, ctx: SlashContext, extension: str):
        try:
            if extension == "cogs.all":
                for cog in [
                    "cogs.slash.admin",
                    "cogs.slash.minecraft",
                    "cogs.presence",
                ]:
                    self.bot.unload_extension(cog)
                    self.bot.load_extension(cog)
                    await ctx.send(
                        embed=Embed(
                            title="Cog! Reloaded",
                            description=f"Reloaded cog: ```py\n{cog}\n```",
                            color=0xC0B1DC,
                        ).set_thumbnail(
                            url="https://ik.imagekit.io/zg1ibtq0dje/cogs_Q_QChU23W.png?updatedAt=1633105510396"
                        )
                    )
            else:
                self.bot.unload_extension(extension)
                self.bot.load_extension(extension)
                await ctx.send(
                    embed=Embed(
                        title="Cog! Reloaded",
                        description=f"Reloaded cog: {extension}",
                        color=0xC0B1DC,
                    ).set_thumbnail(
                        url="https://ik.imagekit.io/zg1ibtq0dje/cogs_Q_QChU23W.png?updatedAt=1633105510396"
                    )
                )
        except Exception as _error:
            try:
                await ctx.send(
                    embed=Embed(title="Error has occured!", color=0xCD2D2D).add_field(
                        name="\u202D", value=f"{traceback_maker(_error, advance=False)}"
                    )
                )
            except Exception as _error:
                print(traceback_maker(_error, advance=False))


def setup(bot):
    bot.add_cog(AdminCommands(bot))
