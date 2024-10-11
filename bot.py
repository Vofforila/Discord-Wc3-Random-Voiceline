import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
import random
import os

# Load environment variables from the .env file
load_dotenv()

# Get the bot token from the .env file
TOKEN = os.getenv('DISCORD_TOKEN')

# Define intents to specify what the bot is allowed to do
intents = discord.Intents.default()
intents.message_content = True  # Make sure the bot can read messages

# Initialize the bot with the specified intents
bot = commands.Bot(command_prefix='/', intents=intents)

# Folder where the voice lines are stored
VOICE_LINES_FOLDER = './voicelines'

# Event handler for when the bot is ready
@bot.event
async def on_ready():
    print(f'Bot connected as {bot.user}')

# Helper function to join a voice channel
async def join_voice_channel(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        return await channel.connect()
    else:
        await ctx.send("You need to be in a voice channel to play the sound.")
        return None

# Command to play a random voice line
@bot.command(name='random')
async def random_voice_line(ctx):
    voice_client = await join_voice_channel(ctx)
    if not voice_client:
        return

    # List all audio files in the voicelines folder, including subdirectories
    voice_files = []
    for root, dirs, files in os.walk(VOICE_LINES_FOLDER):
        for file in files:
            if file.endswith('.wav'):  # Only consider .wav files
                voice_files.append(os.path.join(root, file))

    if not voice_files:
        await ctx.send("No voice lines available!")
        await voice_client.disconnect()
        return

    # Choose a random file from the collected voice lines
    random_file = random.choice(voice_files)

    # Play the random audio file
    voice_client.play(discord.FFmpegPCMAudio(random_file))

    # Send a message with the name of the voice line
    await ctx.send(f"Playing: {os.path.basename(random_file)}")

    # Wait until the audio is done playing
    while voice_client.is_playing():
        await discord.utils.sleep_until(voice_client)

    # Disconnect after playing
    await voice_client.disconnect()

# Run the bot
bot.run(TOKEN)
