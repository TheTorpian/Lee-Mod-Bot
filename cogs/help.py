from collections import OrderedDict
from discord.ext import commands
from tokenfile import Vars

INVITE = Vars.INVITE


class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(when_mentioned=True, aliases=['commands'])
    async def help(self, ctx, *args):
        commands = OrderedDict()
        commands['challenge'] = ['Challenge another user', '<mention>']
        commands['letmeknow'] = ['Get the letmeknow role, useful for getting pings when Lee goes live']
        commands['morning'] = ['Good morning to our glorious Supreme Leader']
        commands['quote'] = ['Shows quote #[quote_nr] or a random quote by [user]; if no number or user is given, a random quote is shown', '[quote_nr|user]', 'q']
        commands['add_quote'] = ['Adds quote', '<quote> - <user>']
        commands['remove_quote'] = ['Removes quote #[quote_nr] (Security only)', '<quote_nr>']
        commands['update_quote'] = ['Updates quote #[quote_nr] (Security only)', '<quote_nr> <"quote">']
        commands['mute'] = ['Mutes the tagged user (Security only)', '<mention>']
        commands['unmute'] = ['Unmutes the tagged user (Security only)', '<mention>']
        commands['ban'] = ['Bans the tagged user (Security only)', '<mention> [reason] [days to purge]', 'yeet']
        commands['unban'] = ['Unbans the tagged user (Security only)', '<mention> [reason]', 'unyeet']
        commands['offenses'] = ['Lists the amount of offenses the user has (Security only)', '<mention>', '']
        commands['ignore'] = ['Adds [channel_id] to ignored channels; adds current channel if no parameter is given (Security only)', '[channel_id]']
        commands['del_ignore'] = ['Removes channel [channel_id] from the ignored channel list (Security only)', '[channel_id]']
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

    @commands.command()  # invite link
    async def invite(self, ctx):
        await ctx.send(INVITE)


def setup(bot):
    bot.add_cog(HelpCog(bot))
