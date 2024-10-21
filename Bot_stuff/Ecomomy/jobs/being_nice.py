from Bot_stuff.Ecomomy.items.items import *
from ...Utls.bot_init import *
from ...Utls.bank import *

# TODO add a day reset 
# ^^^^^^^^^^^^^^^^^^^^
class responding_to_times:
    def __init__(self,min,max,good_responce,bad_responce) -> None:
        self.min = min
        self.max = max
        self.good_responce = good_responce
        self.bad_responce = bad_responce

    async def responding(self,channel_id: int,user,current):
        async def add_points(user,points:int) -> None:
            try:
                data = open_file(points_P)
                user_id = user.name.lower()
                if "points" not in data[user_id]:
                    data[user_id]["points"] = 0

                if user_id in data:
                    channel = bot.get_channel(channel_id)
                    if channel:
                        data[user_id]["points"] += points
                        thing = await send_to_bank(-points,channel) 
                        data = thing if thing != None else data
                save_file(points_P,data)
            except bobwillendthis:
                return
        def setting_has_used_day(current,user):
            data = open_file(points_P)
            user_id = user.name.lower()
            if "has_used_day_thing" not in data[user_id]:
                data[user_id]["has_used_day_thing"] = [False,False,False]

            if data[user_id]["has_used_day_thing"][current] == True:return
            data[user_id]["has_used_day_thing"][current] = True
            save_file(points_P,data)
        data = open_file(points_P)
        user_id = user.name.lower()
        if "points" not in data[user_id]:
            data[user_id]["points"] = 0

        current_datetime = datetime.now()
        current_time_int = current_datetime.hour * 100 + current_datetime.minute
        if current_time_int <= self.max and current_time_int >= self.min:
            channel = bot.get_channel(channel_id)
            if channel:
                await channel.send(self.good_responce)
                await add_points(user,20)
                setting_has_used_day(current,user)
            else:
                print(f"Channel with ID {channel_id} not found.")
        else:
            channel = bot.get_channel(channel_id)
            if channel:
                await channel.send(self.bad_responce)
            else:
                print(f"Channel with ID {channel_id} not found.")

@bot.command()
async def goodmorning(ctx):
    await responding_to_times(100,1000,f"Goodmorning {ctx.author.mention}",f"You're an idiot {ctx.author.mention}, it's not the morning").responding(ctx.channel.id,ctx.author,0)

@bot.command()
async def goodnoon(ctx):
    await responding_to_times(1200,1300,f"Good noon {ctx.author.mention}",f"You're an idiot {ctx.author.mention}, it's not the noon").responding(ctx.channel.id,ctx.author,1)

@bot.command()
async def goodnight(ctx):
    await responding_to_times(1900,2300,f"Goodnight {ctx.author.mention}",f"You're an idiot {ctx.author.mention}, it's not the night").responding(ctx.channel.id,ctx.author,2)


#end
