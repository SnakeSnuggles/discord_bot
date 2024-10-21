from ...Utls.bot_init import *
from .items import *

@bot.command()
async def inventory(ctx):
    inv = users[ctx.author.name.lower()].get("inventory")
    inv = "\n".join(inv)
    await ctx.send("Inventory:\n```" + inv + "```")

@bot.command()
async def use(ctx,*args):
    args = " ".join(args)
    args = args.split(",")

    user = ctx.author.name.lower()

    user_object = users[user]

    inv = user_object.get("inventory")
    def used_on_real():
        try:
            used_on = args[1]
            return used_on
        except IndexError:
            pass
    used_on = used_on_real()
    
    if args[0] not in items:
        await ctx.send("That item does not exist")
        return
    if args[0] not in inv:
        await ctx.send("You do not have that item")
        return
    if items[args[0]]["used_on"] != None:
        if args[1] not in users:
            await ctx.send("That user does not exist")
            return

    if items[args[0]]["unlimited_use"] == False:
        user_object.remove_inventory(args[0])
    if items[args[0]]["has_more_functions"] == True:
        await items[args[0]]["item_func"](ctx=ctx,function=args[2])
    else:
        await items[args[0]]["item_func"](ctx=ctx)

@bot.command()
async def shop(ctx, *args):
    data = open_file(points_P)

    data2 = open_file(shop_P)
    
    points = data[ctx.author.name.lower()]["points"]
    args = ' '.join(args)

    if args in data2:
        if data[ctx.author.name.lower()]["points"] >= data2[args]:
            data[ctx.author.name.lower()]["points"] -= data2[args]
            try:
                thing = await send_to_bank(data2[args],ctx) 
                data = thing if thing != None else data
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
    save_file(points_P,data)

@bot.command()
async def pokemon(ctx,*args):
    args = " ".join(args)
    args = args.split(",")
    data = open_file(points_P)
    # custom_ctx = copy.copy(ctx)

    if args[0] not in data[ctx.author.name.lower()]["caught"]:
        ctx.send("You have not caught that person")
        return
    # custom_ctx.author.name = str(args[0])

    args[2] = args[2].split(" ")
    print(args[2])
    data[ctx.author.name.lower()]["caught"].remove(args[0])
    # await gift(custom_ctx,args[2][0],args[2][1])
    save_file(points_P,data)
