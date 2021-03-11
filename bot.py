import sys

from discord.ext import tasks, commands

from cogs.Checker import Checker
from cogs.AdminCommands import AdminCommands
from cogs.VipCommands import VipCommands

SERVER_ADRESS = sys.argv[2]
RCON_PASS = sys.argv[3]

SQL_HOST = '31.31.196.163'
SQL_USER = 'u1103989_stewex'
SQL_PASS = 'winn36podol'
SQL_DATABASE = sys.argv[4]

client = commands.Bot(command_prefix=sys.argv[1], description='PUB-2')
checker = Checker(client, SERVER_ADRESS)


cog_loaded = False

@client.event
async def on_ready():
    client.add_cog(AdminCommands(client, SQL_DATABASE, SERVER_ADRESS, RCON_PASS))
    client.add_cog(VipCommands(client, SERVER_ADRESS, RCON_PASS))
    check.start()
    print(f'ServerBot with ip {SERVER_ADRESS} is ready!')

@tasks.loop(seconds=5)
async def check():
    await checker.start()
    

client.run(sys.argv[5])

