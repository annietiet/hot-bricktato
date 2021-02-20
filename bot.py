import os
from twitchio.ext import commands
#pipenv run python bot.py

bot = commands.Bot(
    irc_token=os.environ['TMI_TOKEN'],
    client_id=os.environ['CLIENT_ID'],
    nick='hot_bricktato',
    prefix=os.environ['BOT_PREFIX'],
    initial_channels=['92soo'],
)

@bot.event
async def event_message(ctx):
    print(ctx.author)
    print(ctx.content)

@bot.event
async def bot_ready():
    'Called once when the bot goes online.'
    print(bot.nick + " is online!")
    ws = bot._ws  # this is only needed to send messages within event_ready
    await ws.send_privmsg(os.environ['CHANNEL'], f"/me has arrived! Is it getting hot in here?")

@bot.command(name='help')
async def help_command(ctx):
    await ctx.send("Use !play command to start a game of hot bricktato!")

if __name__ == "__main__":
    bot.run()