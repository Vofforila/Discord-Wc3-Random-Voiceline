from asyncio import sleep

import pathlib
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import random
import asyncio

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

print(f"Token: {TOKEN}")

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print("Bot ready")


@bot.command(name="test")
async def test(ctx):
    await ctx.send("The test command was successful!")








@bot.command(name="random")
async def rand(ctx):
    voicelines_folder = pathlib.Path('voicelines')

    files_in_folder = os.listdir(voicelines_folder)
    directory_only = [
        d for d in os.listdir(voicelines_folder)
        if os.path.isdir(os.path.join(voicelines_folder, d))
    ]
    random_directory = random.choice(directory_only)
    random_directory_path = voicelines_folder / random_directory

    files_in_folder = os.listdir(random_directory_path)
    files_only = [
        f for f in files_in_folder
        if os.path.isfile(os.path.join(random_directory_path, f))
    ]
    random_file = random.choice(files_only)
    random_voiceline_path = random_directory_path / random_file

    # await ctx.send(random_voiceline_path)

    voice_channel = ctx.author.voice.channel
    discord.channel = None
    if (voice_channel != None):
        discord.channel = voice_channel.name
        vc = await voice_channel.connect()
        source = await discord.FFmpegOpusAudio.from_probe(
            source=random_voiceline_path.as_posix())
        vc.play(source)
        while vc.is_playing():
            await sleep(.1)
        await vc.disconnect()
    else:
        await ctx.send(str(ctx.author.name) + " is not in a channel.")
    await ctx.message.delete()


bot.run(TOKEN)
