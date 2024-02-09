import discord
from discord.ext import commands, tasks
from discord import app_commands
import random
from datetime import datetime
import json

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.message_content = True
intents.guilds = True
intents.members = True
# Create a bot instance with a prefix and the intents
bot = commands.Bot(command_prefix='!', intents=intents)
bot_token_file = "C:\\Users\\daves\\bot_token.txt"
with open(bot_token_file, 'r') as file:
        # Read the first line
        bot_Token = file.readline()


@bot.command()
async def test(ctx):
    print(bot.guilds)

bot.run(bot_Token)