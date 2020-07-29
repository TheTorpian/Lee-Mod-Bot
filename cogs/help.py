import os

from collections import OrderedDict
from discord.ext import commands
from sql import sql_ignored
from datetime import datetime

class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):  # checks if channel where command was called isn't ignored (value has to be false, func returns true if ignored)
        return not sql_ignored.check_ignore(ctx.message.channel.id)

    @commands.command(when_mentioned=True, aliases=['commands'])
    async def help(self, ctx, *args):
        commands = OrderedDict()
        commands['challenge'] = ['Challenge another user', '<mention>']
        commands['letmeknow'] = ['Get the letmeknow role, useful for getting pings when Lee goes live']
        commands['morning'] = ['Good morning to our glorious Supreme Leader']
        commands['quote'] = ['Shows quote #[quote_nr] or a random quote by [user]; if no number or user is given, a random quote is shown', '[quote_nr|user]', 'q']
        commands['add_quote'] = ['Adds quote', '<quote> - <user>']
        commands['remove_quote'] = ['Removes quote #[quote_nr] (Security only)', '<quote_nr>', 'remove_quote, del_quote']
        commands['update_quote'] = ['Updates quote #[quote_nr] (Security only)', '<quote_nr> <"quote">', 'edit_quote, mod_quote']
        commands['qcount'] = ['Shows how many quotes <name> has', '<name>']
        commands['visit'] = ['Check out the wonders of the gulag as a visitor for a limited time.']
        commands['mute'] = ['Mutes the tagged user (Security only)', '<mention>']
        commands['gulag'] = ['Sends the tagged user to the gulag (Security only)', '<mention>']
        commands['unmute'] = ['Unmutes the tagged user (Security only)', '<mention>']
        commands['free'] = ['Frees the tagged user from the gulag (Security only)', '<mention>']
        commands['escape'] = ['Attempt to escape from the gulag (in gulag only)']
        commands['ban'] = ['Bans the tagged user (Security only)', '<user_id> [reason] [days to purge]', 'yeet']
        commands['unban'] = ['Unbans the tagged user (Security only)', '<user_id> [reason]', 'unyeet']
        commands['offenses'] = ['Lists the amount of offenses the user has (Security only)', '<user_id>']
        commands['ignore'] = ['Adds [channel_id] to ignored channels; adds current channel if no parameter is given (Security only)', '[channel_id]', 'add_ignore']
        commands['del_ignore'] = ['Removes channel [channel_id] from the ignored channel list (Security only)', '[channel_id]', 'remove_ignore']
        commands['list_ignored'] = ['Lists all ignored channels (Security only)']
        commands['help'] = ['It\'s this command', '[command]', 'commands']

        prefix = 'l!'

        if not args:
            msg = '```'
            for command, desc in commands.items():  # for every command in the commands dict
                msg += f'{command}'  # command name
                try:
                    msg += f' {desc[1]}'
                except IndexError:
                    pass
                msg += f'\n'

            msg += f'''\n\n<required parameter>; [optional parameter]; \'...\' variable number of parameters; \'|\' OR operator\n
This server\'s prefix is {prefix}
Type {prefix}help [command] for more info on a command.```'''

        elif args[0] in commands:
            msg = f'```{prefix}{args[0]}'  # command name, arguments and aliases (if needed)
            try:
                msg += f' {commands[args[0]][1]}'
            except IndexError:
                pass
            msg += f'\n\n{commands[args[0]][0]}'
            try:
                msg += f'\n\nAliases: {commands[args[0]][2]}'
            except IndexError:
                pass
            msg += f'```'

        else:
            msg = 'No command called "'
            msg += ' '.join(args)
            msg += '" found.'
        await ctx.send(msg)

    @commands.command(when_mentioned=True)
    async def prefix(self, ctx):  # get the prefix for this server
        prefix = 'l!'
        await ctx.send(f'This server\'s prefix is `{prefix}`\nType {prefix}help to see a list of commands.')

    @commands.command()
    async def ping(self, ctx):
        time = ctx.message.created_at
        delta = datetime.now() - time
        latency = round(delta.total_seconds() * 1000, 2)
        await ctx.send(f'Pong! Approximate latency is {latency} ms')

        
    @commands.command()
    async def system(self, ctx):
        CPU_Pct = str(round(float(os.popen('''grep 'cpu ' /proc/stat | awk '{usage=($2+$4)*100/($2+$4+$5)} END {print usage }' ''').readline()), 2))
        tot_m, used_m, free_m = map(int, os.popen('free -t -m').readlines()[-1].split()[1:])

        string = "```Total Usage:\nCPU Usage    = %5s %%\nTotal Memory = %5s MB\nUsed Memory  = %5s MB\nFree Memory  = %5s MB```" % (CPU_Pct, tot_m, used_m, free_m)

        await ctx.send(string)

def setup(bot):
    bot.add_cog(HelpCog(bot))
