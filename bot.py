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


@bot.event
async def on_ready():
    try:
        synced_command = await bot.tree.sync()
        print(f"Synced {len(synced_command)} command")
    except Exception as e:
        print(e)
    print("Ready!")


# Function to retrieve available voiceline folder names
def get_voiceline_categories() -> list[app_commands.Choice[str]]:
    voicelines_folder = pathlib.Path('voicelines')
    if not voicelines_folder.exists():
        return []

    # Return the folder names as choices for the autocomplete
    return [
        app_commands.Choice(name=folder, value=folder)
        for folder in os.listdir(voicelines_folder)
        if os.path.isdir(voicelines_folder / folder)
    ]


# Autocomplete function for voiceline names
async def voiceline_autocomplete(
        interaction: discord.Interaction,
        current: str) -> list[app_commands.Choice[str]]:
    categories = get_voiceline_categories()

    # Filter categories based on the user's input (if they type part of the name)
    if current:
        return [
            category for category in categories
            if current.lower() in category.name.lower()
        ]

    # Show all categories if no input or no matches yet
    return categories


# Command with Autocomplete
@bot.tree.command(
    name="play",
    description="Play a random voiceline from a specified category")
@app_commands.describe(
    voiceline_name="The category name to play a random voiceline from")
@app_commands.autocomplete(
    voiceline_name=voiceline_autocomplete)  # Add autocomplete functionality
async def play(interaction: discord.Interaction, voiceline_name: str):
    voicelines_folder = pathlib.Path('voicelines') / voiceline_name

    # Check if the provided folder exists
    if not voicelines_folder.exists() or not voicelines_folder.is_dir():
        await interaction.response.send_message(
            f"Voiceline category '{voiceline_name}' not found.")
        return

    # Choose a random file from the selected folder
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

    # Defer response to give time for playing the file
    await interaction.response.defer()

    if interaction.guild is None:  # Check if the interaction is not in a guild
        await interaction.followup.send(
            "This command can only be used in a guild.")
        return

    member = interaction.guild.get_member(interaction.user.id)

    if member is not None and member.voice is not None:  # Check if the member is in a voice channel
        voice_channel = member.voice.channel
        if isinstance(voice_channel, discord.VoiceChannel
                      ):  # Check if voice_channel is a VoiceChannel
            vc = await voice_channel.connect()

            # Play the random audio file
            source = discord.FFmpegPCMAudio(random_voiceline_path.as_posix())
            vc.play(source)

            # Wait until the audio is finished
            while vc.is_playing():
                await asyncio.sleep(0.1)

            # Disconnect after playback is done
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

    # Choose a random directory and file
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

    if interaction.guild is None:  # Check if the interaction is not in a guild
        await interaction.response.send_message(
            "This command can only be used in a guild.")
        return

    member = interaction.guild.get_member(interaction.user.id)

    if member is not None and member.voice is not None:  # Check if the member is in a voice channel
        voice_channel = member.voice.channel
        if isinstance(voice_channel, discord.VoiceChannel
                      ):  # Check if voice_channel is a VoiceChannel
            vc = await voice_channel.connect()
            # Play the audio file
            source = discord.FFmpegPCMAudio(random_voiceline_path.as_posix())
            await interaction.response.send_message(
                f"Playing: {random_voiceline_path}")
            vc.play(source)

            # Wait until the audio is finished
            while vc.is_playing():
                await asyncio.sleep(0.1)

            # Disconnect after playback is done
            await vc.disconnect()

        else:
            await interaction.response.send_message(
                "You are not in a voice channel.")
    else:
        await interaction.response.send_message(
            "You are not in a voice channel.")


# @bot.tree.command(name="hello", description="This is a hello command")
# async def hello(interaction: discord.Interaction):
#     await interaction.response.send_message(
#         f"Hey {interaction.user.mention}! This is a slash command")

# @bot.tree.command(name="random", description="Get a random Wc3 Voiceline")
# async def rand(interaction: discord.Interaction):
#     voicelines_folder = pathlib.Path('voicelines')

#     files_in_folder = os.listdir(voicelines_folder)
#     directory_only = [
#         d for d in os.listdir(voicelines_folder)
#         if os.path.isdir(os.path.join(voicelines_folder, d))
#     ]
#     random_directory = random.choice(directory_only)
#     random_directory_path = voicelines_folder / random_directory

#     files_in_folder = os.listdir(random_directory_path)
#     files_only = [
#         f for f in files_in_folder
#         if os.path.isfile(os.path.join(random_directory_path, f))
#     ]
#     random_file = random.choice(files_only)
#     random_voiceline_path = random_directory_path / random_file

#     # await ctx.send(random_voiceline_path)

#     voice_channel = VoiceClient.channel
#     if (voice_channel != None):
#         source = await discord.FFmpegOpusAudio.from_probe(
#             source=random_voiceline_path.as_posix())

#         vc = await voice_channel.connect()
#         vc.play(source)
#         while vc.is_playing():
#             await asyncio.sleep(.1)
#         await vc.disconnect()
#     else:
#         await interaction.response.send_message(
#             str(interaction.user.name) + " is not in a channel.")

bot.run(TOKEN)
