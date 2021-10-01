from mcstatus import MinecraftServer


class MinecraftProvider:
    def __init__(self, name: str = "localhost", port: int = 0):
        self._name = name
        self._port = port
        if self._port == 0:
            self._server = MinecraftServer.lookup(self._name)
        else:
            self._server = MinecraftServer(self._name, self._port)

    def ping_server(self):
        return self._server.ping()

    def player_count(self):
        _srv = self._server.status()
        return {"online": _srv.players.online, "max": _srv.players.max}

    def player_list_ext(self):
        if self.player_count().get("online"):
            return self._server.status().raw.get("players").get("sample")
        else:
            return [{"name": "No one is online", "id": "\u202D"}]

    def player_list(self):
        return ", ".join([_player.get("name") for _player in self.player_list_ext()])
