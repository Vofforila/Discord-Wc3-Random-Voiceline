import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Set up intents and create bot instance
intents = discord.Intents.default()
intents.message_content = True  # Required for message content
bot = commands.Bot(command_prefix='/', intents=intents)


@bot.event
async def on_ready():
    print("Bot ready")


@bot.command()
async  def hello(ctx):
    await ctx.send("Hello there!")


bot.run(TOKEN)