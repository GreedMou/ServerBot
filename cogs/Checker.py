import discord
import valve.rcon
import valve.source.a2s as a2s


class Checker:

    def __init__(self, client, address):
        self.client = client
        self.address = address[1:-1].split()
        port = int(self.address[1])
        self.address = [self.address[0][1:-2], port]
        print(self.address)
        print("Checker initialized!")

    async def start(self):
        try:
            with a2s.ServerQuerier(self.address, timeout=5.0) as server:
                info = server.info()
                players = info['player_count']
                max_players = info['max_players']
            if players == 0:
                await self.client.change_presence(status=discord.Status.idle,
                                                  activity=discord.Game(f"{players}/{max_players} игроков"))
            else:
                await self.client.change_presence(status=discord.Status.online,
                                                  activity=discord.Game(f"{players}/{max_players} игроков"))
        except Exception as E:
            await self.client.change_presence(status=discord.Status.dnd,
                                              activity=discord.Game("Ислам"))
            pass
        except Exception as e:
            print(f"Checker error: {e}")
