import discord.utils
from discord.ext import commands
from discord.ext.commands import has_permissions
from tokenfile import check_ignore, Vars
from datetime import datetime
import pytz


class AdminCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()  # listener, checks on member join, assigns default role
    async def on_member_join(self, member):
        role = discord.utils.get(member.guild.roles, name='baby chicks')
        if role not in member.roles:
            await member.add_roles(role)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.id != Vars.poleece_tag:
            embed = discord.Embed(description='Deleted message', color=0xed1c27)
            embed.add_field(name='Content', value=message.content, inline=True)
            embed.set_footer(text=message.author, icon_url=message.author.avatar_url)
            log_channel = self.bot.get_channel(int(Vars.deleted_messages_channel))
            await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author.id != Vars.poleece_tag and before.content != after.content:
            embed = discord.Embed(description='Edited message', color=0xed1c27)
            embed.add_field(name='Original', value=before.content, inline=True)
            embed.add_field(name='Edited', value=after.content, inline=True)
            embed.set_footer(text=before.author, icon_url=before.author.avatar_url)
            log_channel = self.bot.get_channel(int(Vars.deleted_messages_channel))
            await log_channel.send(embed=embed)

    @commands.command()  # mute user
    @has_permissions(manage_roles=True)
    async def mute(self, ctx, user: discord.Member):
        timeout = discord.utils.get(ctx.guild.roles, name='Timeout')
        await user.add_roles(timeout)
        await ctx.send(f'{user} has been muted.')

    @commands.command()  # unmute user
    @has_permissions(manage_roles=True)
    async def unmute(self, ctx, user: discord.Member):
        timeout = discord.utils.get(ctx.guild.roles, name='Timeout')
        await user.remove_roles(timeout)
        await ctx.send(f'{user} has been unmuted.')

    @commands.command()  # add channel to ignored_channels
    @has_permissions(administrator=True)
    async def ignore_channel(self, ctx, channel=None):
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
    @has_permissions(administrator=True)
    async def remove_ignore_channel(self, ctx, channel=None):
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

    @commands.command()
    async def time(self, ctx):
        utc_now = pytz.utc.localize(datetime.utcnow())
        kst_now = utc_now.astimezone(pytz.timezone('Asia/Seoul'))
        await ctx.send(f'Lee\'s time is currently {kst_now.hour}:{kst_now.minute}, {kst_now.day}/{kst_now.month}/{kst_now.year}')


def setup(bot):
    bot.add_cog(AdminCog(bot))
