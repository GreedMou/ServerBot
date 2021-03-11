import pymysql
import valve.rcon

from discord.ext import commands
from steamid import SteamID

valve.rcon.RCONMessage.ENCODING = "utf-8"

role_list = []

def convert_time(str_time: str) -> int:
    if str_time == 0:
        return 0

    key = str_time[-1]
    try:
        time_value = int(str_time[:-1])
    except TypeError:
        return None
    if key == 'm':
        return time_value
    elif key == 'h':
        return time_value * 60
    elif key == 'd':
        return time_value * 60 * 24
    elif key == 'w':
        return time_value * 60 * 24 * 7
    elif key == 'M':
        return time_value * 60 * 24 * 30

async def send_report(type, channel, admin, intruder, reason, time):

    text = f"```Администратор: {admin}\nSteamID: {intruder}\n"
        
    if type == "BAN":
        text += f"Действие: Бан\nВремя: {time}\nПричина: {reason}```"
    elif type == "UNBAN":
        text += f"Действие: Разбан\nПричина: {reason}\n```"
    elif type == "KICK":
        text += f"Действие: Кик\nПричина: {reason}\n```"
    elif type == "MUTE":
        text += f"Действие: Мут\nВремя: {time}\nПричина: {reason}\n```"
    await channel.send(text)
    

class AdminCommands(commands.Cog):


    def __init__(self, client, sql_db, rcon_address, rcon_pass):  
        self.client = client
        self.rcon_address = rcon_address
        self.rcon_pass = rcon_pass
        self.db = sql_db
        print("Admin cog loaded!")
        
    @commands.command()
    @commands.has_any_role(693460548444094589, 720386038580903947, 696426895121711126)
    async def ban(self, ctx, str_steam_id: str, str_time: str, *, reason: str):
        steam_id = SteamID(str_steam_id)
        if not steam_id.isValid():
            await ctx.send('`Введите корректно SteamID`', delete_after = 10)
            return
        time = convert_time(str_time)
        if time:
            with valve.rcon.RCON(self.rcon_address, self.rcon_pass) as rcon:
                request = rcon.execute(f"sm_addban {steam_id.steam2(True)} {time} {reason}")
                result = request.text
            if "[MA] Invalid ip" in result:
                await ctx.send('`Введите корректно SteamID`', delete_after = 10)
                return
            await send_report("BAN",ctx.channel, ctx.message.author.name, str_steam_id, reason, str_time)
        else:
            await ctx.send('`Введите корректно время бана`', delete_after = 10)
            return
    
    @commands.command()
    @commands.has_any_role(693460548444094589, 720386038580903947, 696426895121711126)
    async def unban(self, ctx, str_steam_id: str, *, reason: str):
        print(reason)
        steam_id = SteamID(str_steam_id)
        print(f"Database: {self.db}")
        mysql = pymysql.connect(
            host = '31.31.196.163',
            user = 'u1103989_stewex',
            password = 'winn36podol',
            db = self.db
        )
        if not steam_id.isValid():
            await ctx.send('`Введите корректно SteamID`', delete_after = 10)
            return
        cursor = mysql.cursor()
        cursor.execute(f"DELETE FROM sb_bans WHERE authid='{steam_id.steam2(True)}'")
        mysql.commit()
        mysql.close()
        if cursor.rowcount > 0:
            await send_report("UNBAN", ctx.channel, ctx.message.author.name, str_steam_id, reason, '-')
        else:
            await ctx.send('`Введите корректно SteamID`', delete_after = 10)

    @commands.command()
    @commands.has_any_role(693460548444094589, 720386038580903947, 696426895121711126)
    async def kick(self, ctx, str_steam_id, *, reason):
        steam_id = SteamID(str_steam_id)
        if not steam_id.isValid():
            await ctx.send('`Введите корректно SteamID`', delete_after = 10)
            return
        with valve.rcon.RCON(self.rcon_address, self.rcon_pass) as rcon:
            request = rcon.execute(f"sm_kick {steam_id.steam2(True)} {reason}")
            result = request.text
        if "[MA] Invalid ip" in result:
            await ctx.send('`Введите корректно SteamID`', delete_after = 10)
            return
        await send_report("KICK",ctx.channel, ctx.message.author.name, str_steam_id, reason, "-")

    @commands.command()
    @commands.has_any_role(693460548444094589, 720386038580903947, 696426895121711126)
    async def mute(self, ctx, str_steam_id, str_time, *, reason):
        steam_id = SteamID(str_steam_id)
        if not steam_id.isValid():
            await ctx.send('`Введите корректно SteamID`', delete_after = 10)
            return
        time = convert_time(str_time)
        if time:
            with valve.rcon.RCON(self.rcon_address, self.rcon_pass) as rcon:
                request = rcon.execute(f"sm_mute {steam_id.steam2(True)} {time} {reason}")
                result = request.text
            if "[MA] Invalid ip" in result:
                await ctx.send('`Введите корректно SteamID`', delete_after = 10)
                return
            await send_report("MUTE",ctx.channel, ctx.message.author.name, str_steam_id, reason, str_time)
        else:
            await ctx.send('`Введите корректно время бана`', delete_after = 10)
            return

    @commands.command()
    @commands.has_any_role(693460548444094589, 720386038580903947, 696426895121711126)
    async def send(self, ctx, command, arg: str = None):
        if self.rcon_user.count(ctx.message.author.id) > 0:
            with valve.rcon.RCON(self.address, self.password) as rcon:
                if arg is None:
                    response = rcon.execute(command)
                else:
                    response = rcon.execute(f'{command} {arg}')
                value = response.body.decode("utf-8")
                if value == '':
                    await ctx.send("Command send!")
                else:
                    await ctx.send(value)