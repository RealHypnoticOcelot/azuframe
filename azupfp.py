import discord
import datetime
from discord.ext import commands, tasks
from discord import app_commands, Interaction
from discord.app_commands import Choice
from pathlib import Path
import random
from io import BytesIO

# This module will change the bot's profile picture to a random frame every day at the specified time.

class azupfpchange(commands.Cog):
    def __init__(self, bot):
        self.bot = bot # adding a bot attribute for easier access
        self.azupfp.start()

    def cog_unload(self):
        self.azupfp.cancel()

    @tasks.loop(time=datetime.time(hour=00, minute=00, tzinfo=datetime.timezone.utc)) # utc, midnight
    async def azupfp(self):
        folder = Path("daiohframes")
    
        episodelist = list(folder.iterdir())
        episode = random.choice(episodelist)
        framelist = list(episode.iterdir())
        frame = str(random.choice(framelist))
        with open(frame, "rb") as newAvatar:
            await self.bot.user.edit(avatar=newAvatar.read())


async def setup(bot):
    await bot.add_cog(azupfpchange(bot=bot))
