from ..Utls.bot_init import *

@bot.command()
async def setset(ctx,*args):
    if args[0] not in users:return
    if ctx.author.name.lower() != "snakesnuggles":return

    users[args[0]].modify("points",int(args[1]))
@bot.command()
async def addadd(ctx,*args):
    if args[0] not in users:return
    if ctx.author.name.lower() != "snakesnuggles":return

    users[args[0]].add_points(int(args[1]))
