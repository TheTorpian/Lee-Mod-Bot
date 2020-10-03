import os
import discord
from datetime import datetime
from discord.ext import commands
from tokenfile import user_is_torp

TOKEN = os.getenv('TOKEN')
# idk how intents actually work yet, just doing what the docs say
intents = discord.Intents.default()
intents.members = True
intents.messages = True


def get_prefix(bot, message):
    prefix = 'l!'
    return commands.when_mentioned_or(prefix)(bot, message)


cogs = [
    'cogs.admin',
    'cogs.help',
    'cogs.fun',
    'cogs.quotes',
    'cogs.test',
    'cogs.error_handler'
]

bot = commands.Bot(command_prefix=get_prefix, intents=intents)
bot.remove_command('help')  # removes default help command

if __name__ == '__main__':
    for cog in cogs:
        bot.load_extension(cog)


@bot.command(name='reload', pass_context=True)  # reloads all cogs
@user_is_torp()
async def _reload(ctx):
    try:
        for cog in cogs:
            bot.unload_extension(cog)
            bot.load_extension(cog)
        await ctx.send('Cogs reloaded successfully!')
    except Exception:
        await ctx.send('An error occurred')


@bot.event
async def on_ready():
    game = discord.Activity(name='l!help', type=discord.ActivityType.listening)
    await bot.change_presence(status=discord.Status.online, activity=game)
    print(f'{datetime.now()}')
    print(f'Logged in as {bot.user.name}\n')

bot.run(TOKEN, bot=True, reconnect=True)
