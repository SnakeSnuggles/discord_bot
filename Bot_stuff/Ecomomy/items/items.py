from .item_class import *
from ...Utls.bot_init import *
from ...Utls.bank import *

class pokeball(item):
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

class gun(item):
    async def item_function(self, ctx):
        data = open_file(points_P)

        bank = open_file(bank_P)

        inv = data[ctx.author.name.lower()]["inventory"]
        if "bullet" not in inv:
            await ctx.send("You don't have bullet.")
            return
        if "balaclava" not in inv:
            await ctx.send("You don't have balaclava.")
            return
        
        robsucceses = random.randint(1,3)

        if robsucceses != 1:
            howmuch_to_steal = random.randint(1,bank["points"])
            data[ctx.author.name.lower()]["points"] += howmuch_to_steal
            await ctx.send(f"You did it, you stole {howmuch_to_steal} point(s) from the bank")
        else:
            await ctx.send("You failed")
        if "balaclava" in inv:
            inv.remove("balaclava")
        if "bullet" in inv:
            inv.remove("bullet")
        save_file(points_P,data)
        save_file(bank_P,bank)

class fanum_tax(item):
    async def item_function(self, ctx,function:str):
        data = open_file(points_P)

        if function == "buff":
            await ctx.send("This is still being worked on please stand by")
        if function == "debt":
            if data[self.used_on]["points"] == 2500:
                data[self.used_on]["points"] = -2500
                await ctx.send(f"You set {self.used_on} 2500 debt")
            else:
                if data[self.used_on]["points"] < 0 and self.used_on != "elichat3025":
                    await ctx.send("You can't put people into debt more debt")
                else:
                    data[self.used_on]["points"] -= 2500
                    await ctx.send(f"You got rid of 2500 points from {self.used_on}'s bank")
        else:
            await ctx.send("That function does not exist")
        save_file(points_P,data)
class statistical_advantage(item):
    async def item_function(self, ctx):
        data = open_file(points_P)

        if "helm_on" not in data[self.user]:
            data[self.user]["helm_on"] = False
        
        if data[self.user]["helm_on"] == True:
            data[self.user]["helm_on"] = False
            await ctx.send("Helm is now off")
        elif data[self.user]["helm_on"] == False:
            await ctx.send("Helm is now on")
            data[self.user]["helm_on"] = True
        save_file(points_P,data)
class spoon(item):
    async def item_function(self, ctx):
        user_data = open_file(points_P) 

        if self.used_on not in user_data:
            ctx.send("that user does not exist")
            return
        ten_percent = round(user_data[self.used_on]["points"] * 0.1)
        user_data[self.used_on]["points"] -= ten_percent

        await ctx.send(f"You ate 10% of {self.used_on}'s points or {ten_percent} points. The bank stole them though")
        await send_to_bank(ten_percent, ctx)

        save_file(points_P,user_data)
class emoji_gun(item):
    async def item_function(self, ctx):
        emojis = ["😀","😃","😄","😁","😆","🥹","😅","😂","🤣","🥲","☺️","😊","😇","🙂","🙃","😉","😌","😍","🥰","😘","😗","😙","😚","😋","😛","😝","😜","🤪","🤨","🧐","🤓","😎","🥸","🤩","🥳","😏","😒","😞","😔","😟","😕","☹️","🙁","😣","😖","🤬","😡","😠","😤","😤","😭","😢","🥺","😩","😫","🤯","😳","🥵","🥶","😶‍🌫️","😱","😨","😰","😥","🫠","🤫","🫡","🫢","🤭","🫣","🤔","🤗","😓","🤥","😶","🫥","😐","🫤","😑","😬","🙄","😯","😮‍💨","😪","🤤","😴","🥱","😲","😮","😦","😧","😵","😵‍💫","🤐","🥴","🤢","🤮","🤧","😷","🤒","💩","🤡","👺","👹","👿","😈","🤠","🤑","🤕","👻","👻","💀","☠️","👽","👾","🤖","🎃","😺","😸","🤲","🫶","😾","😿","🙀","😽","😼","😻","😹","👐","👐","🙌","👏","🤝","👍","👎","👊","✊","🤛","🤏","🤌","👌","🤘","🤟","🫰","✌️","🤞","🤜","🫳","🫴","👈","👉","👆","👇","☝️","✋","🤚","🖐️","🖖","👋","🤙","🫲","🫱","💪","🦾","🖕","👄","💋","💄","🦿","🦵","🦶","🫵","🙏","✍️","🫦","🦷","👅","👂","🦻","👃","👣","👁️","👀","🧒","👶","🫂","👥","👤","🗣️","🧠","🫁","🫀"]
        choice = random.randint(0,len(emojis)-1)
        if ctx.author.name.lower() == "elichat3025":
            DM = await ctx.author.create_dm()
            await DM.send(emojis[choice])
            return
        await ctx.send(emojis[choice])

class insult_gun(item):
    async def item_function(self, ctx):
        used_on = discord.utils.get(ctx.guild.members, name=self.used_on)
        insults = [f"{used_on.mention}, you gigglebox"]
        choice = random.randint(0,len(insults)-1)
        DM = await used_on.create_dm()

        await DM.send(insults[choice])

class economy_reset_idol(item):
    async def item_function(self, ctx):
        user_data = open_file(points_P)
        await ctx.send("By the power of points I guess the economy will be reset")
        for user in user_data:
            if "points" not in user_data[user]:
                user_data[user]["points"] = 0
            user_data[user]["points"] = 0
            await ctx.send(f"{user}'s points 0")
        await send_to_bank(999999999999999999999999999999999999999999999999999999999999999,self.ctx)
        await ctx.send("The economy is reset")
        save_file(points_P,user_data)
