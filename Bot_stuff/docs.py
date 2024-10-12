from .Utls.bot_init import *

@bot.command()
async def command(ctx):
    await ctx.send(
'''
I will not tell you what these do:
```
!choose item,item,ect
!bank
!should
!coin (heads or tails) (How much you want to bet)
!rps
!words
!use (item) (args)
!void (how much)
!inventory
!gift (user) (How much)
!lir
!shop (what you want to but, write nothing if you want to see the list)
!goodnight (7pm-11pm)
!goodmorning (1am-10am)
!goodnoon (12pm-1pm)
!ballsack
!yourthoughts
!command (I don't know why you'd need to know this if you just did it)
!ourlist (The title of the list),(what you add to the list)
```
''')

@bot.command()
async def docs(ctx):
    await ctx.send(
'''
Docs
```
!choose item,item,ect
    chooses from the list you provide
!bank
    shows how much the bank has
!should
    says yes or no to the question you ask
!coin (heads or tails) (How much you want to bet)
    gives you points if you win lose points if you lose
!rps
    play rps, get a win streak
!words
    just use it
!use (item),(other args)
    uses the item
!inventory
    gives a list of items you have
!void (how much)
    gets rid of the points you specify
!gift (user) (How much)
    gifts the user the amount you specifyed
!shop (what you want to but, write nothing if you want to see the list)
    buy stuff
!goodnight (7pm-11pm)
    say that to the bot
!lir
    plays the let it ride game
!hangman
    plays the hangman game 
!goodmorning (1am-10am)
    say that to the bot
!goodnoon (12pm-1pm)
    say that to the bot
!ballsack
    no
!yourthoughts
    says "I think it's good" or "I think it's bad" to your question
!command
    shows the list of commands
!ourlist (The title of the list),(what you add to the list)
    allows you to make a list of items saved for later
```
''')
