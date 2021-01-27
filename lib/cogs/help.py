from typing import Optional
from attr import __description__
from discord import Embed
from discord.utils import get
from discord.ext.menus import MenuPages, ListPageSource
from discord.ext.commands import Cog
from discord.ext.commands import command


def syntax(command):
	komut_and_aliases = "|".join([str(command), *command.aliases])
	params = []

	for key, value in command.params.items():
		if key not in ("self", "ctx"):
			params.append(f"[{key}]" if "NoneType" in str(value) else f"<{key}>")

	params = " ".join(params)

	return f"`{komut_and_aliases} {params}`"


class HelpMenu(ListPageSource):
	def __init__(self, ctx, data):
		self.ctx = ctx

		super().__init__(data, per_page=3)

	async def write_page(self, menu, fields=[]):
		offset = (menu.current_page*self.per_page) + 1
		len_data = len(self.entries)

		embed = Embed(title=":blue_book:Yardım kitapçığı",
					  description="The X Files Bot'un yardım kitapçığına hoş geldin!",
					  colour=0x87ceeb)
		embed.set_thumbnail(url=self.ctx.guild.me.avatar_url)
		embed.set_footer(text=f"{offset:,}'den {min(len_data, offset+self.per_page-1):,}'e kadar olan komutlar. Toplam {len_data:,} komut bulunmakta.")

		for name, value in fields:
			embed.add_field(name=name, value=value, inline=False)

		return embed

	async def format_page(self, menu, entries):
		fields = []

		for entry in entries:
			fields.append((entry.brief or "Açıklama yok.", syntax(entry)))

		return await self.write_page(menu, fields)


class Help(Cog):
	def __init__(self, bot):
		self.bot = bot
		self.bot.remove_command("help")

	async def komut_help(self, ctx, command):
		embed = Embed(title=f"`{command}` komutu",
					  description=syntax(command),
					  colour=ctx.author.colour)
		embed.add_field(name="Komut açıklaması", value=command.help)
		await ctx.send(embed=embed)

	@command(name="help", aliases=["Help", "Yardım", "yardım", "yardim", "Yardim"], brief="Bu mesajı gösterir.")
	async def show_help(self, ctx, komut: Optional[str]):
		if komut is None:
			menu = MenuPages(source=HelpMenu(ctx, list(self.bot.commands)),
							 delete_message_after=True,
							 timeout=60.0)
			await menu.start(ctx)

		else:
			if (command := get(self.bot.commands, name=komut)):
				await self.komut_help(ctx, command)

			else:
				await ctx.send("Böyle bir komut bulunmamaktadır, lütfen başka bir komut ile tekrar deneyiniz.")

	@Cog.listener()
	async def on_ready(self):
		if not self.bot.ready:
			self.bot.cogs_ready.ready_up("help")


def setup(bot):
	bot.add_cog(Help(bot))