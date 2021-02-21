import os
from twitchio.ext import commands
import random
#pipenv run python bot.py

bot = commands.Bot(
    irc_token=os.environ['TMI_TOKEN'],
    client_id=os.environ['CLIENT_ID'],
    nick='hot_bricktato',
    prefix=os.environ['BOT_PREFIX'],
    initial_channels=['92soo'],
)

collecting_players = False
game_ongoing = False
queueing = False
players = set()
has_potato = None
potato_hp = 0

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
    await ctx.send("Use !open command to start a game of hot bricktato!")

@bot.command(name='open')
async def open_command(ctx):
    global game_ongoing
    global queueing
    if game_ongoing and queueing is False:
        await ctx.channel.send("The hot bricktato is already being passed. Please try again later.")
    else:
        queueing = True
        await ctx.channel.send(f"@{ctx.author.name} has started a hot bricktato game. Use !open enter the lobby and !close when all players are ready")

@bot.command(name='join')
async def join_command(ctx):
    global game_ongoing
    global queueing
    if game_ongoing is False and queueing is True:
        add_player(ctx.author.name)
        await ctx.channel.send(f"@{ctx.author.name} has joined the hot bricktato game")
    elif game_ongoing is True:
        await ctx.channel.send("The hot bricktato is already being passed. Please try joining again later.")
    else:
        await ctx.send("Use !open command to start a game of hot bricktato! Join after that.")


@bot.command(name='leave')
async def leave_command(ctx):
    global game_ongoing
    global queueing
    if queueing is False:
        ctx.send("No bricktato game currently going on. Use !open command to start a game of hot bricktato.")
    elif game_ongoing:
        await ctx.channel.send("The hot bricktato is already being passed. Please try again later.")
    else:
        remove_player(ctx.author.name)
        await ctx.channel.send(f"@{ctx.author.name} does not want to play anymore")

@bot.command(name='close')
async def close_command(ctx):
    global game_ongoing
    global queueing
    global has_potato
    if game_ongoing:
        await ctx.channel.send("The hot bricktato is already being passed. Please try again later.")
    elif queueing is False:
        await ctx.channel.send("No bricktato game currently going on. Use !open command to start a game of hot bricktato.")
    else:
        queueing = False
        game_ongoing = True
        randomize_health()
        await ctx.channel.send("The hot bricktato is on fire!")
        has_potato = randomize_player()
        await ctx.channel.send(f"@{has_potato} has the hot bricktato")


@bot.command(name='pass')
async def pass_command(ctx):
    global game_ongoing
    global queueing
    global has_potato
    global players
    if game_ongoing and ctx.author is has_potato:
        randomize_pass_loss()
        if potato_hp < 0:
            await ctx.channel.send(f"@{ctx.author.name} can't take the heat. They're out of the game!")
            remove_player(ctx.author)
        else:
            await ctx.channel.send(f"@{ctx.author.name} passed the bricktato.")
            has_potato = randomize_player()
            if len(players) == 1:
                await ctx.channel.send(f"@{has_potato} won the game.")
                game_ongoing = False
            else:
                await ctx.channel.send(f"@{has_potato} has the hot bricktato")

def randomize_health():
    global potato_hp
    potato_hp = random.randint(1, 100)

def randomize_pass_loss():
    global potato_hp
    potato_hp -= random.randint(0, potato_hp-1)

def add_player(username):
    global players
    players.add(username)

def remove_player(username):
    global players
    if username in players:
        players.remove(username)

def randomize_player():
    global players
    return random.choice(tuple(players))

if __name__ == "__main__":
    bot.run()

