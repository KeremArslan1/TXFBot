from random import choice, randint
from re import search
from typing import Optional
from aiohttp import request
from attr import __description__
from discord.errors import HTTPException
from discord import Member, Embed
from discord.ext.commands import Cog, BucketType
from discord.ext.commands import BadArgument
from discord.ext.commands import command, cooldown
from datetime import datetime
import wikipedia

def wiki_summary(arg):
    definition = wikipedia.summary(arg, sentences=3, chars=1000, auto_suggest=True, redirect=True)
    return definition

class Fun(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="Selam", aliases=["selam", "Merhaba", "merhaba"], brief="Botun gününün güzel geçmesi için ona bir selam verebilirsin :).")
    @cooldown(1, 60, BucketType.user)
    async def selam(self, ctx):
        await ctx.send(f"{choice(('Selam', 'Merhaba'))} {ctx.author.mention}!")

    @command(name="zar_at", aliases=["Zar_at", "zar_At", "Zar_At"], brief="Zar atarak arkadaşlarınla oyunlar oynayabilirsin. 'Zar atma sayısı x Zarın yüz sayısı' şeklinde kullanabilirsin. ")
    @cooldown(1, 15, BucketType.user)
    async def zar_at(self, ctx, Zar_kombinasyonu: str):
        dice, value = (int(term) for term in Zar_kombinasyonu.split("x"))

        if dice <= 25:
            rolls = [randint(1, value) for i in range(dice)]

            await ctx.send(" + ".join([str(r) for r in rolls]) + f"= {sum(rolls)}")

        else:
            await ctx.send("tek seferde çok fazla zar kullanıldı! Ben bu kadar zeki değilim :point_right: :point_left: :pleading_face: ")

    @command(name="tokat", aliases=["Vur", "Tokat", "vur"], brief="Arkadaşlarına tokat atabilirsin, bu sayede onları utandırabilir veya cezalandırabilirsin.")
    @cooldown(1, 60, BucketType.user)
    async def slap_member(self, ctx, kullanıcı: Member, *, sebep: Optional[str] = "sebepsizce"):
        await ctx.send(f"{ctx.author.mention}, {kullanıcı.mention}'a {sebep} sebebiyle vurdu!")

    @slap_member
    async def slap_member_error(self, ctx, exc):
        if isinstance(exc, BadArgument):
            await ctx.send("Bu isimde bir kullanıcı bulamadım!")

    @command(name="echo", aliases=["eko", "Eko", "Echo", "söyle", "Söyle"], brief="Bomboş bir odadaymışsın gibi sesin yankılanır.")
    @cooldown(1, 40, BucketType.user)
    async def echo_message(self, ctx, *, mesaj):
            await ctx.message.delete()
            await ctx.send(mesaj)

    @command(name="Wikipedia", aliases=["Wiki", "wikipedia", "wiki"], brief="Wikipedia'da istediğin konu hakkında araştırma yapabilirsin.")
    @cooldown(1, 25, BucketType.user)
    async def Wikipedia(self, ctx, *,konu):
        embed=Embed(title="Arama yapılıyor...", description=wiki_summary(konu), colour=0x0088ff)
        await ctx.send(embed=embed)

    @command(name="Gerçekler", aliases=["gerçekler", "Facts", "facts"], brief="Hayvanlar hakkında garip bilgiler edinebilirsin, maalesef şu an sadece ingilizce şekilde kullanılabilir.")
    @cooldown(1, 25, BucketType.user)
    async def animal_fact(self, ctx, animal: str):
        if animal.lower() in ("dog", "cat", "panda", "fox", "bird", "koala"):
            fact_url = f"https://some-random-api.ml/facts/{animal.lower()}"
            image_url = f"https://some-random-api.ml/img/{'birb' if animal.lower() == 'bird' else animal.lower()}"
            
            async with request("GET", image_url, headers={}) as response:
                if response.status == 200:
                    data = await response.json()
                    image_link = data["link"]

                else:
                    image_link = None

            async with request("GET", fact_url, headers={}) as response:
                if response.status == 200:
                    data = await response.json()

                    embed = Embed(title=f"{animal.title()} hakkında şaşırtıcı gerçekler", description=data["fact"], color=ctx.author.colour)
                    
                    if image_link is not None:
                        embed.set_image(url=image_link)
                    await ctx.send(embed=embed)

                else:    
                    await ctx.send(f"API {response.status} geri dönüşü yaptı.")
        
        else:
            await ctx.send("Bu hayvan için hiçbir şaşırtıcı gerçek bulunamadı!")

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("fun")

def setup(bot):
    bot.add_cog(Fun(bot))
    #bot.scheduler.add_job(...)