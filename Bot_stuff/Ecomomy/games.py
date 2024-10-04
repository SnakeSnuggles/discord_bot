from ..Utls.bot_init import *
from ..Utls.bank import *

@bot.command()
async def coin(ctx,*args):
    data = open_file(points_P)
    
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
        args = list(args)
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
                thing = await send_to_bank(-(int(args[1])),ctx) 
                data = thing if thing != None else data
        except bobwillendthis:
                #data[ctx.author.name.lower()]["points"] += int(args[1])
                return
        await ctx.send(f"You won {int(args[1])*2}, you now have {points + int(args[1])}")

        save_file(points_P,data)
        return
    
    await ctx.send(c[HorT])
    data[ctx.author.name.lower()]["points"] -= int(args[1])
    if c[HorT] == args[0]:
        data[ctx.author.name.lower()]["points"] += int(args[1]) + int(args[1])
        try:
            thing = await send_to_bank(-(int(args[1])),ctx) 
            data = thing if thing != None else data
        except bobwillendthis:
            #data[ctx.author.name.lower()]["points"] += int(args[1])
            return
        await ctx.send(f"You won {int(args[1])*2}, you now have {points + int(args[1])}")
    
    else:
        thing = await send_to_bank((int(args[1])),ctx) 
        data = thing if thing != None else data

        await ctx.send(f"You lost {args[1]}, you now have {points - int(args[1])}")
        save_file(points_P,data)
@bot.command()
async def lir(ctx):
    data = open_file(points_P)

    if "lir_data" not in data[ctx.author.name.lower()]:
        data[ctx.author.name.lower()]["lir_data"] = 0
    if data[ctx.author.name.lower()]["lir_data"] < 2:
        if data[ctx.author.name.lower()]["points"] >= 2:
            data[ctx.author.name.lower()]["points"] -= 2
            data[ctx.author.name.lower()]["lir_data"] = 2
        else:
            await ctx.send("How are you this poor? Can't even spair 2 points LOSER LOSER LOSER LOSER")
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
            if player_choice == "cash":
                await send_to_bank(-data[ctx.author.name.lower()]["lir_data"],ctx)
                thing = await send_to_bank(-data[ctx.author.name.lower()]["lir_data"],ctx) 
                data = thing if thing != None else data
                data[ctx.author.name.lower()]["points"] += data[ctx.author.name.lower()]["lir_data"]
                await ctx.send(f"You cashed out for {lir_data}")
                data[ctx.author.name.lower()]["lir_data"] = 0 
            else:
                data[ctx.author.name.lower()]["lir_data"] *= 2
                lir_data = data[ctx.author.name.lower()]["lir_data"]
                await ctx.send(f"You won, the pot is now {lir_data}")

        elif player_choice == "cash":
            await send_to_bank(-data[ctx.author.name.lower()]["lir_data"],ctx)
            thing = await send_to_bank(-data[ctx.author.name.lower()]["lir_data"],ctx) 
            data = thing if thing != None else data
            data[ctx.author.name.lower()]["points"] += data[ctx.author.name.lower()]["lir_data"]
            await ctx.send(f"You cashed out for {lir_data}")
            data[ctx.author.name.lower()]["lir_data"] = 0 
        else:
            await ctx.send(f"You lost")
            data[ctx.author.name.lower()]["lir_data"] = 0

        save_file(points_P,data)

    except TimeoutError:
        await ctx.send("You didn't make a choice in time. Game over!")  
@bot.command()
async def rps(ctx,d = None):
    data = open_file(points_P)

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
            save_file(points_P,data)
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
                thing = await send_to_bank(-(20*int(getwinstreak)),ctx) 
                data = thing if thing != None else data
            except bobwillendthis:
                return
        else:
            result = f"{bot.user.mention} wins! {bot_choice.capitalize()} beats {player_choice}."
            data[ctx.author.name.lower()]["win_streak_rps"] = 1
        await ctx.send(f"{bot.user.mention} choice was: {bot_choice}\n {ctx.author.mention} choice was: {player_choice}\n {result}")

        save_file(points_P,data)
    except TimeoutError:
        await ctx.send("You didn't make a choice in time. Game over!")  
@bot.command()
async def stock(ctx, mode="view", stock=None, amount=1):
    # Show all the stocks, prices, and how much you own out of the amount the bank owns
    # Should also show if the stock went up or down since the last update
    # Be able to buy and sell stocks. Buying should remove points and the stocks that the bank owns and the opposite for sell
    # After every 2 minutes update the stock market (Don't know how prob randomly)
    # Add some admin commands like crash or boom
    # Add a more in depth look for stocks
    print("")
# TODO add hang man
