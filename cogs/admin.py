import discord.utils
from discord.ext import commands
from discord.ext.commands import has_permissions
from tokenfile import check_ignore


# @commands.check(check_ignore)
class AdminCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):  # checks if channel where command was called isn't ignored
        return check_ignore(ctx, ctx.message.channel.id)


    @commands.Cog.listener()  # listener, checks on member join, assigns default role
    async def on_member_join(self, member):
        role = discord.utils.get(member.guild.roles, name='baby chicks')
        if role not in member.roles:
            await member.add_roles(role)

    @commands.command()  # mute user
    @has_permissions(administrator=True, manage_roles=True)
    async def mute(self, ctx, user: discord.Member):
        timeout = discord.utils.get(ctx.guild.roles, name='Timeout')
        await user.add_roles(timeout)
        await ctx.send(f'{user} has been muted.')

    @commands.command()  # unmute user
    @has_permissions(administrator=True, manage_roles=True)
    async def unmute(self, ctx, user: discord.Member):
        timeout = discord.utils.get(ctx.guild.roles, name='Timeout')
        await user.remove_roles(timeout)
        await ctx.send(f'{user} has been unmuted.')

    @commands.command()  # add channel to ignored_channels
    @has_permissions(administrator=True, manage_roles=True)
    async def ignore_channel(self, ctx, channel = None):
        if channel is None:
            channel = str(ctx.message.channel.id)
        if not self.bot.get_channel(int(channel)):
            await ctx.send('Not a valid channel')
        else:
            if check_ignore(ctx, channel):  # returns false if channel is in list
                with open('ignored_channels', 'a+') as f:
                    f.write(f'{channel}\n')
                    f.close()
                await ctx.send(f'Added `{channel}` to ignored list.')
            else:
                await ctx.send(f'Channel `{channel}` already ignored.')

    @commands.command()  # remove channel from ignored_channels
    @has_permissions(administrator=True, manage_roles=True)
    async def remove_ignore_channel(self, ctx, channel = None):
        if channel is None:
            channel = str(ctx.message.channel.id)
        if not self.bot.get_channel(int(channel)):
            await ctx.send('Not a valid channel')
        else:
            if not check_ignore(ctx, channel):  # returns false if channel is in list
                with open('ignored_channels', 'r') as f:
                    lines = f.readlines()
                with open('ignored_channels', 'w') as f:
                    for line in lines:
                        if line.strip('\n') != channel:
                            f.write(line)
                await ctx.send(f'Removed `{channel}` from ignored list.')
            else:
                await ctx.send(f'Channel `{channel}` is not ignored.')

    @commands.command()  # adds letmeknow role
    async def letmeknow(self, ctx):
        role = discord.utils.get(ctx.author.guild.roles, name='letmeknow')
        if role in ctx.author.roles:
            await ctx.send('You already have the role...')
        else:
            await ctx.author.add_roles(role)
            await ctx.send('Role added!')


def setup(bot):
    bot.add_cog(AdminCog(bot))
