from discord import Embed, Colour
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from dinteractions_Paginator import Paginator
from discord_slash.model import ButtonStyle
# from discord_slash.utils.manage_components import create_button, create_actionrow
import utilities.config as _config
from utilities.paneldata import PanelConnector
from utilities.gamedata import MinecraftProvider
from utilities.traceback_own import traceback_maker

class MinecraftCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(
        name=_config.pack_info['name'].lower().replace(" ", "_"),
        description="Obtain info about modpack we're hosting!",
        guild_ids=_config.guild_ids
    )
    async def _modpack_info(self, ctx: SlashContext):
        try:
            # Delay execution
            await ctx.defer()   
            try:
                # Set variables
                _panel = PanelConnector(_config.pack_info['name'], _config.panel['app-api-token'], _config.panel['client-api-token'], _config.panel['panel-url']).resource_usage()
                _server = MinecraftProvider(_config.server['ip'], _config.server['port'])
                _plist_user = _server.player_list()
                _plist_admin = _server.player_list_ext()

                # Prepare embeds
                _info = Embed(
                    title=f"{_config.pack_info['name']}",
                    description=f"Version: {_config.pack_info['version']}",
                    url=f"{_config.pack_info['url']}",
                    color=0xF16436
                )
                _list = Embed(
                    title="Players online: ",
                    color=Colour.green()
                )
                _usage = Embed(
                    title="Server resource usage",
                    color=0x33404D
                )

                _info.set_thumbnail(url=_config.pack_info['icon'])
                _info.add_field(inline=False, name="Server IP: ", value=f"{_config.server['ip']}")
                _info.add_field(name="Link to modpack: ", value=f"{_config.pack_info['url']}")

                _list.set_thumbnail(url="https://ik.imagekit.io/zg1ibtq0dje/steve-list_p_2g1zpAP?updatedAt=1631206073416")

                _usage.set_thumbnail(url="https://ik.imagekit.io/zg1ibtq0dje/green-icon_G5vt9kaci.png?updatedAt=1631220072794")
                _usage.add_field(inline=True, name="CPU Usage:", value=f"{_panel['cpu']}")
                _usage.add_field(inline=True, name="RAM Usage:", value=f"{_panel['ram']}")
                _usage.add_field(inline=True, name="Disk space usage:", value=f"{_panel['disk']}")  

                # Internal permission check for extended player list as of today
                _roles = ctx.author.roles
                _roles_ids = []
                for _i in _roles:
                    _roles_ids.append(_i.id)
                _ranks = _config.bot_info['permitted_ranks']

                if set(_ranks) & set(_roles_ids):
                    for _it in range(len(_plist_admin)):
                        _list.add_field(
                            inline=True,
                            name=f"{_plist_admin[_it]['name']}",
                            value=f"UUID: {_plist_admin[_it]['id']}"
                        )

                    # _usage_buttons = [
                    #     create_button(
                    #         style=ButtonStyle.green,
                    #         label="Start"
                    #     ),
                    #     create_button(
                    #         style=ButtonStyle.gray,
                    #         label="Restart"
                    #     ),
                    #     create_button(
                    #         style=ButtonStyle.red,
                    #         label="Stop"
                    #     )
                    # ]
                    # _usage_action_row = create_actionrow(*_usage_buttons)
                    # async def _usage_row(self, button_ctx):
                    #     pass
                    # _usage.add_field(inline=False, name="Take actions: ", value=_usage_action_row)

                else:
                    # _usage_buttons = []
                    # _usage_action_row = create_actionrow(*_usage_buttons) 
                    # async def _usage_row(self, button_ctx):
                    #     pass
                    _list.add_field(
                        inline=True,
                        name="\u202D",
                        value=f"{_plist_user}"
                    )

                # Put embeds into list for paginator
                pages = [_info, _list, _usage]

                # Define Paginator and run it
                await Paginator(
                    bot=self.bot,
                    ctx=ctx,
                    pages=pages,
                    content=None,
                    dm=False,
                    timeout=30,
                    useSelect=False,
                    firstEmoji=_config.emojis['home'],
                    lastEmoji=_config.emojis['end'],
                    prevEmoji=_config.emojis['arrow-left'],
                    nextEmoji=_config.emojis['arrow-right'],
                    prevStyle=ButtonStyle.green,
                    nextStyle=ButtonStyle.green,
                    # customActionRow=[_usage_action_row, _usage_row],
                    authorOnly=True,
                    useNotYours=True
                ).run()
            except Exception as _error:
                await ctx.send(traceback_maker(_error))

        except Exception as _error:
            await ctx.send(traceback_maker(_error))


def setup(bot):
    bot.add_cog(MinecraftCommands(bot))