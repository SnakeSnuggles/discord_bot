from ..Utls.bot_init import *

@bot.command()
async def rob(ctx, *args):
    data = open_file(points_P)

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
            save_file(points_P,data)
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
        thing = await send_to_bank(int(args[1]),ctx) 
        data = thing if thing != None else data
        await ctx.send(f"You failed now the bank gets {args[1]} point(s) from you. LOL")
        save_file(points_P,data)
@bot.command()
async def gift(ctx,*args):
    data = open_file(points_P)

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
    save_file(points_P,data)
