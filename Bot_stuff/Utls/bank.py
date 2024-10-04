from .bot_init import *

async def send_to_bank(howmuch:int,ctx):
    bank = open_file(bank_P)
    # user_data = open_file("points.json")

    # president = None
    # for user in user_data:
    #     if "titles" not in user_data[user]: user_data[user]["titles"] = []
    #     if "president" in user_data[user]["titles"]: 
    #         president = user
    #         break
    # if president != None:
    #     if "points" not in user_data[president]: 
    #         user_data[president]["points"] = 0
    #     user_data[president]["points"] += howmuch

    #     with open("points.json", "w") as json_file:
    #         json.dump(user_data, json_file,indent=4)
    #     return user_data

    if (bank["points"]+howmuch) < 0:
        await ctx.send("Bank is out of money, sorry")
        raise bobwillendthis
    bank["points"] += howmuch

    save_file(bank_P,bank)
    return None

