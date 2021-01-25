from datetime import datetime
from typing import Optional
from discord import Embed, Member
from discord.ext.commands import Cog
from discord.ext.commands import CheckFailure
from discord.ext.commands import command, has_permissions, cooldown

class Info(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="Kullanıcı_Bilgisi", aliases=["K_B",])
    async def Kullanıcı_Bilgisi(self, ctx, target: Optional[Member]):
        target = target or ctx.author
        embed = Embed(title="Kullanıcı bilgisi",
                      colour=0x87ceeb,
                      timestamp=datetime.utcnow(),
                      )

        fields = [("İsim:", str(target), True),
				  ("ID", target.id, True),
				  ("Bot:", target.bot, True),
				  ("Yetki:", target.top_role.mention, True),
				  ("Durum:", str(target.status).title(), True),
				  ("Aktivite:", f"{str(target.activity.type).split('.')[-1].title() if target.activity else 'N/A'} {target.activity.name if target.activity else ''}", True),
				  ("Discord'a katılma tarihi:", target.created_at.strftime("%d/%m/%Y %H:%M:%S"), True),
				  ("Sunucuya katılma tarihi:", target.joined_at.strftime("%d/%m/%Y %H:%M:%S"), True),
				  ("Boost:", bool(target.premium_since), True)]
        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)
        await ctx.send(embed=embed)

    @command(name="Sunucu_Bilgisi", aliases=["S_B"])
    async def Sunucu_Bilgisi(self, ctx):
        embed = Embed(title="Sunucu Bilgisi",
					  colour=ctx.guild.owner.colour,
					  timestamp=datetime.utcnow())

        embed.set_thumbnail(url=ctx.guild.icon_url)

        statuses = [len(list(filter(lambda m: str(m.status) == "Çevrimiçi", ctx.guild.members))),
					len(list(filter(lambda m: str(m.status) == "Uzakta", ctx.guild.members))),
					len(list(filter(lambda m: str(m.status) == "Rahatsız Etmeyin", ctx.guild.members))),
					len(list(filter(lambda m: str(m.status) == "Çevrimdışı", ctx.guild.members)))]

        fields = [("ID:", ctx.guild.id, True),
				  ("Kurucu:", ctx.guild.owner, True),
				  ("Bölge:", ctx.guild.region, True),
				  ("Oluşturulma tarihi:", ctx.guild.created_at.strftime("%d/%m/%Y %H:%M:%S"), True),
				  ("Üye sayısı:", len(ctx.guild.members), True),
				  ("Kullanıcı sayısı:", len(list(filter(lambda m: not m.bot, ctx.guild.members))), True),
				  ("Bot sayısı:", len(list(filter(lambda m: m.bot, ctx.guild.members))), True),
				  ("Yasaklı üye sayısı:", len(await ctx.guild.bans()), True),
				  ("Durum:", f"🟢 {statuses[0]} 🟠 {statuses[1]} 🔴 {statuses[2]} ⚪ {statuses[3]}", True),
				  ("Metin kanalı sayısı:", len(ctx.guild.text_channels), True),
				  ("Ses kanalı sayısı:", len(ctx.guild.voice_channels), True),
				  ("Kategori sayısı:", len(ctx.guild.categories), True),
				  ("Rol sayısı:", len(ctx.guild.roles), True),
				  ("Davet sayısı:", len(await ctx.guild.invites()), True),
				  ("\u200b", "\u200b", True)]

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        await ctx.send(embed=embed)

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("info")
def setup(bot):
    bot.add_cog(Info(bot))