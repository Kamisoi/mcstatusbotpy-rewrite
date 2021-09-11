from mcstatus import MinecraftServer


class MinecraftProvider:
    def __init__(self, ip: str, port: int):
        self._ip = ip
        self._port = port
        if self._port == 0:
            self._server = MinecraftServer.lookup(self._ip)
        else:
            self._server = MinecraftServer(self._ip, self._port)

    def ping_server(self):
        return self._server.ping()

    def player_count(self):
        _srv = self._server.status()
        return {"online": _srv.players.online, "max": _srv.players.max}

    def player_list(self):
        if self.player_count().get("online") == 0:
            return "No one is online"
        else:
            return "{}".format(", ".join(self._server.query().players.names))

    def player_list_ext(self):
        if self.player_count().get("online") != 0:
            return self._server.status().raw.get("players").get("sample")
        else:
            return [{"name": "No one is online", "id": "\u202D"}]

    def data_load(self):
        for i in range(len(self.player_list_ext())):
            print(self.player_list_ext()[i].get("id"))
