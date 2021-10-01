from discord import Embed, Colour
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from dinteractions_Paginator import Paginator
from discord_slash.model import ButtonStyle
from utilities.config import config
from utilities.paneldata import PanelConnector
from utilities.gamedata import MinecraftProvider
from utilities.traceback_own import traceback_maker

try:
    _config = config.read_config()
except Exception as _error:
    print(traceback_maker(_error, False))


class MinecraftCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(
        name=_config["bot"]["command_name"],
        description="Check info about modpack, players online and server resource usage.",
    )
    async def _modpack_info(self, ctx: SlashContext):
        try:
            _cfg = await config.async_read_config()
            await ctx.defer()
            try:
                _panel = PanelConnector(
                    _cfg["pack"]["name"],
                    _cfg["panel"]["app-api-token"],
                    _cfg["panel"]["client-api-token"],
                    _cfg["panel"]["panel-url"],
                ).resource_usage()
                _server = MinecraftProvider(_cfg["server"]["ip"])
                _playerlist_user = _server.player_list()
                _playerlist_admin = _server.player_list_ext()

                _info = Embed(
                    title=f"{_cfg['pack']['name']}",
                    description=f"Version: {_cfg['pack']['version']}",
                    url=f"{_cfg['pack']['url']}",
                    color=0xF16436,
                )
                _playerlist = Embed(title="Players online: ", color=Colour.green())
                _usage = Embed(title="Server resource usage", color=0x33404D)

                _info.set_thumbnail(url=_cfg["pack"]["icon"])
                _info.add_field(
                    inline=False,
                    name="Server IP: ",
                    value=f"{_cfg['server']['ip']}",
                )
                _info.add_field(
                    name="Link to modpack: ", value=f"{_cfg['pack']['url']}"
                )

                _playerlist.set_thumbnail(
                    url="https://ik.imagekit.io/zg1ibtq0dje/steve-list_p_2g1zpAP?updatedAt=1631206073416"
                )

                _usage.set_thumbnail(
                    url="https://ik.imagekit.io/zg1ibtq0dje/green-icon_G5vt9kaci.png?updatedAt=1631220072794"
                )
                _usage.add_field(
                    inline=True, name="CPU Usage:", value=f"{_panel['cpu']}"
                )
                _usage.add_field(
                    inline=True, name="RAM Usage:", value=f"{_panel['ram']}"
                )
                _usage.add_field(
                    inline=True, name="Disk space usage:", value=f"{_panel['disk']}"
                )

                if set(_cfg["bot"]["permitted_ranks"]) & set(
                    [_i.id for _i in ctx.author.roles]
                ):
                    for _player_dict in _playerlist_admin:
                        _playerlist.add_field(
                            inline=True,
                            name=f"{_player_dict['name']}",
                            value=f"```{_player_dict['id']}```",
                        )
                else:
                    _playerlist.add_field(
                        inline=True, name="\u202D", value=f"{_playerlist_user}"
                    )

                pages = [_info, _playerlist, _usage]

                await Paginator(
                    bot=self.bot,
                    ctx=ctx,
                    pages=pages,
                    content=None,
                    dm=False,
                    timeout=30,
                    useSelect=False,
                    firstEmoji=_cfg["messages"]["emojis"]["home"],
                    lastEmoji=_cfg["messages"]["emojis"]["end"],
                    prevEmoji=_cfg["messages"]["emojis"]["arrow-left"],
                    nextEmoji=_cfg["messages"]["emojis"]["arrow-right"],
                    prevStyle=ButtonStyle.green,
                    nextStyle=ButtonStyle.green,
                    authorOnly=True,
                    useNotYours=True,
                ).run()

            except Exception as _error:
                await ctx.send(
                    embed=Embed(title="Error has occured!", color=0xCD2D2D).add_field(
                        name="\u202D", value=f"{traceback_maker(_error, advance=False)}"
                    )
                )

        except Exception as _error:
            await ctx.send(traceback_maker(_error))


def setup(bot):
    bot.add_cog(MinecraftCommands(bot))
