import json
from utilities.traceback_own import traceback_maker


class Config:
    def __init__(self, path: str):
        self.path = path

    def read_config(self):
        try:
            with open(self.path, "r") as _config_file:
                _data = json.load(_config_file)
                return _data
        except Exception as _error:
            print(traceback_maker(_error, False))


try:
    _data = Config("config.json").read_config()

    token = _data["bot"]["token"]
    guild_ids = _data["bot"]["guild_ids"]
    bot_info = _data["bot"]
    pack_info = _data["pack"]
    server = _data["server"]
    panel = _data["panel"]
    emojis = _data["messages"]["emojis"]
    messages = _data["messages"]["activities"]

except Exception as _error:
    print(traceback_maker(_error, False))
