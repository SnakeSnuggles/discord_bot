from ..Utls.bot_init import *


'''
How I want this to work because this is garbage

- Time calculation should check if the next election < than what it is rn and it should still run
- Then all other functions in this file should use better functions 
'''
@tasks.loop(seconds=1)
async def lower_tax_cooldown():
    bank_data = open_file(bank_P)
    if "tax_cooldown" not in bank_data:
        bank_data["tax_cooldown"] = 0
    
    if bank_data["tax_cooldown"] > 0:
        bank_data["tax_cooldown"] -= 1

    with open(bank_P, "w") as json_file:
        json.dump(bank_data, json_file,indent=4)


def time_calculation():
    '''
    "Time to next election" : 1 week from now at 0:00
    "Time to choose canadate" : from 00:00 - 23:59
    ''' 
    time_events = open_file("time_events.json")

    if "next election" not in time_events:
        time_events["next election"] = 'SHOULD BE BE CHANGED'
    if "choose canadate" not in time_events:
        time_events["choose canadate"] = 'SHOULD BE BE CHANGED'

    current_time = time.localtime()

    current_datetime = datetime(*current_time[:6])

    modified_datetime = current_datetime + timedelta(days=7)

    modified_time = modified_datetime.timetuple()

    modified_time = modified_time[0:3]

    time_events["next election"] = modified_time
    
    choose_time = current_datetime + timedelta(days=8)

    choose_time = choose_time.timetuple()

    choose_time = choose_time[0:3]
    time_events["choose canadate"] = choose_time
    
    with open("time_events.json","w") as json_file:
        json.dump(time_events, json_file,indent=4)

def tally_and_give_president():
    user_data = open_file("points.json")
    most_votes = 0
    person_with_most_votes = None

    for user_id, data in user_data.items():
        if "titles" not in data:
            data["titles"] = []
        if "votes" not in data:
            data["votes"] = 0

        if data["votes"] > most_votes:
            most_votes = data["votes"]
            person_with_most_votes = user_id
    for user in user_data:
        if "president" in user_data[user]["titles"]:
            user_data[user]["titles"].remove("president")
    if person_with_most_votes == None:
        return "no one all of you either did not vote or all of you voted for yourself's which is very selfish"
    if "titles" not in user_data[person_with_most_votes]:
        user_data[person_with_most_votes]["titles"] = []
    user_data[person_with_most_votes]["titles"].append("president")
    with open("points.json","w") as json_file:
        json.dump(user_data, json_file,indent=4)
    return person_with_most_votes

def reset_votes():
    user_data = open_file("points.json")

    for user in user_data:
        user_data[user]["has_voted"] = False
        user_data[user]["voted_for"] = None
        user_data[user]["votes"] = 0
    with open("points.json","w") as json_file:
        json.dump(user_data, json_file,indent=4)

async def send_election_start_and_end(start_or_end:str):
    signed_up_channeles = guilds_sign_up()
    time_data = open_file("time_events.json")

    if start_or_end == "start" and time_data["elec started"] == False:
        for guild in bot.guilds:
            if guild.id not in signed_up_channeles:
                continue
            channel = guild.get_channel(signed_up_channeles[guild.id])
            if channel:
                await channel.send("The election has now started use '!vote user' to vote for someone")
    elif start_or_end == "end":
        winner = tally_and_give_president()
        for guild in bot.guilds:
            if guild.id not in signed_up_channeles:
                continue
            channel = guild.get_channel(signed_up_channeles[guild.id])
            if channel:
                await channel.send(f'The election has now ended welcome our new presedent {winner}')
                time_data["elec started"] = False
                with open("time_events.json","w") as json_file:
                    json.dump(time_data, json_file,indent=4)
                time_calculation()
                reset_votes()

@tasks.loop(seconds=1,)
async def check_if_election():
    time_events = open_file("time_events.json")
    current_time = time.localtime()
    if "elec started" not in time_events:
        time_events["elec started"] = False
        with open("time_events.json","w") as json_file:
            json.dump(time_events, json_file,indent=4)
    if current_time.tm_mon == time_events["next election"][1] and current_time.tm_mday == time_events["next election"][2]:
        #send "election start" for signed up channels
        await send_election_start_and_end("start")
        time_events["elec started"] = True
        with open("time_events.json","w") as json_file:
            json.dump(time_events, json_file,indent=4)

    if current_time.tm_mon == time_events["choose canadate"][1] and current_time.tm_mday == time_events["choose canadate"][2]:
        #send "election stop" for signed up channels
        await send_election_start_and_end("end")

@bot.command()
async def vote(ctx,person_to_vote_for = None):
    file_path = "points.json"
    data = open_file(file_path)
    time_events = open_file("time_events.json")

    next_elect = time_events["next election"]
    if time_events["elec started"] == False:
        await ctx.send(f"The next election is on {next_elect[0]}/{next_elect[1]}/{next_elect[2]}")
        return
    if "has_voted" not in data[ctx.author.name.lower()]:
        data[ctx.author.name.lower()]["has_voted"] = False
    if "voted_for" not in data[ctx.author.name.lower()]:
        data[ctx.author.name.lower()]["voted_for"] = None
    if "votes" not in data[ctx.author.name.lower()]:
        data[ctx.author.name.lower()]["votes"] = 0
    if data[ctx.author.name.lower()]["has_voted"] == True:
        await ctx.send("You have already voted")
        return
    
    if person_to_vote_for not in data:
        await ctx.send("That person does not exist")
        return
    if "votes" not in data[person_to_vote_for]:
        data[person_to_vote_for]["votes"] = 0

    data[person_to_vote_for]["votes"] += 1
    data[ctx.author.name.lower()]["has_voted"] = True
    data[ctx.author.name.lower()]["voted_for"] = person_to_vote_for 

    await ctx.send(f"You succesfully voted for {person_to_vote_for} they now have {data[person_to_vote_for]["votes"]}, here's a sticker :exploding_head:")

    with open(file_path, "w") as json_file:
        json.dump(data, json_file,indent=4)

@bot.command()
async def sign_up(ctx):
    data = open_file("election_sign_up.json")

    data[ctx.guild.id] = ctx.channel.id
    await ctx.send("You are signed up for the next election and for the next and for the next ect.")
    with open("election_sign_up.json", "w") as json_file:
        json.dump(data, json_file,indent=4)

@bot.command()
async def leave_elections(ctx):
    data = open_file("election_sign_up.json")

    del data[ctx.guild.id]
    await ctx.send("You have left the next election and for the next and for the next ect.")
    with open("election_sign_up.json", "w") as json_file:
        json.dump(data, json_file,indent=4)
        
def guilds_sign_up():
    guild_channels = open_file("election_sign_up.json")
    guild_channels = {int(key): value for key, value in guild_channels.items()}
    return guild_channels
def get_president():
    user_data = open_file("points.json")

    president = None
    for user in user_data:
        if "titles" not in user_data[user]:user_data[user]["titles"]
        if "president" in user_data[user]["titles"]:
            president = user
            break
    return president

@bot.command()
async def tax(ctx,tax_amount):
    points = "points.json"
    data = open_file(points)
    
    bank_path = "bank.json"
    bank_data = open_file(bank_path)

    if "titles" not in data[ctx.author.name.lower()]:
        data[ctx.author.name.lower()]["titles"] = []
    if "tax_cooldown" not in bank_data:
        bank_data["tax_cooldown"] = 0

    if "president" not in data[ctx.author.name.lower()]["titles"]:
        await ctx.send("You are not the president")
        return
    if bank_data["tax_cooldown"] > 0:
        await ctx.send(f"Tax is on cooldown for the next {bank_data['tax_cooldown']} seconds")
        return

    tax_amount = float(tax_amount)
    if tax_amount > 30:
        await ctx.send("That is too much tax")
        return
    if tax_amount < 0:
        await ctx.send("You're too generous but as your advisor I can't let you do that")
        return
    total_tax = 0
    for user in data:
        if user == ctx.author.name.lower():
            continue
        try:
            data[user]["points"] -= round(data[user]["points"] * (tax_amount/100))
            data[ctx.author.name.lower()]["points"] += round(data[user]["points"] * (tax_amount/100))
            total_tax += round(data[user]["points"] * 0.05)
        except OverflowError:
            error_tax = 99999999999999999999999999999999999999
            data[user]["points"] -= error_tax
            data[ctx.author.name.lower()]["points"] += error_tax
            total_tax += error_tax
    
    await ctx.send(f"The president collected {total_tax} points worth of tax")
    bank_data["tax_cooldown"] = 1200

    with open(bank_path, "w") as json_file:
        json.dump(bank_data, json_file,indent=4)
    with open(points, "w") as json_file:
        json.dump(data, json_file,indent=4)
