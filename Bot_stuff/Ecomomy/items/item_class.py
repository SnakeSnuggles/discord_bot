from ...Utls.bot_init import *

class Item:
    def __init__(self,
                 user:str,
                 used_on:str = None,
                 has_inlimited_uses:bool = False,
                 has_more_functions=False,
                 rarity:float=0
                 ):
        self.user = user
        self.used_on = used_on
        self.has_inlimited_uses = has_inlimited_uses
        self.has_more_functions = has_more_functions
        self.rarity = rarity
    async def item_function(self,ctx):
        await ctx.send("It did nothing")

@tasks.loop(seconds=1)
async def catch_cooldown():
    user_data = open_file("points.json")
    for user in user_data:
        if "catch cooldown" not in user_data[user]:
            user_data[user]["catch cooldown"] = 0
        
        if user_data[user]["catch cooldown"] > 0:
            user_data[user]["catch cooldown"] -= 1
    with open("points.json","w") as json_file:
        json.dump(user_data,json_file,indent=4)

