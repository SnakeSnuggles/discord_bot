from ...Utls.bot_init import *
from ...Utls.bank import *

'''
- Rather than using a class which is unnessisary it should just be a decorator
- There should an item wrapper that adds a name value defined when wrapper is called to the dictionary and the function itself to the dictionary
- All vars declared in an item class will just be in the use function so all funtions can just use them
- There should also be some other specified values like unlimited_use or rarity if I ever get around to dealing with that
{"name":function}

@item("helm of stitistical advantage",unlimited_use=True)
def hosa():
    ...

'''

items = {}
def item(name:str, used_on=None, has_more_functions=False, unlimited_use:bool=False, rarity:float=0):

    def item_dec(func): items[name] = {"item_func":func,"used_on":used_on,"unlimited_use":unlimited_use,"has_more_functions":has_more_functions}

    return item_dec

@item("HOSA",unlimited_use=True,rarity=5000)
async def hosa(ctx):
        user_object = users[ctx.author.name.lower()]
        user_object.modify("helm_on", not user_object.get("helm_on"))
        if user_object.get("helm_on") == True:
            await ctx.send("Helm is now on")
        elif user_object.get("helm_on") == False:
            await ctx.send("Helm is now off")

@item("Emoji gun",unlimited_use=True,rarity=5)
async def emoji_gun(ctx):
        emojis = ["😀","😃","😄","😁","😆","🥹","😅","😂","🤣","🥲","☺️","😊","😇","🙂","🙃","😉","😌","😍","🥰","😘","😗","😙","😚","😋","😛","😝","😜","🤪","🤨","🧐","🤓","😎","🥸","🤩","🥳","😏","😒","😞","😔","😟","😕","☹️","🙁","😣","😖","🤬","😡","😠","😤","😤","😭","😢","🥺","😩","😫","🤯","😳","🥵","🥶","😶‍🌫️","😱","😨","😰","😥","🫠","🤫","🫡","🫢","🤭","🫣","🤔","🤗","😓","🤥","😶","🫥","😐","🫤","😑","😬","🙄","😯","😮‍💨","😪","🤤","😴","🥱","😲","😮","😦","😧","😵","😵‍💫","🤐","🥴","🤢","🤮","🤧","😷","🤒","💩","🤡","👺","👹","👿","😈","🤠","🤑","🤕","👻","👻","💀","☠️","👽","👾","🤖","🎃","😺","😸","🤲","🫶","😾","😿","🙀","😽","😼","😻","😹","👐","👐","🙌","👏","🤝","👍","👎","👊","✊","🤛","🤏","🤌","👌","🤘","🤟","🫰","✌️","🤞","🤜","🫳","🫴","👈","👉","👆","👇","☝️","✋","🤚","🖐️","🖖","👋","🤙","🫲","🫱","💪","🦾","🖕","👄","💋","💄","🦿","🦵","🦶","🫵","🙏","✍️","🫦","🦷","👅","👂","🦻","👃","👣","👁️","👀","🧒","👶","🫂","👥","👤","🗣️","🧠","🫁","🫀"]
        choice = random.randint(0,len(emojis)-1)
        if ctx.author.name.lower() == "elichat3025":
            DM = await ctx.author.create_dm()
            await DM.send(emojis[choice])
            return
        await ctx.send(emojis[choice])





class pokeball(Item):
    async def item_function(self, ctx):
        data = open_file(points_P)
        
        if "points" not in data[ctx.author.name.lower()]:
            data[ctx.author.name.lower()]["points"] = 0

        if data[self.user]["points"] <= 0:
            points = data[self.user]["points"]
            await ctx.send(f"Yea right, nice try you got {points}")
            return
        chance = data[self.user]["points"] / data[self.used_on]["points"]
        choice = random.random()
        if chance >= choice:
            await ctx.send("You did it")
            if "caught" not in data[self.user]:
                data[self.user]["caught"] = []
            data[self.user]["caught"].append(self.used_on)

        else:
            await ctx.send("They got away, oh well")

        if "catch cooldown" not in data[ctx.author.name.lower()]:
            data[ctx.author.name.lower()]["catch cooldown"] = 0

        data[ctx.author.name.lower()]["catch cooldown"] = 10_800 # 3 hours in seconds

        save_file(points_P,data)

class gun(Item):
    async def item_function(self, ctx):
        user_object = users[ctx.author.name.lower()]

        inv = user_object.get("inventory") 
        if "bullet" not in inv:
            await ctx.send("You don't have bullet.")
            return
        if "balaclava" not in inv:
            await ctx.send("You don't have balaclava.")
            return
        
        robsucceses = random.randint(1,3)

        if robsucceses != 1:
            howmuch_to_steal = random.randint(1,bank["points"])
            user_object.add_points(howmuch_to_steal)
            await send_to_bank(ctx,-howmuch_to_steal)
            await ctx.send(f"You did it, you stole {howmuch_to_steal} point(s) from the bank")
        else:
            await ctx.send("You failed")
        to_remove = ["balaclava", "bullet"]
        
        for item in to_remove:
            user_object.inventory_remove(item)


# class fanum_tax(item):
#     async def item_function(self, ctx,function:str):
#         data = open_file(points_P)
# 
#         if function == "buff":
#             await ctx.send("This is still being worked on please stand by")
#         if function == "debt":
#             if data[self.used_on]["points"] == 2500:
#                 data[self.used_on]["points"] = -2500
#                 await ctx.send(f"You set {self.used_on} 2500 debt")
#             else:
#                 if data[self.used_on]["points"] < 0 and self.used_on != "elichat3025":
#                     await ctx.send("You can't put people into debt more debt")
#                 else:
#                     data[self.used_on]["points"] -= 2500
#                     await ctx.send(f"You got rid of 2500 points from {self.used_on}'s bank")
#         else:
#             await ctx.send("That function does not exist")
#         save_file(points_P,data)

class spoon(Item):
    async def item_function(self, ctx):
            
        if self.used_on not in users:
            ctx.send("that user does not exist")
            return
        user_object = users[self.used_on]

        ten_percent = round(user_object.get("points") * 0.1)
        user_object.add_points(-ten_percent)

        await ctx.send(f"You ate 10% of {self.used_on}'s points or {ten_percent} points. The bank stole them though")
        await send_to_bank(ten_percent, ctx)

class insult_gun(Item):
    async def item_function(self, ctx):
        used_on = discord.utils.get(ctx.guild.members, name=self.used_on)
        insults = [f"{used_on.mention}, you gigglebox"]
        choice = random.randint(0,len(insults)-1)
        DM = await used_on.create_dm()

        await DM.send(insults[choice])

class economy_reset_idol(Item):
    async def item_function(self, ctx):
        
        await ctx.send("By the power of points I guess the economy will be reset")
        for user in users:
            users[user].modify("points", 0)
            await ctx.send(f"{user}'s points 0")
        await send_to_bank(999999999999999999999999999999999999999999999999999999999999999,self.ctx)
        await ctx.send("The economy is reset")
