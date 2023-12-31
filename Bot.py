import discord
from discord.ext import commands
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
bot_token_file = "C:\\Users\\User\\bot_token.txt"
with open(bot_token_file, 'r') as file:
        # Read the first line
        bot_Token = file.readline()

def open_file(file_path:str):
    with open(file_path) as file:
        data = json.load(file)
    return data

#checks if user is real


async def send_to_bank(howmuch:int,ctx):
    bank = open_file("bank.json")
    if (bank["points"]+howmuch) < 0:
        await ctx.send("Bank is out of money, sorry")
        raise bobwillendthis
    bank["points"] += howmuch

    with open("bank.json", "w") as json_file:
        json.dump(bank, json_file,indent=4)

class bobwillendthis(Exception):
    pass

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.event
async def on_reaction_add(reaction, user):
    reaction_messages = {
        '👍': f'Thank you, {user.mention}, for your approval!',
        '🗣️': f'Stop your babbling, {user.mention}',
        '🤓': f'stfu you nerd, {user.mention}',
        '👎': f'I disagree, {user.mention}',
        '🐍': f'Hail our god, thank you {user.mention}',
        '🦅': f'Back to hell Satan! You are truly evil for bringing that here {user.mention}!',
        '💩': f'Fuck you {user.mention}!'
    }

    # Assuming `reaction` and `user` are defined earlier
    if str(reaction) in reaction_messages:
        await reaction.message.channel.send(reaction_messages[str(reaction)])

@bot.event
async def on_message_delete(message):
    
    if message.author.name == "snakesnuggles":
        return
    chance = random.randint(1,1000)
    if message.author != bot.user and chance == 1:
        deleted_content = message.content
        await message.channel.send(f'I saw that, you deleted "{deleted_content}" {message.author.mention}')
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        ...
    else:
        # Handle other errors if needed
        print(f"An error occurred: {error}")
@bot.event
async def on_message(message):

    if message.author == bot.user:
        return

    if random.randint(1,10000) == 1:
        await message.channel.send("I hate my life, stop sending messages please")
    await bot.process_commands(message) 

@bot.event
async def on_member_ban(guild, user):
    user_id = user.name.lower()
    banned_in_guild = guild.name

    if user_id == "snakesnuggles":
        await guild.guild.unban(user)

#Games
@bot.command()
async def coin(ctx,*args):
    
    file_path = "points.json"
    data = open_file(file_path)
    
    if "points" not in data[ctx.author.name.lower()]:
        data[ctx.author.name.lower()]["points"] = 0
    if "inventory" not in data[ctx.author.name.lower()]:
        data[ctx.author.name.lower()]["inventory"] = []

    HorT = random.randint(0, 1)
    c = {0: "heads", 1: "tails"}
    points = data[ctx.author.name.lower()]["points"]
    if args[0] not in c.values():
        await ctx.send("You did not put heads or tails")
        return

    if args[1] == "all":
        args = list(args[1])
        args[1] = data[ctx.author.name.lower()]["points"]

    if data[ctx.author.name.lower()]["points"] < int(args[1]):
        await ctx.send("You do not have that much")
        return


    if int(args[1]) < 0:
        await ctx.send("You can't bet negative points")
        return
    if "Helm of Statistical Advantage" in data[ctx.author.name.lower()]["inventory"] and data[ctx.author.name.lower()]["helm_on"] == True:
        data[ctx.author.name.lower()]["points"] -= int(args[1])
        await ctx.send(args[0])
        data[ctx.author.name.lower()]["points"] += int(args[1]) + int(args[1])
        try:
                await send_to_bank(-(int(args[1])),ctx)
        except bobwillendthis:
                #data[ctx.author.name.lower()]["points"] += int(args[1])
                return
        await ctx.send(f"You won {int(args[1])*2}, you now have {points + int(args[1])}")
        with open(file_path, "w") as json_file:
                json.dump(data, json_file,indent=4)
        return
    
    await ctx.send(c[HorT])
    data[ctx.author.name.lower()]["points"] -= int(args[1])
    if c[HorT] == args[0]:
        data[ctx.author.name.lower()]["points"] += int(args[1]) + int(args[1])
        try:
            await send_to_bank(-(int(args[1])),ctx)
        except bobwillendthis:
            #data[ctx.author.name.lower()]["points"] += int(args[1])
            return
        await ctx.send(f"You won {int(args[1])*2}, you now have {points + int(args[1])}")
    
    else:
        await send_to_bank(int(args[1]),ctx)
        await ctx.send(f"You lost {args[1]}, you now have {points - int(args[1])}")
    with open(file_path, "w") as json_file:
        json.dump(data, json_file,indent=4)

@bot.command()
async def rps(ctx,d = None):
    file_path = "points.json"
    data = open_file(file_path)

    if d != "Fgchatrtheerfg":
        message = ctx.message
    else:
        message = await ctx.send("React with your choice")
    
    if ctx.author.name.lower() not in data:
        data[ctx.author.name.lower()] = {}

    if "points" not in data[ctx.author.name.lower()]:
        data[ctx.author.name.lower()]["points"] = 0
    if "inventory" not in data[ctx.author.name.lower()]:
        data[ctx.author.name.lower()]["inventory"] = []
    if "win_streak_rps" not in data[ctx.author.name.lower()]:
        data[ctx.author.name.lower()]["win_streak_rps"] = 0

    # Define the reactions for rock, paper, and scissors
    reactions = ['🪨', '📄', '✂️']

    # Add reactions to the message
    for reaction in reactions:
        await message.add_reaction(reaction)

    # Define a check function to filter reactions by user and emoji
    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in reactions

    try:
        reaction, user = await bot.wait_for('reaction_add', check=check, timeout=30.0)

        # Determine the user's choice based on the reaction emoji
        emoji_to_event = {"🪨":'rock',"📄":'paper','✂️':'scissors'}
        player_choice = emoji_to_event[str(reaction.emoji)]

        # Generate the bot's choice
        bot_choice = random.choice(['rock', 'paper', 'scissors'])

        # Define the game rules using a dictionary
        game_rules = {
            'rock': {'win': 'scissors', 'lose': 'paper'},
            'paper': {'win': 'rock', 'lose': 'scissors'},
            'scissors': {'win': 'paper', 'lose': 'rock'}
        }
        rig = {
            'rock' : 'paper',
            'paper' : 'scissors',
            'scissors' : 'rock'
        }
        rig_lose = {value: key for key, value in rig.items()}

        if ctx.author.name.lower() == "elichat3025":
            result = f"{bot.user.mention} wins! {rig[player_choice].capitalize()} beats {player_choice}."
            await ctx.send(f"{bot.user.mention} choice was: {rig[player_choice]}\n {ctx.author.mention} choice was: {player_choice}\n {result}")
            return
        if "Helm of Statistical Advantage" in data[ctx.author.name.lower()]["inventory"] and data[ctx.author.name.lower()]["helm_on"] == True:
            getwinstreak = data[ctx.author.name.lower()]["win_streak_rps"]
            result = f"{ctx.author.mention} wins! {player_choice.capitalize()} beats {rig_lose[player_choice]}.\n {ctx.author.mention} won {20 * getwinstreak} points"
            data[ctx.author.name.lower()]["win_streak_rps"] += 1
            data[ctx.author.name.lower()]["points"] += 20 * int(getwinstreak)
            await ctx.send(f"{bot.user.mention} choice was: {bot_choice}\n {ctx.author.mention} choice was: {player_choice}\n {result}")
            with open(file_path, "w") as json_file:
                json.dump(data, json_file,indent=4)
            return

        getwinstreak = data[ctx.author.name.lower()]["win_streak_rps"]
        # Determine the winner based on the game rules
        if player_choice == bot_choice:
            result = "It's a tie!"
            await ctx.send("I'll give you another chance")

            await rps(ctx,"Fgchatrtheerfg")
            return
        elif bot_choice == game_rules[player_choice]['win']:
            try:
                result = f"{ctx.author.mention} wins! {player_choice.capitalize()} beats {bot_choice}.\n {ctx.author.mention} won {20 * getwinstreak} points"
                data[ctx.author.name.lower()]["win_streak_rps"] += 1
                data[ctx.author.name.lower()]["points"] += 20 * int(getwinstreak)
                
                pokegetchance = getwinstreak/100
                if random.random() >= pokegetchance and "pokeball belt" in data[ctx.author.name.lower()]["inventory"]:
                    data[ctx.author.name.lower()]["inventory"].append("pokeball")
                    await ctx.send("You got a pokeball")
                await send_to_bank(-(20*int(getwinstreak)),ctx)
            except bobwillendthis:
                return
        else:
            result = f"{bot.user.mention} wins! {bot_choice.capitalize()} beats {player_choice}."
            data[ctx.author.name.lower()]["win_streak_rps"] = 1
        await ctx.send(f"{bot.user.mention} choice was: {bot_choice}\n {ctx.author.mention} choice was: {player_choice}\n {result}")

        with open(file_path, "w") as json_file:
            json.dump(data, json_file,indent=4)
    except TimeoutError:
        await ctx.send("You didn't make a choice in time. Game over!")  

@bot.command()
async def lir(ctx):
    file_path = "points.json"
    data = open_file(file_path)
    if "lir_data" not in data[ctx.author.name.lower()] or data[ctx.author.name.lower()]["lir_data"] < 2:
        if data[ctx.author.name.lower()]["points"] > 2:
            data[ctx.author.name.lower()]["lir_data"] = 2
            data[ctx.author.name.lower()]["points"] -= 2
            await send_to_bank(2,ctx)
        else:
            await ctx.send("Bro, how are you this poor? Can't even spare 2 points?")
            return
    lir_data = data[ctx.author.name.lower()]["lir_data"]

    current_number = random.randint(1,10)
    future_number = random.randint(1,10)
    while True:
        if future_number == current_number:
            future_number = random.randint(1,10)
            continue
        break
    
    message = await ctx.send(f"Prize: {lir_data} \nNumber 1-10: {current_number}")
    reactions_to_add = ["⬆️","⬇️","💰"]
    for x in reactions_to_add:
        if x == "💰" and lir_data == 2:
            continue
        await message.add_reaction(x)
    try:
        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in reactions_to_add
        reaction, user = await bot.wait_for('reaction_add', check=check, timeout=30.0)
        emoji_to_event = {"⬆️":'up',"⬇️":'down','💰':'cash'}
        player_choice = emoji_to_event[str(reaction.emoji)]

        game_rules = {
            "up": lambda future_number, current_number: future_number > current_number,
            "down": lambda future_number, current_number: future_number < current_number
        }
        lir_data = data[ctx.author.name.lower()]["lir_data"]
        if player_choice in game_rules and game_rules[player_choice](future_number, current_number):
            data[ctx.author.name.lower()]["lir_data"] *= 2
            lir_data = data[ctx.author.name.lower()]["lir_data"]
            await ctx.send(f"You won, the pot is now {lir_data}")
        elif "Helm of Statistical Advantage" in data[ctx.author.name.lower()]["inventory"] and data[ctx.author.name.lower()]["helm_on"] == True:
            data[ctx.author.name.lower()]["lir_data"] *= 2
            lir_data = data[ctx.author.name.lower()]["lir_data"]
            await ctx.send(f"You won, the pot is now {lir_data}")
        elif player_choice == "cash":
            await send_to_bank(-data[ctx.author.name.lower()]["lir_data"],ctx)
            data[ctx.author.name.lower()]["points"] += data[ctx.author.name.lower()]["lir_data"]
            await ctx.send(f"You cashed out for {lir_data}")
            data[ctx.author.name.lower()]["lir_data"] = 0 
        else:
            await ctx.send(f"You lost")
            data[ctx.author.name.lower()]["lir_data"] = 0

        with open(file_path, "w") as json_file:
            json.dump(data, json_file,indent=4)

    except TimeoutError:
        await ctx.send("You didn't make a choice in time. Game over!")  
#end

#Earning points
class responding_to_times:
    def __init__(self,min,max,good_responce,bad_responce) -> None:
        self.min = min
        self.max = max
        self.good_responce = good_responce
        self.bad_responce = bad_responce

    async def responding(self,channel_id: int,user,current):
        file_path = "points.json"
        async def add_points(user,points:int) -> None:
            try:
                file = open(file_path)
                data = json.load(file)
                user_id = user.name.lower()
                if "points" not in data[user_id]:
                    data[user_id]["points"] = 0

                if user_id in data:
                    channel = bot.get_channel(channel_id)
                    if channel:
                        data[user_id]["points"] += points
                        await send_to_bank(-points,channel)
                with open(file_path, "w") as json_file:
                    json.dump(data, json_file,indent=4)
            except bobwillendthis:
                return
        def setting_has_used_day(current,user):
            data = open_file(file_path)
            user_id = user.name.lower()
            if "has_used_day_thing" not in data[user_id]:
                data[user_id]["has_used_day_thing"] = [False,False,False]

            if data[user_id]["has_used_day_thing"][current] == True:return
            data[user_id]["has_used_day_thing"][current] = True
            with open(file_path, "w") as json_file:
                json.dump(data, json_file,indent=4)
        data = open_file(file_path)
        user_id = user.name.lower()
        if "points" not in data[user_id]:
            data[user_id]["points"] = 0

        current_datetime = datetime.now()
        current_time_int = current_datetime.hour * 100 + current_datetime.minute
        if current_time_int <= self.max and current_time_int >= self.min:
            channel = bot.get_channel(channel_id)
            if channel:
                await channel.send(self.good_responce)
                await add_points(user,20)
                setting_has_used_day(current,user)
            else:
                print(f"Channel with ID {channel_id} not found.")
        else:
            channel = bot.get_channel(channel_id)
            if channel:
                await channel.send(self.bad_responce)
            else:
                print(f"Channel with ID {channel_id} not found.")

@bot.command()
async def goodmorning(ctx):
    await responding_to_times(100,1000,f"Goodmorning {ctx.author.mention}",f"You're an idiot {ctx.author.mention}, it's not the morning").responding(ctx.channel.id,ctx.author,0)

@bot.command()
async def goodnoon(ctx):
    await responding_to_times(1200,1300,f"Good noon {ctx.author.mention}",f"You're an idiot {ctx.author.mention}, it's not the noon").responding(ctx.channel.id,ctx.author,1)

@bot.command()
async def goodnight(ctx):
    await responding_to_times(1900,2300,f"Goodnight {ctx.author.mention}",f"You're an idiot {ctx.author.mention}, it's not the night").responding(ctx.channel.id,ctx.author,2)
#end

#Removing things
class item:
    def __init__(self,
                 user:str,
                 used_on:str = None,
                 has_inlimited_uses:bool = False,
                 has_more_functions=False,
                 rarity:float=0
                 ):
        self.user = user
        self.used_on = used_on
        self.has_inlimited_uses = has_inlimited_uses
        self.has_more_functions = has_more_functions
        self.rarity = rarity
    async def item_function(self,ctx):
        await ctx.send("It did nothing")

class pokeball(item):
    async def item_function(self, ctx):
        file_path = "points.json"
        data = open_file(file_path)
        
        if "points" not in data[ctx.author.name.lower()]:
            data[ctx.author.name.lower()]["points"] = 0

        if data[self.user]["points"] <= 0:
            points = data[self.user]["points"]
            await ctx.send(f"Yea right, nice try you got {points}")
            return
        chance = data[self.user]["points"] / data[self.used_on]["points"]
        choice = random.random()
        if chance >= choice:
            await ctx.send("You did it")
            if "caught" not in data[self.user]:
                data[self.user]["caught"] = []
            data[self.user]["caught"].append(self.used_on)

        else:
            await ctx.send("They got away, oh well")
        with open(file_path, "w") as json_file:
            json.dump(data, json_file,indent=4)
class gun(item):
    async def item_function(self, ctx):
        file_path = "points.json"
        data = open_file(file_path)

        bank_file = "bank.json"
        bank = open_file(bank_file)

        inv = data[ctx.author.name.lower()]["inventory"]
        if "bullet" not in inv:
            await ctx.send("You don't have bullet.")
            return
        if "balaclava" not in inv:
            await ctx.send("You don't have balaclava.")
            return
        
        robsucceses = random.randint(1,3)

        if robsucceses != 1:
            howmuch_to_steal = random.randint(1,bank["points"])
            data[ctx.author.name.lower()]["points"] += howmuch_to_steal
            await ctx.send(f"You did it, you stole {howmuch_to_steal} point(s) from the bank")
        else:
            await ctx.send("You failed")
        if "balaclava" in inv:
            inv.remove("balaclava")
        if "bullet" in inv:
            inv.remove("bullet")
        with open(bank_file, "w") as json_file:
            json.dump(bank, json_file,indent=4)
        with open(file_path, "w") as json_file:
            json.dump(data, json_file,indent=4)

class fanum_tax(item):
    async def item_function(self, ctx,function:str):
        file_path = "points.json"
        data = open_file(file_path)

        if function == "buff":
            await ctx.send("This is still being worked on please stand by")
        if function == "debt":
            if data[self.used_on]["points"] == 2500:
                data[self.used_on]["points"] = -2500
                await ctx.send(f"You set {self.used_on} 2500 debt")
            else:
                if data[self.used_on]["points"] < 0 and self.used_on != "elichat3025":
                    await ctx.send("You can't put people into debt more debt")
                else:
                    data[self.used_on]["points"] -= 2500
                    await ctx.send(f"You got rid of 2500 points from {self.used_on}'s bank")
        else:
            await ctx.send("That function does not exist")
        with open(file_path, "w") as json_file:
            json.dump(data, json_file,indent=4)

class statistical_advantage(item):
    async def item_function(self, ctx):
        file_path = "points.json"
        data = open_file(file_path)

        if "helm_on" not in data[self.user]:
            data[self.user]["helm_on"] = False
        
        if data[self.user]["helm_on"] == True:
            data[self.user]["helm_on"] = False
            await ctx.send("Helm is now off")
        elif data[self.user]["helm_on"] == False:
            await ctx.send("Helm is now on")
            data[self.user]["helm_on"] = True
        
        with open(file_path, "w") as json_file:
            json.dump(data, json_file,indent=4)

class emoji_gun(item):
    async def item_function(self, ctx):
        emojis = ["😀","😃","😄","😁","😆","🥹","😅","😂","🤣","🥲","☺️","😊","😇","🙂","🙃","😉","😌","😍","🥰","😘","😗","😙","😚","😋","😛","😝","😜","🤪","🤨","🧐","🤓","😎","🥸","🤩","🥳","😏","😒","😞","😔","😟","😕","☹️","🙁","😣","😖","🤬","😡","😠","😤","😤","😭","😢","🥺","😩","😫","🤯","😳","🥵","🥶","😶‍🌫️","😱","😨","😰","😥","🫠","🤫","🫡","🫢","🤭","🫣","🤔","🤗","😓","🤥","😶","🫥","😐","🫤","😑","😬","🙄","😯","😮‍💨","😪","🤤","😴","🥱","😲","😮","😦","😧","😵","😵‍💫","🤐","🥴","🤢","🤮","🤧","😷","🤒","💩","🤡","👺","👹","👿","😈","🤠","🤑","🤕","👻","👻","💀","☠️","👽","👾","🤖","🎃","😺","😸","🤲","🫶","😾","😿","🙀","😽","😼","😻","😹","👐","👐","🙌","👏","🤝","👍","👎","👊","✊","🤛","🤏","🤌","👌","🤘","🤟","🫰","✌️","🤞","🤜","🫳","🫴","👈","👉","👆","👇","☝️","✋","🤚","🖐️","🖖","👋","🤙","🫲","🫱","💪","🦾","🖕","👄","💋","💄","🦿","🦵","🦶","🫵","🙏","✍️","🫦","🦷","👅","👂","🦻","👃","👣","👁️","👀","🧒","👶","🫂","👥","👤","🗣️","🧠","🫁","🫀"]
        choice = random.randint(0,len(emojis)-1)
        if ctx.author.name.lower() == "elichat3025":
            DM = await ctx.author.create_dm()
            await DM.send(emojis[choice])
            return
        await ctx.send(emojis[choice])

class insult_gun(item):
    async def item_function(self, ctx):
        used_on = discord.utils.get(ctx.guild.members, name=self.used_on)
        insults = [f"{used_on.mention}, you gigglebox"]
        choice = random.randint(0,len(insults)-1)
        DM = await used_on.create_dm()

        await DM.send(insults[choice])
@bot.command()
async def pokemon(ctx,*args):
    args = " ".join(args)
    args = args.split(",")
    file_path = "points.json"
    data = open_file(file_path)
    # custom_ctx = copy.copy(ctx)

    if args[0] not in data[ctx.author.name.lower()]["caught"]:
        ctx.send("You have not caught that person")
        return
    # custom_ctx.author.name = str(args[0])

    args[2] = args[2].split(" ")
    print(args[2])
    data[ctx.author.name.lower()]["caught"].remove(args[0])
    # await gift(custom_ctx,args[2][0],args[2][1])
 
@bot.command()
async def debug(ctx,*args):
    await ctx.send(args)

@bot.command()
async def inventory(ctx):
    data = open_file("points.json")

    inv = data[ctx.author.name.lower()]["inventory"]
    inv = "\n".join(inv)
    await ctx.send("Inventory:\n```" + inv + "```")

@bot.command()
async def use(ctx,*args):
    args = " ".join(args)
    args = args.split(",")

    data = open_file("points.json")
    user = ctx.author.name.lower()
    def used_on_real():
        try:
            used_on = args[1]
            return used_on
        except IndexError:
            pass
    used_on = used_on_real()
    pokeballinst = pokeball(user=user,used_on=used_on)
    guninst = gun(user=user,has_inlimited_uses=True,rarity=1.1)
    fanum_taxinst = fanum_tax(user=user,used_on=used_on,has_inlimited_uses=True,has_more_functions=True,rarity=1.1)
    uselessnessinst = item(user=user)
    statistical_advantageinst = statistical_advantage(user=user,has_inlimited_uses=True,rarity=1.1)
    emoji_guninst = emoji_gun(user=user,has_inlimited_uses=True,rarity=-5)
    insult_guninst = insult_gun(user=user,used_on=used_on,has_inlimited_uses=True,rarity=15)
    items = {
        "pokeball":pokeballinst,
        "gun":guninst,
        "fanum tax wand":fanum_taxinst,
        "Uselessness":uselessnessinst,
        "Helm of Statistical Advantage":statistical_advantageinst,
        "Emoji gun":emoji_guninst,
        "Insult gun":insult_guninst
    }

    if args[0] not in items:
        await ctx.send("That item does not exist")
        return
    if args[0] not in data[user]["inventory"]:
        await ctx.send("You do not have that item")
        return
    if items[args[0]].used_on != None:
        if args[1] not in data:
            await ctx.send("That user does not exist")
            return

    if items[args[0]].has_inlimited_uses == False:
        data[user]["inventory"].remove(args[0])
    with open("points.json", "w") as json_file:
        json.dump(data, json_file,indent=4)
    if items[args[0]].has_more_functions == True:
        await items[args[0]].item_function(ctx=ctx,function=args[2])
    else:
        await items[args[0]].item_function(ctx=ctx)

@bot.command()
async def mock(ctx, *args):
    args = " ".join(args)
    args = args.split()
    fixed_string = []
    for x in args:
        for i in x:
            number = random.randint(0, 1)
            if number == 1:
                fixed_string.append(i.upper())
            elif number == 0:
                fixed_string.append(i.lower())
    await ctx.send("".join(fixed_string))

@bot.command()
async def shop(ctx, *args):
    file_path = "points.json"
    file = open(file_path)
    data = json.load(file)

    file_path2 = "shop.json"
    file2 = open(file_path2)
    data2 = json.load(file2)
    
    points = data[ctx.author.name.lower()]["points"]
    args = ' '.join(args)

    if args in data2:
        if data[ctx.author.name.lower()]["points"] >= data2[args]:
            data[ctx.author.name.lower()]["points"] -= data2[args]
            try:await send_to_bank(data2[args],ctx)
            except bobwillendthis:return
            if "inventory" in data[ctx.author.name.lower()]:
                data[ctx.author.name.lower()]["inventory"].append(args)
            else:
                data[ctx.author.name.lower()]["inventory"] = args
            await ctx.send(f"You have bought {args}. You now have {points-data2[args]}")
        else:await ctx.send("You do not have enough")
    else:
        string = []
        for x in data2:
            string.append(f"{x}:{data2[x]}")
        string = '\n'.join(string)
        await ctx.send(f"**Shop: **\nPoints: {points} \n```{string}```")
    with open(file_path, "w") as json_file:
        json.dump(data, json_file,indent=4)

@bot.command()
async def void(ctx,*args):
    file_path = "points.json"
    data = open_file(file_path)

    if int(args[0]) > data[ctx.author.name.lower()]["points"]:
        await ctx.send("You do not have that much to void")
        return
    if int(args[0]) < 0:
        await ctx.send("You can't void negative points")
        return
    data[ctx.author.name.lower()]["points"]-=int(args[0])
    points = data[ctx.author.name.lower()]["points"]
    await ctx.send(f"You voided {args[0]} you now have {points}")
    with open(file_path, "w") as json_file:
        json.dump(data, json_file,indent=4)
#end

#misc
@bot.command()
async def leaderboard(ctx):
    file_path = "points.json"
    data = open_file(file_path)
    string = []
    sorted_data = sorted(data.items(), key=lambda x: x[1]["points"], reverse=True)
    
    def points_to_readable(points:int):
        numbers_amounts = []
        for x in range(6,1000):
            numbers_amounts.append(x)
        numbers = [
            "Million"
            "Billion",
            "Trillion",
            "Quadrillion",
            "Quintillion",
            "Sextillion",
            "Septillion",
            "Octillion",
            "Nonillion",
            "Decillion",
            "Undecillion",
            "Duodecillion",
            "Tredecillion",
            "Quattuordecillion",
            "Quindecillion",
            "Sexdecillion",
            "Septendecillion",
            "Octodecillion",
            "Novemdecillion",
            "Vigintillion",
            "Centillion",
            "Duckecillion",
            "Slyilliton",
            "Januarillion",
            "Februarillion",
            "Marchillion",
            "Aprillion",
            "Maillion",
            "Junillion",
            "Julillion",
            "Augustesillion",
            "Septembillion",
            "Octobillion",
            "Novembecillion",
            "Decembillion",
                    ]
        newnumbers = []
        for number in numbers:
            newnumbers.append(number)
            newnumbers.append(number)
            newnumbers.append(number)
        number = dict(zip(numbers_amounts,newnumbers))

        pointsstr = str(points)
        numberlength = len(pointsstr)

        cutoff_point = numberlength % 6
        
        pointsthing = pointsstr[:cutoff_point]

        if numberlength >= 7 and numberlength < 99:
            return f"{pointsthing} {number[numberlength]}" 
        elif numberlength > 99: 
            return "You're rich"
        else: 
            return pointsstr
    # Create a list of strings
    
    string = [f"{x[0]} points: {points_to_readable(x[1]['points'])}" for x in sorted_data]
    string = string[0:10]
    string = '\n'.join(string)
    await ctx.send("**Leaderboard:**\n" + "```" + string + "```")

@bot.command()
async def bank(ctx):
    file_path = "bank.json"
    data = open_file(file_path)
    points = "points"
    await ctx.send(f"Bank's points:\n```{data[points]}```")

@bot.command()
async def choose(ctx, *args):
    choice = []
    for arg in args:
        choice.append(arg)
    choice = " ".join(choice)
    choice = str.split(choice,',')
    rand = random.randint(0,len(choice)-1)
    await ctx.send(f"I choose: {choice[rand]}")

@bot.command()
async def should(ctx):
    dic = {1 : "yes", 0 : "no"}
    await ctx.send(dic[random.randint(0,1)])

@bot.command()
async def gift(ctx,*args):
    file_path = "points.json"
    data = open_file(file_path)

    giftgetter = args[0]
    howmuch = int(args[1])
    if howmuch < 0:
        await ctx.send("You can't send negative gifts, that's selfish")
        return

    if giftgetter in data:
        if data[ctx.author.name.lower()]["points"] >= howmuch:
            data[ctx.author.name.lower()]["points"]-=howmuch
            data[giftgetter]["points"]+=howmuch
            await ctx.send(f"You sent {giftgetter} {howmuch} points")
        else:await ctx.send("You do not have that much")
    else:await ctx.send("That person does not exist")
    with open(file_path, "w") as json_file:
        json.dump(data, json_file,indent=4)

@bot.command()
async def words(ctx):
    verb = ['fart','jump', 'act','answer', 'approve', 'arrange', 'break', 'build', 'buy', 'coach', ' colour', 'cough', 'create', 'complete', 'cry', 'dance', 'describe', 'draw', 'drink', 'eat', 'edit', 'enter', 'exit', 'imitate', 'invent', 'jump', 'laugh', 'lie', 'listen', 'paint', 'plan', 'play', 'read', 'replace', 'run', 'scream', 'see', 'shout', 'sing', 'skip', 'sleep', 'sneeze', 'solve', 'study', 'teach', 'touch', 'turn', 'walk', 'win', 'write', 'whistle', 'yank', 'zip']
    chosenverb = verb[random.randint(0,len(verb))]

    questions = [f'if you were to {chosenverb} how would you {chosenverb}.', f'If you were to choose to {chosenverb} why would you {chosenverb}?', f'If you were to {chosenverb} when would you {chosenverb}',f'How would you {chosenverb}?']
    randq = random.randint(0, len(questions)-1)
    randv = random.randint(0,len(verb)-1)
    questionchosen = questions[randq]
    print(ctx.author.name)
    await ctx.send(questionchosen)

@bot.command()
async def ourlist(ctx,*args):
    filepath = "lists.json"
    file = open(filepath)
    data = json.load(file)
    args = " ".join(args)
    args = args.split(",")

    if args[0] not in data:
        data[args[0]] = []
    out = []
    if len(args) == 1:
        if args[0]=='':
            for keys in data:out.append(keys)
            out = '\n'.join(out)
            await ctx.send(f"**Lists:** \n```{out}```")
        else:
            out = '\n'.join(data[args[0]])
            await ctx.send(f"**{args[0]}:**\n```"+out+'```')

    elif len(args) >= 2:
        try:
            for x in args[1:]:
                data[args[0]].append(x)
        except:data[args[0]] = args[1:]
    #adds everything back to the file
    with open(filepath, "w") as json_file:
        json.dump(data, json_file,indent=4)

@bot.command()
async def ballsack(ctx):
    await ctx.send(f"What did you say to me? {ctx.author.mention}")

@bot.command()
async def rob(ctx, *args):

    file_path = "points.json"
    data = open_file(file_path)

    if ctx.author.name.lower() in ['snakesnuggles',"elichat3025"]:
        await ctx.send("Robbing is disabled for you")
        return
    if 'points' not in data[ctx.author.name.lower()]:
        data[ctx.author.name.lower()]["points"] = 0

    if args[0] not in data:
        await ctx.send("You did not put a valid user")
        return
    if int(args[1]) < 0:
        await ctx.send("Why would you want to rob debt?")
        return
    if int(args[1]) > data[args[0]]["points"]:
        await ctx.send(f"{args[0]} does not have that much")
        return
    if int(args[1])>data[ctx.author.name.lower()]["points"]:
        await ctx.send(f"You can't rob more than you have")
        return

    if "Helm of Statistical Advantage" in data[ctx.author.name.lower()]["inventory"] and data[ctx.author.name.lower()]["helm_on"] == True:
            data[args[0]]["points"] -= int(args[1])
            data[ctx.author.name.lower()]["points"] += int(args[1])
            await ctx.send(f"You stole {args[1]} point(s) from {args[0]}")
            with open(file_path, "w") as json_file:
                json.dump(data, json_file,indent=4)
            return



    chance = int(args[1])/data[args[0]]["points"]
    choice = random.random()
    #good
    if chance <= choice:
        data[args[0]]["points"] -= int(args[1])
        data[ctx.author.name.lower()]["points"] += int(args[1])
        await ctx.send(f"You stole {args[1]} point(s) from {args[0]}")
    #bad
    else:
        data[ctx.author.name.lower()]["points"] -= int(args[1])
        await send_to_bank(int(args[1]),ctx)
        await ctx.send(f"You failed now the bank gets {args[1]} point(s) from you. LOL")
    with open(file_path, "w") as json_file:
        json.dump(data, json_file,indent=4)

@bot.command()
async def yourthoughts(ctx):
    
    if random.randint(0,1) == 0: await ctx.send("I think it's good")
    else:
        if random.randint(0,50) == 0:
            await ctx.send("I think it's horrid, the worst thing to ever happen, the only thing I'd get rid of.")
        else:
            await ctx.send("I think it's bad")

@bot.command()
async def command(ctx):
    await ctx.send(
'''
I will not tell you what these do:
```
!choose item,item,ect
!bank
!should
!coin (heads or tails) (How much you want to bet)
!rps
!words
!use (item) (args)
!void (how much)
!gift (user) (How much)
!lir
!shop (what you want to but, write nothing if you want to see the list)
!goodnight (7pm-11pm)
!goodmorning (1am-10am)
!goodnoon (12pm-1pm)
!ballsack
!yourthoughts
!command (I don't know why you'd need to know this if you just did it)
!ourlist (The title of the list),(what you add to the list)
```
''')

@bot.command()
async def clear(ctx):
    await ctx.send('''
‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n                       
''')

@bot.command()
async def docs(ctx):
    await ctx.send(
'''
Docs
```
!choose item,item,ect
    chooses from the list you provide
!bank
    shows how much the bank has
!should
    says yes or no to the question you ask
!coin (heads or tails) (How much you want to bet)
    gives you points if you win lose points if you lose
!rps
    play rps, get a win streak
!words
    just use it
!use (item),(other args)
    uses the item
!void (how much)
    gets rid of the points you specify
!gift (user) (How much)
    gifts the user the amount you specifyed
!shop (what you want to but, write nothing if you want to see the list)
    buy stuff
!goodnight (7pm-11pm)
    say that to the bot
!lir
    plays the let it ride game
!goodmorning (1am-10am)
    say that to the bot
!goodnoon (12pm-1pm)
    say that to the bot
!ballsack
    no
!yourthoughts
    says "I think it's good" or "I think it's bad" to your question
!command
    shows the list of commands
!ourlist (The title of the list),(what you add to the list)
    allows you to make a list of items saved for later
```
''')
#end

#admin
@bot.command()
async def setset(ctx,*args):
    file_path = "points.json"
    data = open_file(file_path)
    if args[0] not in data:return
    if ctx.author.name.lower() != "snakesnuggles":return
    data[args[0]]["points"] = int(args[1])
    with open(file_path, "w") as json_file:
        json.dump(data, json_file,indent=4)
@bot.command()
async def addadd(ctx,*args):
    file_path = "points.json"
    data = open_file(file_path)
    if args[0] not in data:return
    if ctx.author.name.lower() != "snakesnuggles":return
    data[args[0]]["points"] += int(args[1])
    with open(file_path, "w") as json_file:
        json.dump(data, json_file,indent=4)
#end

bot.run(bot_Token)