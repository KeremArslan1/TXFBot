from discord.ext.commands import Cog, BucketType
from discord.ext.commands import command, cooldown
from discord import Embed
import requests
import json
from datetime import datetime
from pprint import pprint
from attr import __description__

def parse_data(data):
    data = data['main']
    del data['humidity']
    del data['pressure']
    return data

with open('./lib/bot/api.json', 'r') as api:
    api_key = json.load(api)

API_KEY = api_key["API_KEY"]
dereceler = {
    'temp' : 'Sıcaklık:',
    'feels_like' : 'Hissedilen:',
    'temp_max' : 'En Yüksek Sıcaklık:',
    'temp_min' : 'En Düşük Sıcaklık:',
    'description' : 'Hava durumu:'
}


class weather(Cog):
    def __init__(self, bot,):
        self.bot = bot

    @command(name="Hava_Durumu", aliases=["Hava", "hava", "hava_durumu", "Hava_durumu", "hava_Durumu"], brief="Hava durumunu kontrol edebilirsin.")
    @cooldown(1, 60, BucketType.guild)
    async def Hava_Durumu(self, ctx, *,konum):
        if len(konum) >= 1:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={konum}&appid={API_KEY}&units=metric"
            data = json.loads(requests.get(url).content)
            data = parse_data(data)
            try:
                embed=Embed(title=f"{konum}'da Hava Durumu", description="Tüm dereceler °C birimini kullanmaktadır.", colour=0x87ceeb, timestamp=datetime.utcnow())
                for key in data:
                    embed.add_field(name=dereceler[key], value=str(data[key]), inline=False)
                await ctx.send(embed=embed)
            except KeyError:
                embed=Embed(title="Hata!", description=f"{konum} konumundan hava durumu verisi alınırken bir hata oluştu!", colour=0x87ceeb, timestamp=datetime.utcnow())
                await ctx.send(embed=embed)

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("weather")

def setup(bot):
    bot.add_cog(weather(bot))