from discord import Intents
from discord import Embed
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord.ext.commands import Bot as BotBase

PREFIX = "T-"
OWNER_IDS = [385800441709068288]


class Bot(BotBase):
    def __init__(self):
        self.PREFIX = PREFIX
        self.ready = False
        self.guild = None
        self.scheduler = AsyncIOScheduler()

        super().__init__(
            command_prefix=PREFIX,
            owner_ids=OWNER_IDS,
            Intents=Intents.all(),
            )

    def run(self, version):
        self.VERSION = version

        with open("./lib/bot/token.0", "r", encoding="utf-8") as tf:
            self.TOKEN = tf.read()

        print("Bot çalıştırılıyor...")
        super().run(self.TOKEN, reconnect =True)

    async def on_connect():
        print("Bot bağlandı!")

    async def on_disconnect(self):
        print("Bot'un bağlantısı koptu!")

    async def on_ready(self):
        if not self.ready:
            self.ready = True
            self.guild = self.get_guild(720314831818719253)
            print("Bot hazır!")

            channel = self.get_channel(720319247628369950)
            await channel.send("Bot hazır!")

            embed = Embed(title="Bot Aktif", description="TXF Botu artık aktif hâlde!")
            fields = [("Name", "Value", True),
                        ("Başka bir alan", "Bu alan başka bir alanın bitişiğinde.", True),
                        ("Çizgide olmayan alan", "Bu alan kendi sırasında gözükecek.", False)]
            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
            await channel.send(embed=embed)
        else:
            print("Bot yeniden bağlandı!")

    async def on_message(self, message):
        pass

bot = Bot()