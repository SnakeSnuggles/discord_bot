from ...Utls.bot_init import *
from .items import *

@bot.command()
async def inventory(ctx):
    data = open_file(points_P)

    inv = data[ctx.author.name.lower()]["inventory"]
    inv = "\n".join(inv)
    await ctx.send("Inventory:\n```" + inv + "```")

@bot.command()
async def use(ctx,*args):
    args = " ".join(args)
    args = args.split(",")

    data = open_file(points_P)
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
#    fanum_taxinst = fanum_tax(user=user,used_on=used_on,has_inlimited_uses=True,has_more_functions=True,rarity=1.1)
    uselessnessinst = item(user=user)
    statistical_advantageinst = statistical_advantage(user=user,has_inlimited_uses=True,rarity=1.1)
    emoji_guninst = emoji_gun(user=user,has_inlimited_uses=True,rarity=-5)
    spooninst = spoon(user=user,used_on=used_on,has_inlimited_uses=True,rarity=-5)
    insult_guninst = insult_gun(user=user,used_on=used_on,has_inlimited_uses=True,rarity=15)
    ecomomy_restartinst = economy_reset_idol(user=user,rarity=15)
    items = {
        "pokeball":pokeballinst,
        "gun":guninst,
      #  "fanum tax wand":fanum_taxinst,
        "Uselessness":uselessnessinst,
        "Helm of Statistical Advantage":statistical_advantageinst,
        "Emoji gun":emoji_guninst,
        "Insult gun":insult_guninst,
        "spoon":spooninst,
        "Economy reset idol":ecomomy_restartinst
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
    save_file(points_P,data)
    if items[args[0]].has_more_functions == True:
        await items[args[0]].item_function(ctx=ctx,function=args[2])
    else:
        await items[args[0]].item_function(ctx=ctx)

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
