import discord
from discord.ext import commands, tasks
from discord import app_commands
import random
from datetime import datetime, timedelta
import json
import time
from .global_paths import *
import os
intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.message_content = True
intents.guilds = True
intents.members = True

class bobwillendthis(Exception):
    pass
# Create a bot instance with a prefix and the intents
bot = commands.Bot(command_prefix='!', intents=intents)
bot_token_file = "C:\\Users\\daves\\bot_token.txt" # TODO make this relitive for some reason
with open(bot_token_file, 'r') as file:
        # Read the first line
        bot_Token = file.readline()

script_dir = os.path.dirname(os.path.abspath(__file__))




def run_in_script_directory(func):
    def wrapper(*args, **kwargs):
        original_directory = os.getcwd()
        os.chdir(script_dir)
        try:
            result = func(*args, **kwargs)
        finally:
            os.chdir(original_directory)
        return result
    return wrapper

@run_in_script_directory
def open_file(file_path: str):
    with open(file_path) as file:
        data = json.load(file)
    return data

@run_in_script_directory
def save_file(file_path: str, data: dict):
    with open(file_path, "w") as json_file:
        json.dump(data, json_file, indent=4)


from .user_class import User_class
all_of_points = open_file(points_P)
users:dict[str, User_class] = {}
for name, data in all_of_points.items():  
    users[name] = User_class(name, data)
    users[name].check()