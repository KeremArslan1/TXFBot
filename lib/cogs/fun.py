from random import choice, randint
from typing import Optional
from aiohttp import request
from discord import Member, Embed
from discord.ext.commands import Cog, BucketType
from discord.ext.commands import BadArgument
from discord.ext.commands import command, cooldown
from datetime import datetime

class Fun(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="Selam", aliases=["selam", "Merhaba", "merhaba"], hidden=True)
    async def selam(self, ctx):
        await ctx.send(f"{choice(('Selam', 'Merhaba'))} {ctx.author.mention}!")

    @command(name="zar_at", aliases=["Zar_at", "zar_At", "Zar_At"])
    async def zar_at(self, ctx, Zar_kombinasyonu: str):
        dice, value = (int(term) for term in Zar_kombinasyonu.split("x"))
        rolls = [randint(1, value) for i in range(dice)]

        await ctx.send(" + ".join([str(r) for r in rolls]) + f"= {sum(rolls)}")

    @command(name="tokat", aliases=["Vur", "Tokat", "vur"])
    async def slap_member(self, ctx, kullanıcı: Member, *, sebep: Optional[str] = "sebepsizce"):
        await ctx.send(f"{ctx.author.mention}, {kullanıcı.mention}'a {sebep} sebebiyle vurdu!")

    @command(name="echo", aliases=["eko", "Eko", "Echo", "söyle", "Söyle"])
    async def echo_message(self, ctx, *, mesaj):
            await ctx.message.delete()
            await ctx.send(mesaj)

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("fun")

def setup(bot):
    bot.add_cog(Fun(bot))
    #bot.scheduler.add_job(...)