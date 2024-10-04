from ..Utls.bot_init import *

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
