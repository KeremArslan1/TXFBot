from datetime import datetime
from discord import Embed
from discord.ext.commands import Cog
from discord.ext.commands import CheckFailure
from discord.ext.commands import command, has_permissions, cooldown
from discord.ext.commands import Cog, BucketType
from ..db import db
from attr import __description__

class Misc(Cog):
    def __init__(self, bot):
        self.bot = bot
    @command(name="prefix", brief="Sunucunuza özel prefix oluşturmanızı sağlar.")
    @cooldown(1, 25, BucketType.user)
    @has_permissions(manage_guild=True)
    async def change_prefix(self, ctx, new: str):
        if len(new) > 5:
            embed=Embed(title="Prefix kullanılamıyor!", description=f"{new} prefixi kullanılamıyor, Prefix 5 karakterden uzun olamaz.", timestamp=datetime.utcnow(), color=0x00e1ff)
            embed.add_field(name="", value="Lütfen 25 saniye sonra tekrar deneyiniz.", inline=True)
            await ctx.send(embed=embed)
        else:
            db.execute("UPDATE guilds SET Prefix = ? WHERE GuildID = ?", new, ctx.guild.id)
            embed=Embed(title="Prefix değiştirildi!", description=f"Prefixiniz başarıyla {new} olarak değiştirildi. :thumbsup: ", timestamp=datetime.utcnow(), color=0x00e1ff)
            await ctx.send(embed=embed)
    @change_prefix.error
    async def change_prefix_error(self, ctx, exc):
        if isinstance(exc, CheckFailure):
            embed=Embed(title="Prefix kullanılamıyor!", description="Prefix değiştirebilmek için mesajları yönetme yetkisine ihtiyacınız var!", timestamp=datetime.utcnow(), color=0x00e1ff)
            await ctx.send(embed=embed)
    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("misc")    
def setup(bot):
    bot.add_cog(Misc(bot))