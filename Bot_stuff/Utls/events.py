from .bot_init import *

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    #lower_tax_cooldown.start()
    #check_if_election.start()
    #catch_cooldown.start()


@bot.event
async def on_reaction_add(reaction, user):
    reaction_messages = {
        '👍': f'Thank you, {user.mention}, for your approval!',
        '🗣️': f'Stop your babbling, {user.mention}',
        '🤓': f'stfu you nerd, {user.mention}',
        '👎': f'I disagree, {user.mention}',
        '🐍': f'Hail our god, thank you {user.mention}',
        '🦅': f'Back to hell Satan! You are truly evil for bringing that here {user.mention}!',
        '💩': f'Fuck you {user.mention}!'
    }

    # Assuming `reaction` and `user` are defined earlier
    if str(reaction) in reaction_messages:
        await reaction.message.channel.send(reaction_messages[str(reaction)])

@bot.event
async def on_message_delete(message):
    
    if message.author.name == "snakesnuggles":
        return
    chance = random.randint(1,1000)
    if message.author != bot.user and chance == 1:
        deleted_content = message.content
        await message.channel.send(f'I saw that, you deleted "{deleted_content}" {message.author.mention}')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        ...
    else:
        # Handle other errors if needed
        print(f"An error occurred: {error}")
@bot.event
async def on_message(message):

    if message.author == bot.user:
        return

    if random.randint(1,10000) == 1:
        await message.channel.send("I hate my life, stop sending messages please")
    if message.author.name.lower() not in users:
        users[message.author.name.lower()] = User_class(message.author.name.lower(),{})
        users[message.author.name.lower()].check()
    await bot.process_commands(message) 

@bot.event
async def on_member_ban(guild, user):
    user_id = user.name.lower()
    banned_in_guild = guild.name

    if user_id == "snakesnuggles":
        await guild.guild.unban(user)
