from discord import Intents
from discord import Embed

from datetime import datetime

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
            await channel.send("Bot status:")

            embed = Embed(title="Bot Aktif", description="The X Files botu artık aktif!",
                          colour=0x00FF00, timestamp=datetime.utcnow())
            fields = [("Yapımcı", "Kerem Arslan#0001", True),
                        ("Ana sunucu Link", "https://discord.gg/Mtjvspv", True),
                        ("Bot Hakkında", "Bu botun yapılma amacı The X Files dizisi hakkındaki Türkiye discord sunucusunu geliştirmektir.", False)]
            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
            embed.set_author(name="The X Files Türkiye", icon_url="https://i.imgur.com/KLjU8fb.jpg")
            embed.set_footer(text="Yakında komut eklemeyi başarabileceğim -umarım-")
            embed.set_thumbnail(url=self.guild.icon_url)
            
            await channel.send(embed=embed)

            '''
            if you want to add extra image in embed: embed.set_image(url="image url or location")
            '''

            '''
            if you want to put photo from database or local, you need follow these steps:
            change "From discord import Embed" to "From discord import Embed, File"
            add a folder named "images" in data folder
            put whatever photo you want
            the path is = "./data/images/image_name.extansion"
            I am going to use imgur because you are able to see the picture :) (and lot easier than local files)
            '''

        else:
            print("Bot yeniden bağlandı!")

    async def on_message(self, message):
        pass

bot = Bot()