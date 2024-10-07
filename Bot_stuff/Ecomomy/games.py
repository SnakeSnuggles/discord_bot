from ..Utls.bot_init import *
from ..Utls.bank import *

@bot.command()
async def coin(ctx,*args):
    
    user = users[ctx.author.name.lower()]
    points = user.get("points")
    HorT = random.randint(0, 1)
    c = {0: "heads", 1: "tails"}
    if args[0] not in c.values():
        await ctx.send("You did not put heads or tails")
        return

    if args[1] == "all":
        args = list(args)
        args[1] = user.get("points")

    if points < int(args[1]):
        await ctx.send("You do not have that much")
        return


    if int(args[1]) < 0:
        await ctx.send("You can't bet negative points")
        return
    if "Helm of Statistical Advantage" in user.get("inventory") and user.get("helm_on") == True:

        user.add_points(-int(args[1]))
        await ctx.send(args[0])
        user.add_points(int(args[1]) * 2)
        try:
                thing = await send_to_bank(-(int(args[1])),ctx) 
        except bobwillendthis:
                #data[ctx.author.name.lower()]["points"] += int(args[1])
                return
        await ctx.send(f"You won {int(args[1])*2}, you now have {points + int(args[1])}")
        return
    
    await ctx.send(c[HorT])
    user.add_points(-int(args[1]))
    if c[HorT] == args[0]:
        user.add_points(int(args[1]))
        try:
            thing = await send_to_bank(-(int(args[1])),ctx) 
        except bobwillendthis:
            #data[ctx.author.name.lower()]["points"] += int(args[1])
            return
        await ctx.send(f"You won {int(args[1])*2}, you now have {points + int(args[1])}")
    
    else:
        thing = await send_to_bank((int(args[1])),ctx) 

        await ctx.send(f"You lost {args[1]}, you now have {points - int(args[1])}")
@bot.command()
async def lir(ctx):
    
    user_object = users[ctx.author.name.lower()]

    if user_object.get("points") >= 2:
        if user_object.get("lir_data") < 2:
            user_object.add_points(-2)
            user_object.modify("lir_data", 2)
    else:
        await ctx.send("How are you this poor? Can't even spair 2 points LOSER LOSER LOSER LOSER")
        return

    current_number = random.randint(1,10)
    future_number = random.randint(1,10)
    while True:
        if future_number == current_number:
            future_number = random.randint(1,10)
            continue
        break
    
    message = await ctx.send(f"Prize: {user_object.get("lir_data")} \nNumber 1-10: {current_number}")
    reactions_to_add = ["⬆️","⬇️","💰"]
    for x in reactions_to_add:
        if x == "💰" and user_object.get("lir_data") == 2:
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

        if player_choice in game_rules and game_rules[player_choice](future_number, current_number):
            user_object.modify("lir_data", user_object.get("lir_data") * 2)
            await ctx.send(f"You won, the pot is now {user_object.get("lir_data")}")

        elif "Helm of Statistical Advantage" in user_object.get("inventory") and user_object.get("helm_on") == True:
            if player_choice != "cash":
                user_object.modify("lir_data", user_object.get("lir_data") * 2)
                await ctx.send(f"You won, the pot is now {user_object.get("lir_data")}")

        elif player_choice == "cash":
            await send_to_bank(-user_object.get("lir_data"),ctx)
            user_object.add_points(user_object.get("lir_data"))
            await ctx.send(f"You cashed out for {user_object.get("lir_data")}")
            user_object.modify("lir_data",0)
        else:
            await ctx.send(f"You lost")
            user_object.modify("lir_data",0)
    except TimeoutError:
        await ctx.send("You didn't make a choice in time. Game over!")  
@bot.command()
async def rps(ctx,d = None):
    
    if d != "Fgchatrtheerfg":
        message = ctx.message
    else:
        message = await ctx.send("React with your choice")
    user_object = users[ctx.author.name.lower()]

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
            'scissors' : 'rock',
            'paper' : 'scissors'
        }
        rig_lose = {value: key for key, value in rig.items()}

        getwinstreak = user_object.get("win_streak_rps")

        if ctx.author.name.lower() == "elichat3025":
            result = f"{bot.user.mention} wins! {rig[player_choice].capitalize()} beats {player_choice}."
            await ctx.send(f"{bot.user.mention} choice was: {rig[player_choice]}\n {ctx.author.mention} choice was: {player_choice}\n {result}")
            return
        if "Helm of Statistical Advantage" in user_object.get("inventory") and user_object.get("helm_on") == True:
            result = f"{ctx.author.mention} wins! {player_choice.capitalize()} beats {rig_lose[player_choice]}.\n {ctx.author.mention} won {20 * getwinstreak} points"
            user_object.add_arb("win_streak_rps",1)

            user_object.add_points(20 * getwinstreak)

            await ctx.send(f"{bot.user.mention} choice was: {bot_choice}\n {ctx.author.mention} choice was: {player_choice}\n {result}")
            return

        # Determine the winner based on the game rules
        if player_choice == bot_choice:
            result = "It's a tie!"
            await ctx.send("I'll give you another chance")

            await rps(ctx,"Fgchatrtheerfg")
            return
        elif bot_choice == game_rules[player_choice]['win']:
            try:
                result = f"{ctx.author.mention} wins! {player_choice.capitalize()} beats {bot_choice}.\n {ctx.author.mention} won {20 * getwinstreak} points"
                
                user_object.add_arb("win_streak_rps", 1)
                user_object.add_points(20 * getwinstreak)

                pokegetchance = getwinstreak/100
                if random.random() <= pokegetchance and "pokeball belt" in user_object.get("inventory"): 
                    user_object.append_inventory("pokeball")
                    await ctx.send("You got a pokeball")
                    await send_to_bank(-(20*int(getwinstreak)),ctx) 
            except bobwillendthis:
                return
        else:
            result = f"{bot.user.mention} wins! {bot_choice.capitalize()} beats {player_choice}."
            user_object.modify("win_streak_rps", 1)
        await ctx.send(f"{bot.user.mention} choice was: {bot_choice}\n {ctx.author.mention} choice was: {player_choice}\n {result}")

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
