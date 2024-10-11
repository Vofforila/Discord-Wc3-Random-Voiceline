import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import random

# Load environment variables from .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Set up intents and create bot instance
intents = discord.Intents.default()
intents.message_content = True  # Required for message content
intents.voice_states = True  # Required for voice state updates
bot = commands.Bot(command_prefix='/', intents=intents)


@bot.event
async def on_ready():
    print("Bot ready")


@bot.command()
async  def hello(ctx):
    await ctx.send("Hello there!")


# Random voiceline command
@bot.command(name="random")
async def random_voiceline(ctx):
    # Specify the path to the voicelines folder
    voiceline_folder = "./voicelines"  # Change this path as necessary

    # List all files in the folder
    try:
        voicelines = os.listdir(voiceline_folder)  # Get list of files in the directory
        voicelines = [f for f in voicelines if f.endswith('.wav')]  # Filter only .wav files

        if voicelines:
            selected_voiceline = random.choice(voicelines)  # Select a random voiceline

            # Connect to the voice channel
            if ctx.author.voice:
                channel = ctx.author.voice.channel
                voice_client = await channel.connect()  # Connect to the voice channel

                # Play the selected voiceline
                source = discord.FFmpegPCMAudio(os.path.join(voiceline_folder, selected_voiceline))
                voice_client.play(source)

                await ctx.send(f"Random voiceline: {selected_voiceline}")

                # Wait until the audio is finished playing
                while voice_client.is_playing():
                    await discord.utils.sleep(1)

                # Disconnect from the voice channel
                await voice_client.disconnect()
            else:
                await ctx.send("You need to be in a voice channel to use this command.")
        else:
            await ctx.send("No voicelines found.")
    except Exception as e:
        await ctx.send(f"Error occurred: {str(e)}")



bot.run(TOKEN)