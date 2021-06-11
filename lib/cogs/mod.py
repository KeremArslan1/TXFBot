from discord.ext.commands import Cog, Greedy
from discord.ext.commands import CheckFailure
from discord.ext.commands import command, has_permissions, bot_has_permissions
from typing import Optional
from discord import Embed, Member
from datetime import datetime

class Mod(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="kick")
    @bot_has_permissions(kick_members=True)
    @has_permissions(kick_members=True)
    async def kick_members(self, ctx, targets: Greedy[Member], *,  reason: Optional[str] = "Sebep belirtilmedi."):
        if not len(targets):
            await ctx.send("Bir veya birden fazla argüman eksik.")
        else:
            for target in targets:
                if ctx.guild.me.top_role.position > target.top_role.position:
                    await target.kick(reason=reason)
                    embed = Embed(title= "Kullanıcı atıldı.", colour=0x87ceeb, timestamp=datetime.utcnow())
                    embed.set_thumbnail(url=target.avatar_url)
                    fields = [("Kullanıcı", f"<@{target.id}> a.k.a. **{target.display_name}**", False), ("Eylemi gerçekleştiren yönetici", f"<@{ctx.author.id}>", False), ("Sebep", reason, False)]
                    for name, value, inline in fields:
                        embed.add_field(name=name, value=value, inline=inline)
                    await self.log_channel.send(embed=embed)
                    await ctx.send(f"<@{target.id}> başarıyla atıldı!")
                else:
                    await ctx.send(f"<@{target.id}> atılamıyor.")

    @kick_members.error
    async def kick_members_error(self, ctx, exc):
        if isinstance(exc, CheckFailure):
            await ctx.send("Gerekli yetkiye sahip değilsiniz.")

    @command(name="ban")
    @bot_has_permissions(ban_members=True)
    @has_permissions(ban_members=True)
    async def ban_members(self, ctx, targets: Greedy[Member], *,  reason: Optional[str] = "Sebep belirtilmedi."):
        if not len(targets):
            await ctx.send("Bir veya birden fazla argüman eksik.")
        else:
            for target in targets:
                if ctx.guild.me.top_role.position > target.top_role.position:
                    await target.ban(reason=reason)
                    embed = Embed(title= "Kullanıcı yasaklandı.", colour=0x87ceeb, timestamp=datetime.utcnow())
                    embed.set_thumbnail(url=target.avatar_url)
                    fields = [("Kullanıcı", f"<@{target.id}> a.k.a. **{target.display_name}**", False), ("Eylemi gerçekleştiren yönetici", f"<@{ctx.author.id}>", False), ("Sebep", reason, False)]
                    for name, value, inline in fields:
                        embed.add_field(name=name, value=value, inline=inline)
                    await self.log_channel.send(embed=embed)
                    await ctx.send(f"<@{target.id}> başarıyla yasaklandı!")
                else:
                    await ctx.send(f"<@{target.id}> yasaklanılamıyor.")

    @ban_members.error
    async def ban_members_error(self, ctx, exc):
        if isinstance(exc, CheckFailure):
            await ctx.send("Gerekli yetkiye sahip değilsiniz.")
    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.log_channel = self.bot.get_channel(720319247628369950)
            self.bot.cogs_ready.ready_up("mod")



def setup(bot):
    bot.add_cog(Mod(bot))
