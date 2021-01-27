from asyncio import sleep
from apscheduler.triggers.cron import CronTrigger
from glob import glob
import discord
from discord import Intents
from discord import Embed, File

from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord.enums import RelationshipType
from discord.errors import HTTPException, Forbidden
from discord.ext.commands import Bot as BotBase
from discord.ext.commands import Context
from discord.ext.commands import (CommandNotFound, BadArgument, MissingRequiredArgument, CommandOnCooldown)
from discord.ext.commands.core import has_permissions
from discord.ext.commands.errors import BadArgument, CommandOnCooldown
from discord.ext.commands import when_mentioned_or, command, has_permissions

from ..db import db

OWNER_IDS = [385800441709068288]
COGS = [path.split("\\")[-1][:-3] for path in glob("./lib/cogs/*.py")]
IGNORE_EXCEPTIONS = (CommandNotFound, BadArgument)

def get_prefix(bot, message):
    prefix = db.field("SELECT Prefix FROM guilds WHERE GuildID = ?", message.guild.id)
    return when_mentioned_or(prefix)(bot, message)


class Ready(object):
    def __init__(self):
        for cog in COGS:
            setattr(self, cog, False)


    def ready_up(self, cog):
        setattr(self, cog, True)
        print(f"{cog} cog hazır")

    def all_ready(self):
        return all([getattr(self, cog) for cog in COGS])

class Bot(BotBase):
    def __init__(self):
        self.ready = False
        self.cogs_ready = Ready()

        self.guild = None
        self.scheduler = AsyncIOScheduler()

        db.autosave(self.scheduler)
        super().__init__(
            command_prefix=get_prefix,
            owner_ids=OWNER_IDS,
            intents=Intents.all(),
            )

    def setup(self):
        for cog in COGS:
            self.load_extension(f"lib.cogs.{cog}")
            print(f"{cog} cog yüklendı!")

        print("setup complete")

    def run(self, version):
        self.VERSION = version

        print("setup çalıştırılıyor...")
        self.setup()

        with open("./lib/bot/token.0", "r", encoding="utf-8") as tf:
            self.TOKEN = tf.read()

        print("Bot çalıştırılıyor...")
        super().run(self.TOKEN, reconnect =True)

    async def process_commands(self, message):
        ctx = await self.get_context(message, cls=Context)

        if ctx.command is not None and ctx.guild is not None:
            if self.ready:
                await self.invoke(ctx)

            else:
                await ctx.send("Şu an komut çalıştırmaya hazır değilim, birkaç saniye sonra tekrar deneyiniz.")

    async def on_guild_join(self, guild):
        db.execute("INSERT INTO guilds (GuildID, Prefix) VALUES (?, 'T-')", guild.id)

    async def rules_reminder(self):
        channel = self.get_channel(720319247628369950)
        await self.stdout.send("Sunucuyu aktif tutmayı unutmayın @here")

    async def on_connect(self):
        print("Bot bağlandı!")

    async def on_disconnect(self):
        print("Bot'un bağlantısı koptu!")

    async def on_error(self, err, *args, **kwargs):
        if err == "on_command_error":
            await args[0].send("Bir şeyler ters gitti!")

        await self.stdout.send("Bir sorun oluştu!")
        raise

    async def on_command_error(self, ctx, exc):
        if any([isinstance(exc, error) for error in IGNORE_EXCEPTIONS]):
            pass

        elif isinstance(exc, CommandOnCooldown):
            await ctx.send(f"Bu komutu durmadan kullanamazsın, {exc.retry_after:,.2f} saniye sonra tekrardan dene!")
            #await ctx.send(f"That command is on {str(exc.cooldown.type).split(".")[-1]} cooldown, try again in{exc.retry_after:,.2f} secs!")

        elif isinstance(exc, MissingRequiredArgument):
            await ctx.send("Bir veya birden fazla argüman eksik.")
        
        elif hasattr(exc, "original"):
        #elif isinstance(exc.original, HTTPException):
            #await ctx.send("Şu anda mesaj gönderemiyorum!")
            if isinstance(exc.original, Forbidden):
                await ctx.send("Bunu yapmam için gereken yetkiye sahip değilim!")

            else:
                raise exc.original

        else:
            raise exc

    async def on_ready(self):
        if not self.ready:
            self.guild = self.get_guild(720314831818719253)
            self.stdout = self.get_channel(720319247628369950)
            self.scheduler.add_job(self.rules_reminder, CronTrigger(day_of_week=0, hour=12, minute=0, second=0))
            self.scheduler.start()

            await self.stdout.send("Bot status:")

            embed = Embed(title="Bot Aktif", description="The X Files botu artık aktif!",
                          colour=0x00FF00, timestamp=datetime.utcnow())
            fields = [("Yapımcı", "Kerem Arslan#0001", True),
                        ("Ana sunucu Link", "https://discord.gg/Mtjvspv", True),
                        ("Bot Hakkında", "Bu botun yapılma amacı The X Files dizisi hakkındaki Türkiye discord sunucusunu geliştirmektir.", False)]
            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
            embed.set_author(name="TXF Bot", icon_url="https://i.imgur.com/KLjU8fb.jpg")
            embed.set_footer(text="Artık düzgün bir şekilde komut ve embed ekleyebiliyorum!!")
            embed.set_thumbnail(url=self.guild.icon_url)
            
            await self.stdout.send(embed=embed)

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

            while not self.cogs_ready.all_ready():
                await sleep(0.5)


            self.ready = True
            print("Bot hazır!")
            await Bot.change_presence(self, activity=discord.Game(name="T-Help"))
            
            
            
            # Setting `Playing ` status
            #await bot.change_presence(activity=discord.Game(name="a game"))

            # Setting `Streaming ` status
            #await bot.change_presence(activity=discord.Streaming(name="My Stream", url=my_twitch_url))

            # Setting `Listening ` status
            #await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="a song"))

            # Setting `Watching ` status
            #await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="a movie"))
        else:
            print("Bot yeniden bağlandı!")

    async def on_message(self, message):
        if not message.author.bot:
            await self.process_commands(message)

bot = Bot()