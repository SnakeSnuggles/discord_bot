from Bot_stuff.Utls.bot_init import *

@bot.command()
async def leaderboard(ctx):
    data = open_file(points_P)
    string = []
    for user in data:
        if "points" not in data[user]:
            data[user]["points"] = 0  
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
            "cheeseburgerillion",
            "sodaillion",
            "friesillion"
            "uncentillion",
            "bicentillion",
            "tricentillion",
            "triceratops"
                    ]
        newnumbers = []
        for number in numbers:
            newnumbers.append(number)
            newnumbers.append(number)
            newnumbers.append(number)
        number = dict(zip(numbers_amounts,newnumbers))

        pointsstr = str(points)
        numberlength = len(pointsstr)

        cutoff_point = numberlength % 4
        
        pointsthing = pointsstr[:cutoff_point]

        if numberlength >= 7 and numberlength < (len(numbers) * 3):
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
async def void(ctx,*args):
    user_object = users[ctx.author.name.lower()]

    if int(args[0]) > data[ctx.author.name.lower()]["points"]:
        await ctx.send("You do not have that much to void")
        return
    if int(args[0]) < 0:
        await ctx.send("You can't void negative points")
        return
    user_object.add_points(-int(args[0]))
    await ctx.send(f"You voided {args[0]} you now have {user_object.get("points")}")
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
async def ourlist(ctx,*args):
    data = open_file(lists_P)
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
    save_file(lists_P,data)

@bot.command()
async def ballsack(ctx):
    await ctx.send(f"What did you say to me? {ctx.author.mention}")


@bot.command()
async def yourthoughts(ctx):
    
    if random.randint(0,1) == 0: await ctx.send("I think it's good")
    else:
        if random.randint(0,50) == 0:
            await ctx.send("I think it's horrid, the worst thing to ever happen, the only thing I'd get rid of.")
        else:
            await ctx.send("I think it's bad")

@bot.command()
async def clear(ctx):
    await ctx.send('''
‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n‎\n                       
''')

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
async def bank(ctx):
    data = open_file(bank_P)
    await ctx.send(f"Bank's points:\n```{data["points"]}```")
    return
