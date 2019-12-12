import discord
from datetime import datetime
from discord.ext import commands
from tokenfile import Vars

import os

TOKEN = Vars.TOKEN


def get_prefix(bot, message):
    prefix = 'l!'
    return commands.when_mentioned_or(prefix)(bot, message)


cogs = [
    'cogs.admin',
    'cogs.help',
    'cogs.test',
    'cogs.fun'
]

bot = commands.Bot(command_prefix=get_prefix)
bot.remove_command('help')  # removes default help command

if __name__ == '__main__':
    for cog in cogs:
        bot.load_extension(cog)


@bot.command(name='reload', pass_context=True)  # reloads all cogs
@commands.check(Vars.user_is_me)
async def _reload(ctx):
    try:
        for cog in cogs:
            bot.unload_extension(cog)
            bot.load_extension(cog)
        await ctx.send('Cogs reloaded successfully!')
    except Exception:
        await ctx.send('An error occurred')


@bot.command(name='restart', pass_context=True)  # restarts bot app
@commands.check(Vars.user_is_me)
async def _restart(ctx):
    channel = bot.get_channel(581478717046521880)
    await channel.send('Restarting...')
    print('Logging out...\n')
    await bot.logout()  # logs out the app
    os.execl('kill.sh', '')

@bot.event
async def on_ready():
    game = discord.Activity(name='l!help', type=discord.ActivityType.listening)
    await bot.change_presence(status=discord.Status.online, activity=game)
    print(f'{datetime.now()}')
    print(f'Logged in as {bot.user.name}')
    channel = bot.get_channel(581478717046521880)
    await channel.send('Ready!')

bot.run(TOKEN, bot=True, reconnect=True)
