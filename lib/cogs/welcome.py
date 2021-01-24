from discord import Forbidden
from discord.ext.commands import Cog
from discord.ext.commands import command

from ..db import db


class Welcome(Cog):
	def __init__(self, bot):
		self.bot = bot

	@Cog.listener()
	async def on_ready(self):
		if not self.bot.ready:
			self.bot.cogs_ready.ready_up("welcome")

	@Cog.listener()
	async def on_member_join(self, member):
		db.execute("INSERT INTO exp (UserID) VALUES (?)", member.id)
		await self.bot.get_channel(748180227095789620).send(f"Merhaba {member.mention}, **{member.guild.name}** sunucusuna hoş geldin!")

		try:
			await member.send(f"Merhaba, **{member.guild.name}** sunucusuna hoş geldin!")

		except Forbidden:
			pass

		#await member.add_roles(member.guild.get_role(748171036784197752))

	@Cog.listener()
	async def on_member_remove(self, member):
		db.execute("DELETE FROM exp WHERE UserID = ?", member.id)
		await self.bot.get_channel(748180227095789620).send(f"{member.display_name} sunucuyu terk etti.")


def setup(bot):
	bot.add_cog(Welcome(bot))