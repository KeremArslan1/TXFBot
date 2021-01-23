#gonna use this cog in future :D

from discord.ext.commands import Cog
from discord.ext.commands import Command

class weather(Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("weather")

def setup(bot):
    bot.add_cog(weather(bot))