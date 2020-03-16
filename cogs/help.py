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
        commands['letmeknow'] = ['Get the letmeknow role, useful for getting pings when Lee goes live', '']
        commands['morning'] = ['Good morning to our glorious Supreme Leader', '']
        commands['challenge'] = ['Challenge another user', '<mention>']
        commands['quote'] = ['Shows quote #[quote_nr]; if no number given, a random quote is shown', '[quote_nr]', 'q']
        commands['add_quote'] = ['Adds quote', '<quote> - <user>']
        commands['remove_quote'] = ['Removes quote #[quote_nr] (Security only)', '<quote_nr>']
        commands['update_quote'] = ['Updates quote #[quote_nr] (Security only)', '<quote_nr> <"quote">']
        commands['mute'] = ['Mutes the tagged user (Security only)', '<mention>']
        commands['unmute'] = ['Unmutes the tagged user (Security only)', '<mention>']
        commands['ignore_channel'] = ['Adds [channel_id] to ignored channels; adds current channel if no parameter given (Security only)', '[channel_id]']
        commands['remove_ignore_channel'] = ['same as ignore_channel, but it removes the channel from the list (Security only)', '[channel_id]']
        commands['help'] = ['It\'s this command', '[command]', 'commands']

        prefix = 'l!'

        if not args:
            msg = '```'
            for command, desc in commands.items():  # for every command in the commands dict
                msg += f'{command} {desc[1]}\n'  # command name

            msg += f'''\n\n<required parameter>; [optional parameter]; \'...\' variable number of parameters; \'|\' OR operator\n
This server\'s prefix is {prefix}
Type {prefix}help [command] for more info on a command.```'''

        elif args[0] in commands:
            msg = f'```{prefix}{args[0]} {commands[args[0]][1]}\n\n{commands[args[0]][0]}\n\nAliases: {commands[args[0]][2]}```'  # command name and arguments (if needed)

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
