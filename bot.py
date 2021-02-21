import os
from twitchio.ext import commands
import random

# pipenv run python bot.py

bot = commands.Bot(
    irc_token=os.environ['TMI_TOKEN'],
    client_id=os.environ['CLIENT_ID'],
    nick='hot_bricktato',
    prefix=os.environ['BOT_PREFIX'],
    initial_channels=['92soo'],  # swap out for any channel name here
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
    if game_ongoing:
        await ctx.channel.send("The hot bricktato is already being passed. Please try again later.")
    elif queueing:
        await ctx.channel.send("A game has already been opened. Type !join to enter the existing lobby.")
    else:
        queueing = True
        add_player(ctx.author.name)
        await ctx.channel.send(
            f"@{ctx.author.name} has started a hot bricktato game. Use !join enter the lobby and !close when all players are ready")


@bot.command(name='join')
async def join_command(ctx):
    global game_ongoing
    global queueing
    if queueing:
        if ctx.author.name in players:
            await ctx.channel.send(f"You are already in the hot bricktato game @{ctx.author.name}")
        else:
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
    if game_ongoing:
        await ctx.channel.send("The hot bricktato is already being passed. Please try again later.")
    elif queueing is False:
        await ctx.send("No bricktato game currently going on. Use !open command to start a game of hot bricktato.")
    else:  # valid queue
        remove_player(ctx.author.name)
        await ctx.channel.send(f"@{ctx.author.name} does not want to play anymore.")


@bot.command(name='close')
async def close_command(ctx):
    global game_ongoing
    global queueing
    global has_potato
    if game_ongoing:
        await ctx.channel.send("The hot bricktato is already being passed. Please try again later.")
    elif queueing is False:
        await ctx.channel.send(
            "No bricktato game currently going on. Use !open command to start a game of hot bricktato.")
    else:
        if len(players) == 1:
            await ctx.channel.send("You need more than 1 person to play! Try again after someone has joined your lobby")
        else:
            queueing = False
            game_ongoing = True
            randomize_health()
            has_potato = randomize_player()
            print(potato_hp)
            print(players)
            await ctx.channel.send(f"The hot bricktato is on fire! @{has_potato} has the hot bricktato!")


@bot.command(name='who')
async def who_command(ctx):
    if has_potato is None:
        await ctx.channel.send("No one has the bricktato. Start a game with !open to play hot bricktato.")
    else:
        await ctx.channel.send(f"@{has_potato} has the hot bricktato")


@bot.command(name='toss')
async def toss_command(ctx):
    global game_ongoing
    global queueing
    global has_potato
    global players
    if game_ongoing is False:
        if queueing:
            await ctx.channel.send("Hot Bricktato has not yet started. !close the lobby to begin.")
        else:
            await ctx.channel.send("No one has the bricktato. Start a game with !open to play hot bricktato.")
    else:
        if ctx.author.name != has_potato:
            pass
        else:
            randomize_pass_loss()
            if potato_hp <= 0:
                remove_player(ctx.author.name)
                has_potato = randomize_player()
                if len(players) == 1:
                    reset_globals()
                    await ctx.channel.send(f"@{ctx.author.name} can't take the heat! Eliminated! @{has_potato} has won the game.")

                else:
                    await ctx.channel.send(f"@{ctx.author.name} can't take the heat! Eliminated! @{has_potato} now has the bricktato.")
            else:
                has_potato = randomize_player()
                await ctx.channel.send(f"@{ctx.author.name} tosses the brick! @{has_potato} now has the bricktato.")

def randomize_health():
    global potato_hp
    potato_hp = random.randint(1, 100)
    print(potato_hp)


def randomize_pass_loss():
    global potato_hp
    potato_hp -= random.randint(0, potato_hp)
    print(potato_hp)


def add_player(username):
    global players
    players.add(username)


def remove_player(username):
    global players
    if username in players:
        players.remove(username)


def randomize_player():
    global players
    return random.sample(players, 1)[0]


def reset_globals():
    global game_ongoing
    global queueing
    global players
    global potato_hp
    game_ongoing = False
    queueing = False
    players = set()
    potato_hp = 0


if __name__ == "__main__":
    bot.run()
