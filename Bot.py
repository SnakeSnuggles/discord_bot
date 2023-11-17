import discord
from discord.ext import commands
import random
from datetime import datetime
import json
from discord.ext import commands

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.message_content = True
intents.guilds = True
intents.members = True

# Create a bot instance with a prefix and the intents
bot = commands.Bot(command_prefix='!', intents=intents)
file_path = "C:\\Users\\User\\bot_token.txt"
with open(file_path, 'r') as file:
        # Read the first line
        bot_Token = file.readline()

def open_file(file_path:str):
    with open(file_path) as file:
        data = json.load(file)
    return data

def debug(user,thingsthathappen:list):
    return

#checks if user is real
def is_user_real(data,author_name,anything_else = None):
    author_name_lower = author_name.lower()


    if author_name_lower not in data:
        data[author_name_lower] = {
            "points": 0,
            "win_streak_rps": 1,
            "has_used_day_thing":[False,False,False],
            "inventory": []
        }
    
    return data

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
    data = is_user_real(data,ctx.author.name)
    HorT = random.randint(0, 1)
    c = {0: "heads", 1: "tails"}
    points = data[ctx.author.name.lower()]["points"]
    if args[0] not in c.values():
        await ctx.send("You did not put heads or tails")
        return
    
    if data[ctx.author.name.lower()]["points"] <= int(args[1]):
        await ctx.send("You do not have that much")
        return
    
    if int(args[1]) < 0:
        await ctx.send("You can't bet negative points")
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
@commands.cooldown(1, 60, commands.BucketType.user)
async def rps(ctx):
    file_path = "points.json"
    data = open_file(file_path)

    message = await ctx.send("Rock, paper, or scissors? React with your choice!")

    data = is_user_real(data,ctx.author.name)

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
        getwinstreak = data[ctx.author.name.lower()]["win_streak_rps"]
        # Determine the winner based on the game rules
        if player_choice == bot_choice:
            result = "It's a tie!"
            await ctx.send("I'll give you another chance")
            await rps.callback(ctx)
            return
        elif bot_choice == game_rules[player_choice]['win']:
            try:
                result = f"{ctx.author.mention} wins! {player_choice.capitalize()} beats {bot_choice}.\n {ctx.author.mention} won {20 * getwinstreak} points"
                data[ctx.author.name.lower()]["win_streak_rps"] += 1
                data[ctx.author.name.lower()]["points"] += 20 * int(getwinstreak)
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
    ...
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
                data = is_user_real(data,user_id) 
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
            data = is_user_real(data,user_id)
            if data[user_id]["has_used_day_thing"][current] == True:return
            data[user_id]["has_used_day_thing"][current] = True
            with open(file_path, "w") as json_file:
                json.dump(data, json_file,indent=4)
        data = open_file(file_path)
        user_id = user.name.lower()
        data = is_user_real(data,user_id) 
        current_datetime = datetime.now()
        current_time_int = current_datetime.hour * 100 + current_datetime.minute
        if current_time_int <= self.max and current_time_int >= self.min:
            channel = bot.get_channel(channel_id)
            if channel:
                await channel.send(self.good_responce)
                add_points(user,20)
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
@bot.command()
async def use(ctx,*args):
    file_path = "points.json"
    file = open(file_path)
    points = json.load(file)
    
    print(f"splitting strings {args}")
    args = " ".join(args)
    print(f"splitting strings {args}")
    args = args.split(',')
    print(f"splitting strings {args}")

    if args[0] not in points[ctx.author.name.lower()]["inventory"]:
        print("does not have item in inventory")
        return
    print("has item in inventory")  
    async def gate_keep():
        if args[1] not in points:
            ctx.send("User does not exist")
            return

        if "messages_to_delete" not in points[args[1]]:
            points[args[1]].update({"messages_to_delete":0})

        points[args[0]]["messages_to_delete"] += 1

    items = {
        "Gate keep": await gate_keep(),
        "Shut up":78,
        "Shut down":200,
        "Reaction event":50,
        "Giberrsish":200,
        "Rat man":3000000,
        "Get KK6000 a girlfriend for an hour":15000,
        "Uselessness":0,
        "Give KK6000 a bathroom break and a break from Jacob for 5 min":1000
        }
    items[args[0]]

    points[ctx.author.name.lower()]["inventory"].remove(args[0])
    with open(file_path, "w") as json_file:
        json.dump(points, json_file,indent=4)

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
    await send_to_bank(int(args[0]),ctx)
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
    
    # Create a list of strings
    string = [f"{x[0]} points: {x[1]['points']:,}" for x in sorted_data]
    string = string[0:10]
    string = '\n'.join(string)
    await ctx.send("**Leaderboard:**\n" + "```" + string + "```")

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
    file = open(file_path)
    data = json.load(file)

    data = is_user_real(data,ctx.author.name)

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

    chance = int(args[1])/data[args[0]]["points"]
    choice = random.random()

    if chance <= choice:
        data[args[0]]["points"] -= int(args[1])
        data[ctx.author.name.lower()]["points"] += int(args[1])
        await ctx.send(f"You stole {args[1]} point(s) from {args[0]}")
    else:
        data[args[0]]["points"] += int(args[1])
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
async def list(ctx):
    await ctx.send(
'''
I will not tell you what these do:
```
!choose item,item,ect
!should
!coin (heads or tails) (How much you want to bet)
!rps
!words
!void (how much)
!gift (user) (How much)
!shop (what you want to but, write nothing if you want to see the list)
!goodnight (7pm-11pm)
!goodmorning (1am-10am)
!goodnoon (12pm-1pm)
!ballsack
!yourthoughts
!list (I don't know why you'd need to know this if you just did it)
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
!should
    says yes or no to the question you ask
!coin (heads or tails) (How much you want to bet)
    gives you points if you win lose points if you lose
!rps
    play rps, get a win streak
!words
    just use it
!void (how much)
    gets rid of the points you specify
!gift (user) (How much)
    gifts the user the amount you specifyed
!shop (what you want to but, write nothing if you want to see the list)
    buy stuff
!goodnight (7pm-11pm)
    say that to the bot
!goodmorning (1am-10am)
    say that to the bot
!goodnoon (12pm-1pm)
    say that to the bot
!ballsack
    no
!yourthoughts
    says "I think it's good" or "I think it's bad" to your question
!list
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
