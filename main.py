from discord.ext import commands
from discord import app_commands, Interaction
from pathlib import Path
import asyncio
import discord
import re
import typing
import random

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="az!", intents=intents, status=discord.Status.online, activity=discord.Game(name="az!help"), help_command=None)
api_keys = {
    "owner_id": 000000000000000000, # Replace this with your user ID
    "bot_token": "XXYYzZ" # Replace this with your bot token
}

@bot.event
async def on_ready():
    print(f'Bot connected, logged in as {bot.user}, ID {bot.user.id}')

ignored = (commands.CommandNotFound, commands.BadLiteralArgument, commands.MissingRequiredArgument)

@bot.event
async def setup_hook():
    await bot.load_extension("azupfp")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, ignored):
        return
    elif isinstance(error, commands.CheckFailure):
        await ctx.reply("No Permissions!", ephemeral=True, mention_author=False)
    else:
        raise error

@bot.command()
async def resync(ctx: commands.Context):
    if ctx.author.id == api_keys('owner_id'):
        await bot.tree.sync()
        await ctx.reply(content="Resynced slash commands!", mention_author=False)

@bot.command()
async def guildcount(ctx: commands.Context):
    if ctx.author.id == api_keys('owner_id'):
        await ctx.reply(f"I'm in {len(bot.guilds)} guilds!", mention_author=False)

@bot.hybrid_command(name="help", with_app_command=True, description="Get help with the bot!")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def help(ctx: commands.Context):
    embed = discord.Embed(
        color=discord.Color.from_str("#d33682"), 
        title=f"How do I use Azuframes?", 
        description=f"Using Azuframe is straightforward!\nAll you have to do is run `/azuframe`, or use the inbuilt prefix `az!azuframe`!").set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)
    await ctx.reply(mention_author=False, embed=embed)

@bot.hybrid_command(name="azuframe", description="Get a random frame from Azumanga Daioh")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.rename(episodeindex="episode", frameindex="frame")
async def azuframe(ctx: commands.Context, episodeindex: typing.Optional[int] = None, frameindex: typing.Optional[int] = None):
    folder = Path("azuframes") # Replace this with the path to your Azumanga frames

    episodelist = list(folder.iterdir())
    episodelist.sort()
    if episodeindex == None: # If the user didn't select an episode
        episodeindex = random.randint(1, len(episodelist))
    try:
        episode = episodelist[episodeindex - 1]
    except IndexError: # If the user selected an invalid episode, pick a random valid one
        episodeindex = random.randint(1, len(episodelist))
        episode = episodelist[episodeindex - 1]

    framelist = list(episode.iterdir())
    framelist.sort()
    if frameindex == None: # If the user didn't select a frame
        frameindex = random.randint(1, len(framelist))
    try: # If the user selected an invalid frame, pick a random valid one
        frame = framelist[frameindex - 1]
    except IndexError:
        frameindex = random.randint(1, len(framelist))
        frame = framelist[frameindex - 1]

    percent = round((frameindex / len(framelist)) * 10)
    
    async with ctx.typing():
        embed = discord.Embed(
            color=discord.Color.from_str("#d33682"), 
            description=f"""```ansi
\u001b[0;35mAzumanga Daioh
\u001b[0;37mEpisode \u001b[0;40;31m{episodeindex}
\u001b[0;37mFrame \u001b[0;40;32m{frameindex}\u001b[0;37m of \u001b[0;40;32m{len(framelist)}
\u001b[0;37m[\u001b[0;35m{"█" * percent}\u001b[0;31m{"░" * (10 - percent)}\u001b[0;37m]
```""")
        file = discord.File(frame, filename=f"frame_{frameindex}.png")
        embed.set_image(url=f"attachment://frame_{frameindex}.png")
        await ctx.reply(file=file, embed=embed, mention_author=False)

# Check for the delete command
def indms_or_hasperms(ctx: commands.Context):
    if isinstance(ctx.channel, discord.channel.DMChannel):
        return True
    return ctx.channel.permissions_for(ctx.message.author).manage_messages
    
@bot.hybrid_command(name="delete", description="Delete Azuframe messages!")
@commands.check(indms_or_hasperms)
async def delete(ctx: commands.Context, count: int):
    await ctx.reply(f"Deleting {count} messages!", mention_author=False, ephemeral=True)
    messages = []
    if ctx.prefix != "/":
        count += 1
    async for i in ctx.channel.history():
        if i.author == bot.user:
            messages.append(i)
        for i in range(count):
            if messages != []:
                await messages[0].delete()
                await asyncio.sleep(1)
                messages.pop(0)

@bot.event
async def on_message(message):
    await bot.process_commands(message)

bot.run(api_keys['bot_token'])
