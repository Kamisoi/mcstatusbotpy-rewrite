import json
import dns.resolver
import aiohttp
from async_files import FileIO
from urllib.parse import urlparse
from utilities.traceback_own import traceback_maker


class ConfigWrapper:
    def __init__(self, path: str = "config.json"):
        self.path = path

    def read_config(self):
        try:
            with open(self.path, "r") as _config_file:
                _data = json.load(_config_file)
                return _data
        except Exception as _error:
            print(traceback_maker(_error, False))

    async def async_read_config(self):
        try:
            async with FileIO(self.path) as _file:
                return json.loads(await _file.read())
        except Exception as _error:
            print(traceback_maker(_error, False))

    def write_config(self, main_key: str, secondary_key: str, value):
        try:
            _data = self.read_config()
            _data[main_key][secondary_key] = value
            with open(self.path, "w") as _config_file:
                json.dump(_data, _config_file, indent=4)

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

    async def get_image(self, url: str):
        """
        Retrieves an image and returns it
        Code humbly provided by @Jalancar#6124
        At Discord: discord-integrations
        """
        async with aiohttp.ClientSession() as image_session:
            async with image_session.get(url) as image_data:
                if image_data.status == 200:
                    return await image_data.read()
                else:
                    return None


try:
    config = ConfigWrapper()
except Exception as _error:
    print(traceback_maker(_error, False))
