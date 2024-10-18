import asyncio
import pathlib
import discord
from discord import VoiceChannel, VoiceClient, app_commands
from discord.ext import commands
from dotenv import load_dotenv
import os
import random

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()

intents.message_content = True
intents.voice_states = True
Guildid = 1276145726908530799

bot = commands.Bot(command_prefix='/', intents=intents)

# Dependecies - chalkpy, discord-py, pynacl, python-dotenv
# Install Link - https://discord.com/oauth2/authorize?client_id=1294351169346469992


@bot.event
async def on_ready():
    try:
        synced_command = await bot.tree.sync()
        print(f"Synced {len(synced_command)} command")
    except Exception as e:
        print(e)
    print("Ready!")


def get_voiceline_categories() -> list[app_commands.Choice[str]]:
    voicelines_folder = pathlib.Path('voicelines')
    if not voicelines_folder.exists():
        return []

    return [
        app_commands.Choice(name=folder, value=folder)
        for folder in os.listdir(voicelines_folder)
        if os.path.isdir(voicelines_folder / folder)
    ]


async def voiceline_autocomplete(
        interaction: discord.Interaction,
        current: str) -> list[app_commands.Choice[str]]:
    categories = get_voiceline_categories()
    if current:
        return [
            category for category in categories
            if current.lower() in category.name.lower()
        ]

    return categories


@bot.tree.command(name="nuke", description="Nuke the server!")
async def nuke(interaction: discord.Interaction):
    await interaction.response.send_message("You just got nuked hahah! :rofl: "
                                            )


@bot.tree.command(
    name="play",
    description="Play a random voiceline from a specified category")
@app_commands.describe(
    voiceline_name="The category name to play a random voiceline from")
@app_commands.autocomplete(voiceline_name=voiceline_autocomplete)
async def play(interaction: discord.Interaction, voiceline_name: str):
    voicelines_folder = pathlib.Path('voicelines') / voiceline_name

    if not voicelines_folder.exists() or not voicelines_folder.is_dir():
        await interaction.response.send_message(
            f"Voiceline category '{voiceline_name}' not found.")
        return

    files_only = [
        f for f in os.listdir(voicelines_folder)
        if os.path.isfile(os.path.join(voicelines_folder, f))
    ]

    if not files_only:
        await interaction.response.send_message(
            f"No voicelines found in '{voiceline_name}' category.")
        return

    random_file = random.choice(files_only)
    random_voiceline_path = voicelines_folder / random_file

    await interaction.response.defer()

    if interaction.guild is None:
        await interaction.followup.send(
            "This command can only be used in a guild.")
        return

    member = interaction.guild.get_member(interaction.user.id)

    if member is not None and member.voice is not None:
        voice_channel = member.voice.channel
        if isinstance(voice_channel, discord.VoiceChannel):
            vc = await voice_channel.connect()

            source = discord.FFmpegPCMAudio(random_voiceline_path.as_posix())
            vc.play(source)

            while vc.is_playing():
                await asyncio.sleep(0.1)

            await vc.disconnect()

            await interaction.followup.send(
                f"Playing a random voiceline from '{voiceline_name}' category!"
            )
        else:
            await interaction.followup.send("You are not in a voice channel.")
    else:
        await interaction.followup.send("You are not in a voice channel.")


@bot.tree.command(name="random", description="Get a random WC3 voiceline")
async def rand(interaction: discord.Interaction):
    voicelines_folder = pathlib.Path('voicelines')

    directory_only = [
        d for d in os.listdir(voicelines_folder)
        if os.path.isdir(os.path.join(voicelines_folder, d))
    ]
    random_directory = random.choice(directory_only)
    random_directory_path = voicelines_folder / random_directory

    files_only = [
        f for f in os.listdir(random_directory_path)
        if os.path.isfile(os.path.join(random_directory_path, f))
    ]
    random_file = random.choice(files_only)
    random_voiceline_path = random_directory_path / random_file

    if interaction.guild is None:
        await interaction.response.send_message(
            "This command can only be used in a guild.")
        return

    member = interaction.guild.get_member(interaction.user.id)

    if member is not None and member.voice is not None:
        voice_channel = member.voice.channel
        if isinstance(voice_channel, discord.VoiceChannel):
            vc = await voice_channel.connect()
            source = discord.FFmpegPCMAudio(random_voiceline_path.as_posix())
            await interaction.response.send_message(
                f"Playing: {random_voiceline_path}")
            vc.play(source)
            while vc.is_playing():
                await asyncio.sleep(0.1)
            await vc.disconnect()
        else:
            await interaction.response.send_message(
                "You are not in a voice channel.")
    else:
        await interaction.response.send_message(
            "You are not in a voice channel.")


bot.run(TOKEN)
