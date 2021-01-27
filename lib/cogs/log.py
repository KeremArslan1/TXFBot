from datetime import datetime
from discord import Embed
from discord.ext.commands import Cog
from ..db import db

class Log(Cog):
	def __init__(self, bot):
		self.bot = bot

	@Cog.listener()
	async def on_ready(self):
		if not self.bot.ready:
			self.log_channel = self.bot.get_channel(720319247628369950)
			self.bot.cogs_ready.ready_up("log")

	@Cog.listener()
	async def on_user_update(self, before, after):
		if before.name != after.name:
			embed = Embed(title=":bookmark_tabs:Nickname Değiştirildi",
                          description=f"{before.name} ismini değiştirdi.",
						  colour=0x87ceeb,
						  timestamp=datetime.utcnow())
            
			fields = [("Öncesi:", before.name, False),
					  ("Sonrası:", after.name, False)]

			for name, value, inline in fields:
				embed.add_field(name=name, value=value, inline=inline)

			await self.log_channel.send(embed=embed)
        
		if before.discriminator != after.discriminator:
			embed = Embed(title=":bookmark_tabs:Etiket Değiştirildi",
						  description=f"{self.log_channel.guild.get_member(before.id)} etiketini değiştirdi.",
						  colour=0x87ceeb,
						  timestamp=datetime.utcnow())

			fields = [("Öncesi:", before.discriminator, False),
					  ("Sonrası:", after.discriminator, False)]

			for name, value, inline in fields:
				embed.add_field(name=name, value=value, inline=inline)

			await self.log_channel.send(embed=embed)
		
		if before.avatar_url != after.avatar_url:
			embed = Embed(title=":bookmark_tabs:Avatar Değiştirildi",
						  description=f"{self.log_channel.guild.get_member(after.id)} avatarını değiştirdi.",
						  colour=0x87ceeb,
						  timestamp=datetime.utcnow())

			embed.set_thumbnail(url=before.avatar_url)
			embed.set_image(url=after.avatar_url)

			await self.log_channel.send(embed=embed)

	@Cog.listener()
	async def on_member_update(self, before, after):
		if before.display_name != after.display_name:
			embed = Embed(title=":bookmark_tabs:Nickname Değiştirildi",
                          description=f"{before.display_name} ismini değiştirdi.",
						  colour=0x87ceeb,
						  timestamp=datetime.utcnow())

			fields = [("Öncesi:", before.display_name, False),
					  ("Sonrası:", after.display_name, False)]

			for name, value, inline in fields:
				embed.add_field(name=name, value=value, inline=inline)

			await self.log_channel.send(embed=embed)

		if before.roles != after.roles:
			embed = Embed(title=":crossed_swords:Roller Güncellendi",
						  description=f"{self.log_channel.guild.get_member(after.id)} kullanıcısının rolleri güncellendi.",
						  colour=0x87ceeb,
						  timestamp=datetime.utcnow())

			fields = [("Öncesi:", ", ".join([r.mention for r in before.roles]), False),
					  ("Sonrası:", ", ".join([r.mention for r in after.roles]), False)]

			for name, value, inline in fields:
				embed.add_field(name=name, value=value, inline=inline)
             
			await self.log_channel.send(embed=embed)

	@Cog.listener()
	async def on_message_edit(self, before, after):
		if not after.author.bot:
			if before.content != after.content:
				embed = Embed(title=":pencil2:Mesaj düzenlendi",
							  description=f"{after.author.display_name} tarafından mesaj düzenlendi.",
							  colour=0x87ceeb,
							  timestamp=datetime.utcnow())

				fields = [("Öncesi:", before.content, False),
						  ("Sonrası:", after.content, False)]

				for name, value, inline in fields:
					embed.add_field(name=name, value=value, inline=inline)

				await self.log_channel.send(embed=embed)

	@Cog.listener()
	async def on_message_delete(self, message):
		if not message.author.bot:
			embed = Embed(title=":x:Message deletion",
						  description=f"{message.author.display_name} tarafından mesaj silindi.",
						  colour=0x87ceeb,
						  timestamp=datetime.utcnow())

			fields = [("Silinen mesaj:", message.content, False)]

			for name, value, inline in fields:
				embed.add_field(name=name, value=value, inline=inline)
            
			await self.log_channel.send(embed=embed)

def setup(bot):
	bot.add_cog(Log(bot))