import discord
from discord.ext import commands
from discord.utils import get

import valve.rcon
valve.rcon.RCONMessage.ENCODING = "utf-8"

role_list = []


class VipCommands(commands.Cog):

    def __init__(self, client, address, password):
        self.client=client
        self.address = address
        self.password = password
        self.type_message = None
        self.time_message = None
        self.ok_message = None
        self.steam_id = None
        self.type = None
        self.time = None
        self.type_value = None
        self.time_value = None
        self.channel = None
        self.vip = False

    @commands.command()
    @commands.has_any_role(693460548444094589, 720386038580903947, 696426895121711126)
    async def vip(self, ctx, steam_id):
        self.vip = True
        self.steam_id = steam_id
        self.channel = ctx.message.channel
        self.type_message = await self.init_type_message(self.channel)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.member.bot is False and self.vip:
            message = await self.channel.fetch_message(payload.message_id)
            reaction = get(message.reactions, emoji=payload.emoji.name)
            if payload.emoji.name == "1️⃣":
                # Если реакцию поставили к type_message
                if self.type_message.id == payload.message_id:
                    await self.set_type(reaction, "BUNNYHOP", "Баннихоп")
                # Если реакцию поставили к time_message
                if self.time_message.id == payload.message_id:
                    await self.set_time(reaction, "604800", "1 неделя")

            if payload.emoji.name == "2️⃣":
                # Если реакцию поставили к type_message
                if self.type_message.id == payload.message_id:
                    await self.set_type(reaction, "PREMIUM", "Премиум")
                # Если реакцию поставили к time_message
                if self.time_message.id == payload.message_id:
                    await self.set_time(reaction, "1209600", "1 месяц")

            if payload.emoji.name == "3️⃣":
                # Если реакцию поставили к type_message
                if self.type_message.id == payload.message_id:
                    await self.set_type(reaction, "MODER", "Модератор")
                # Если реакцию поставили к time_message
                if self.time_message.id == payload.message_id:
                    await self.set_time(reaction, "2419200", "2 месяца")

            if payload.emoji.name == "4️⃣":
                # Если реакцию поставили к type_message
                if self.type_message.id == payload.message_id:
                    await self.set_type(reaction, "ADMIN", "Администратор")
                # Если реакцию поставили к time_message
                if self.time_message.id == payload.message_id:
                    await self.set_time(reaction, "0", "Навсегда")

            if payload.emoji.name == "✔":
                # Если реакцию поставили к type_message
                if self.ok_message.id == payload.message_id:
                    if reaction and reaction.count > 1:
                        await self.ok_message.delete()
                        with valve.rcon.RCON(self.address, self.password) as rcon:
                            command = "sm_addvip "+f"\"{self.steam_id}\" "+f"\"{self.type}\" "+f"\"{self.time}\""
                            send = rcon.execute(command)
                            bad_name = await self.bad_name(self.channel, send.text)
                            if not bad_name:
                                rcon.execute("sm_refresh_vips")
                                self.time_message = await self.init_successful_message(self.channel)
                            self.restart()

            if payload.emoji.name == "❌":
                # Если реакцию поставили к ok_message
                if self.ok_message.id == payload.message_id:
                    if reaction and reaction.count > 1:
                        await self.ok_message.delete()
                        self.restart()

    async def init_type_message(self, channel):
        embed = discord.Embed(title="Выдача привилегии",
                              description="Выбор привилегии",
                              color=0xff8000)
        embed.set_thumbnail(url="https://timebar.ua/uploads/images/blog/clock-icon--1-.png")
        embed.add_field(name="Выберите привилегию",
                        value=":one: Баннихоп\n\n"
                              ":two: Премиум\n\n"
                              ":three: Модератор\n\n"
                              ":four: Администратор",
                              inline=False)
        embed.set_footer(text=self.steam_id)
        message = await channel.send(embed=embed)
        await message.add_reaction("1️⃣")
        await message.add_reaction("2️⃣")
        await message.add_reaction("3️⃣")
        await message.add_reaction("4️⃣")
        return message

    async def init_time_message(self, channel):
        embed = discord.Embed(title="Выдача привилегии",
                              description="Выбор времени",
                              color=0xff8000)
        embed.set_thumbnail(url="https://timebar.ua/uploads/images/blog/clock-icon--1-.png")
        embed.add_field(name="Выберите срок привилегии:",
                        value=":one: 1 Неделя\n\n"
                              ":two: 1 Месяц\n\n"
                              ":three: 2 Месяца\n\n"
                              ":four: Навсегда",
                              inline=False)
        embed.set_footer(text=self.steam_id)
        message = await channel.send(embed=embed)
        await message.add_reaction("1️⃣")
        await message.add_reaction("2️⃣")
        await message.add_reaction("3️⃣")
        await message.add_reaction("4️⃣")
        return message

    async def init_ok_message(self, channel):
        embed = discord.Embed(title="Выдача привилегии",
                              description="Проверка данных",
                              color=0xb2d979)
        embed.set_thumbnail(url="https://timebar.ua/uploads/images/blog/clock-icon--1-.png")
        embed.add_field(name="Проверьте данные:",
                        value=f"STEAM_ID: **{self.steam_id}**\n"
                              f"Вид привилегии: **{self.type_value}**\n"
                              f"Время: **{self.time_value}**",
                              inline=False)
        embed.set_footer(text=self.steam_id)
        message = await channel.send(embed=embed)
        await message.add_reaction("✔")
        await message.add_reaction("❌")
        return message

    async def init_successful_message(self, channel):
        embed = discord.Embed(title="Выдача привилегии",
                              description="Успешно",
                              color=0x1ab345)
        embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/701355854070284288.png?v=1")
        embed.add_field(name="Успешно",
                        value=f"STEAM_ID: **{self.steam_id}**\n"
                              f"Вид привилегии: **{self.type_value}**\n"
                              f"Время: **{self.time_value}**",
                              inline=False)
        embed.set_footer(text=self.steam_id)
        await channel.send(embed=embed)

    def restart(self):
        self.type_message = None
        self.time_message = None
        self.ok_message = None
        self.steam_id = None
        self.type = None
        self.time = None
        self.type_value = None
        self.time_value = None
        self.channel = None
        self.vip = False

    async def set_type(self, reaction, type, type_value):
        if reaction and reaction.count > 1:
            self.type = type
            self.type_value = type_value
            await self.type_message.delete()
            self.time_message = await self.init_time_message(self.channel)

    async def set_time(self, reaction, tume, time_value):
        if reaction and reaction.count > 1:
            self.time = tume
            self.time_value = time_value
            await self.time_message.delete()
            self.ok_message = await self.init_ok_message(self.channel)

    async def bad_name(self, channel, reason):
        if reason.count("[SM] No matching client was found") > 0:
            await channel.send("```"
                               "Неверный SteamID"
                               "```",
                               delete_after=5)
            return True
        else:
            return False
