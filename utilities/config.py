import json
import dns.resolver
from urllib.parse import urlparse
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

    def _parse_address(self, address):
        _url = urlparse("//" + address)
        if not _url.hostname:
            raise ValueError(f"Invalid address {address}")
        return (_url.hostname, _url.port)

    def srv_lookup(self, hostname: str):
        _host, _port = self._parse_address(hostname)
        if _port is None:
            _port = 25565
            try:
                _answers = dns.resolver.resolve("_minecraft._tcp." + _host, "SRV")
                if len(_answers):
                    answer = _answers[0]
                    _host = str(answer.target).rstrip(".")
                    _port = int(answer.port)
            except Exception as err:
                print(f"Error: {err}")

        return (_host, _port)


try:
    _config = Config("config.json")
    _data = _config.read_config()

    token = _data["bot"]["token"]
    guild_ids = _data["bot"]["guild_ids"]
    bot_info = _data["bot"]
    pack_info = _data["pack"]
    server = _data["server"]
    hostname = _config.srv_lookup(server["ip"])
    panel = _data["panel"]
    emojis = _data["messages"]["emojis"]
    messages = _data["messages"]["activities"]

except Exception as _error:
    print(traceback_maker(_error, False))
