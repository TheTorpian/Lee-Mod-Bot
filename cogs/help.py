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
        commands['challenge <mention>'] = ['Challenge another user', '<mention>']
        commands['mute <mention>'] = ['Mutes the tagged user (Security only)', '<mention>']
        commands['unmute <mention>'] = ['Unmutes the tagged user (Security only)', '<mention>']
        commands['ignore_channel [channel_id]'] = ['Adds [channel_id] to ignored channels; adds current channel if no parameter given (Security only)', '[channel_id]']
        commands['remove_ignore_channel [channel_id]'] = ['same as ignore_channel, but it removes the channel from the list (Security only)', '[channel_id]']
        commands['help|commands [command]'] = ['It\'s this command', '[command]']

        prefix = 'l!'

        if not args:  # get longest command name, to have evenly spaced help message
            max_len = 0
            for cmd in commands:
                if len(cmd) > max_len:
                    max_len = len(cmd)

            msg = '```'
            for command, desc in commands.items():  # for every command in the commands dict
                msg += f'{command} '  # command name
                for _ in range(len(command), max_len):  # extra spaces
                    msg += ' '
                msg += f'{desc[0]}\n'  # add the description
            msg += f'''\n\n<required parameter>; [optional parameter]; \'...\' variable number of parameters; \'|\' OR operator\n
This server\'s prefix is {prefix}
Type {prefix}help [command] for more info on a command.```'''

        elif args[0] in commands:
            msg = f'```{prefix}{args[0]} {commands[args[0]][1]}\n\n{commands[args[0]][0]}```'  # command name and arguments (if needed)

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
