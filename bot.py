import os
from twitchio.ext import commands
import game
from timer import Timer
#pipenv run python bot.py


bot = commands.Bot(
    irc_token=os.environ['TMI_TOKEN'],
    client_id=os.environ['CLIENT_ID'],
    nick='hot_bricktato',
    prefix=os.environ['BOT_PREFIX'],
    initial_channels=['92soo'],
)

current_game = None
boolean joinable = False

@bot.event
async def event_message(ctx):
    print(ctx.author)
    print(ctx.content)
    await bot.handle_commands(ctx)

@bot.event
async def bot_ready():
    'Called once when the bot goes online.'
    print(bot.nick + " is online!")
    ws = bot._ws  # this is only needed to send messages within event_ready
    await ws.send_privmsg(os.environ['CHANNEL'], f"/me has arrived! Is it getting hot in here?")

@bot.command(name='help')
async def help_command(ctx):
    await ctx.send("Use !play command to start a game of hot bricktato!")

@bot.command(name='start')
async def start_command(ctx):
    global current game
    if current_game is None:
        current_game = game()
        await ctx.channel.send(f"@{ctx.author.name} has started a hot bricktato game. Use !join within 20 seconds to start playing!")
        t = Timer()
        t.start()

    else:
        ctx.send("Wait until the current game is over")


@bot.command(name='join')
async def join_command(ctx):
    global current_game
    if current_game is None:
        ctx.send("No game currently going on. Use !play command to start a game of hot bricktato!")
    elif joinable:
        game.add_player(current_game, ctx.author.name)
        await ctx.channel.send(f"@{ctx.author.name} has joined the hot bricktato game")
    else:
        ctx.send("Can't join at the moment")

@bot.command(name='leave')
async def leave_command(ctx):
    global current_game
    if current_game is None:
        ctx.send("No game currently going on. Use !play command to start a game of hot bricktato!")
    else:
        game.remove_player(current_game, ctx.author.name)
        await ctx.channel.send(f"@{ctx.author.name} doesn't want to play...")

if __name__ == "__main__":
    bot.run()

