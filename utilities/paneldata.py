from pydactyl import PterodactylClient


class PanelConnector:
    """Get basic usage from Pterodactyl Panel using external ID as instance name"""

    def __init__(
        self,
        _external_id: str,
        _token_app: str,
        _token_client: str,
        _url: str,
    ):
        """__init__

        Args:
            _external_id (str): External server identifier from Pterodactyl Panel
            _token_app (str): Application API Token, administrative
            _token_client (str): Client API Token, informational
            _url (str): Pterodactyl Panel URL
        """
        self._external_id = _external_id
        self._token_app = _token_app
        self._token_client = _token_client
        self._url = _url

    def _external_to_internal_id(self):
        _application = PterodactylClient(url=self._url, api_key=self._token_app)
        _server = _application.servers.get_server_info(external_id=self._external_id)

        return _server.get("identifier")

    def resource_usage(self):
        """resource_usage - Fetch server's usage from panel, style it and return readable.

        Returns:
            [dict]: Returns dict of used resources by instance.
        """
        _client = PterodactylClient(url=self._url, api_key=self._token_client)
        _usage = _client.client.get_server_utilization(
            self._external_to_internal_id()
        ).get("resources")
        _bytes_to_gb = 1073741824
        _ram_usage = f'{round(_usage["memory_bytes"] / _bytes_to_gb, 2)}GB'
        _cpu_usage = f'{round(_usage["cpu_absolute"], 1)}%'
        _disk_usage = f'{round(_usage["disk_bytes"] / _bytes_to_gb, 2)}GB'

        _usage_dict = {"cpu": _cpu_usage, "ram": _ram_usage, "disk": _disk_usage}

        return _usage_dict
