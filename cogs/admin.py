import discord.utils
from discord.ext import commands
from discord.ext.commands import has_permissions
from tokenfile import Vars
from datetime import datetime
from sql import sql_ignored, sql_offenses, sql_escape
import pytz
import asyncio
import random
import time


class AdminCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()  # listener, checks on member join, assigns default role
    async def on_member_join(self, member):
        role = discord.utils.get(member.guild.roles, name='baby chicks')
        if role not in member.roles:
            await member.add_roles(role)

    @commands.Cog.listener()  # sends an embed message in the message log channel when a message is deleted
    async def on_message_delete(self, message):
        if message.guild.id == 511192102273548292:
            if message.author.id != Vars.poleece_tag:
                embed = discord.Embed(description='Deleted message', color=0xed1c27)
                embed.add_field(name='Content', value=message.content, inline=True)
                embed.add_field(name='Channel', value=message.channel.name, inline=False)
                embed.set_footer(text=message.author, icon_url=message.author.avatar_url)
                log_channel = self.bot.get_channel(int(Vars.deleted_messages_channel))
                await log_channel.send(embed=embed)

    @commands.Cog.listener()  # sends an embed message in the message log channel when a message is edited
    async def on_message_edit(self, before, after):
        if before.guild.id == 511192102273548292:
            if before.author.id != Vars.poleece_tag and before.content != after.content:
                embed = discord.Embed(description='Edited message', color=0xed1c27)
                embed.add_field(name='Original', value=before.content, inline=True)
                embed.add_field(name='Edited', value=after.content, inline=True)
                embed.add_field(name='Channel', value=before.channel.name, inline=False)
                embed.set_footer(text=before.author, icon_url=before.author.avatar_url)
                log_channel = self.bot.get_channel(int(Vars.deleted_messages_channel))
                await log_channel.send(embed=embed)

    @commands.command()  # adds visitor role, allows chatting in gulag for a limited time
    async def visit(self, ctx):
        visitor = discord.utils.get(ctx.guild.roles, name='Visitor')
        gulag_channel = self.bot.get_channel(int(Vars.gulag_channel))
        await ctx.author.add_roles(visitor)
        await gulag_channel.send(f'{ctx.author} is now a visitor. You have two minutes as a visitor.')
        await asyncio.sleep(105)
        await gulag_channel.send(f'<@{ctx.author.id}>, you have 15 seconds left as a visitor.')
        await asyncio.sleep(15)
        await ctx.author.remove_roles(visitor)
        await gulag_channel.send(f'<@{ctx.author.id}>, your visit has ended.')

    @commands.command()  # mute user
    @has_permissions(manage_roles=True)
    async def mute(self, ctx, user: discord.Member):
        timeout = discord.utils.get(ctx.guild.roles, name='Timeout')
        await user.add_roles(timeout)

        # ban counter module
        offense_count = sql_offenses.get_bancount(user.id)
        if offense_count:
            offense_count = offense_count[0]  # result from query is tuple, I need only first (and only) value of tuple
            sql_offenses.alter_ban(user.id, offense_count + 1)
        else:
            sql_offenses.add_ban(user.id, 1)

        await ctx.send(f'{user} has been muted.')

    @commands.command()  # same as mute command, but with extra flavour
    @has_permissions(manage_roles=True)
    async def gulag(self, ctx, user: discord.Member):
        timeout = discord.utils.get(ctx.guild.roles, name='Timeout')
        await user.add_roles(timeout)

        # ban counter module
        offense_count = sql_offenses.get_bancount(user.id)
        if offense_count:
            offense_count = offense_count[0]  # result from query is tuple, I need only first (and only) value of tuple
            sql_offenses.alter_ban(user.id, offense_count + 1)
        else:
            sql_offenses.add_ban(user.id, 1)

        await ctx.send(f'{user} has been sent to gulag.')

    @commands.command()  # unmute user
    @has_permissions(manage_roles=True)
    async def unmute(self, ctx, user: discord.Member):
        timeout = discord.utils.get(ctx.guild.roles, name='Timeout')
        await user.remove_roles(timeout)
        await ctx.send(f'{user} has been unmuted.')

    @commands.command()  # same as unmute, but with extra flavour
    @has_permissions(manage_roles=True)
    async def free(self, ctx, user: discord.Member):
        timeout = discord.utils.get(ctx.guild.roles, name='Timeout')
        await user.remove_roles(timeout)
        await ctx.send(f'{user} has been freed.')

    @commands.command(aliases=['yeet'])  # ban user
    @has_permissions(ban_members=True)
    async def ban(self, ctx, user_id, reason=None, delete_message_days=0):
        if not reason:
            reason = 'No reason'
        try:
            user = ctx.guild.get_member(int(user_id))
            await ctx.guild.ban(user, reason=reason)

            # ban counter module
            offense_count = sql_offenses.get_bancount(user_id)
            if offense_count:
                offense_count = offense_count[0]  # result from query is tuple, I need only first (and only) value of tuple
                sql_offenses.alter_ban(user_id, offense_count + 1)
            else:
                sql_offenses.add_ban(user_id, delete_message_days)

            await ctx.send(f'{user} has been banned.')
        except discord.errors.HTTPException:
            await ctx.send('No user found.')
        except ValueError:
            await ctx.send('You must provide a user id.')

    @commands.command(aliases=['unyeet'])  # unban user
    @has_permissions(ban_members=True)
    async def unban(self, ctx, user_id, reason=None):
        if not reason:
            reason = 'No reason'
        try:
            user = await self.bot.fetch_user(int(user_id))
            await ctx.guild.unban(user, reason=reason)
            await ctx.send(f'{user} has been unbanned.')
        except discord.errors.HTTPException:  # error is raised when unbanning fails
            await ctx.send('No user found or user is not banned.')
        except ValueError:
            await ctx.send('You must provide a user id.')

    @commands.command()  # attempt to escape from gulag
    async def escape(self, ctx):
        gulag_channel = self.bot.get_channel(int(Vars.gulag_channel))
        timeout = discord.utils.get(ctx.guild.roles, name='Timeout')
        cooldown = sql_escape.get_time()
        cooldown = cooldown[0]  # result from query is tuple, I need only first (and only) value of tuple
        if (ctx.channel.id == gulag_channel) and (timeout in ctx.author.roles):
            if int(time.time()) - cooldown > 1800:
                x = random.choice(range(0, 6969))
                if x <= 69 and not ctx.author.bot:
                    await ctx.author.remove_roles(timeout)
                    await ctx.send('Fuck he escaped')
                else:
                    await ctx.send('You failed to escape.')
                sql_escape.update_time(int(time.time()))
            else:
                await ctx.send('There has been a recent escape attempt already.')

    @commands.command()  # checks mutes and bans of user
    @has_permissions(manage_roles=True)
    async def offenses(self, ctx, user_id):
        ban_count = sql_offenses.get_bancount(user_id)
        if ban_count:
            await ctx.send(f'User has {ban_count[0]} offense(s).')
        else:
            await ctx.send('User has no offenses.')

    @commands.command(aliases=['add_ignore'])  # add channel to ignored_channels
    @has_permissions(administrator=True)
    async def ignore(self, ctx, channel=None):
        if channel is None:  # if no channel is provided, the one where the command was called is assigned
            channel = str(ctx.message.channel.id)
        ch_obj = self.bot.get_channel(int(channel))
        if not ch_obj:
            await ctx.send('Not a valid channel')
        else:
            if not sql_ignored.check_ignore(channel):  # returns true if channel is in list
                sql_ignored.add_ignored(channel, ch_obj.name)
                await ctx.send(f'Added `{channel}` to ignored list.')
            else:
                await ctx.send(f'Channel `{channel}` already ignored.')

    @commands.command(aliases=['remove_ignore'])  # remove channel from ignored_channels
    @has_permissions(administrator=True)
    async def del_ignore(self, ctx, channel=None):
        if channel is None:  # if no channel is provided, the one where the command was called is assigned
            channel = str(ctx.message.channel.id)
        ch_obj = self.bot.get_channel(int(channel))
        if not ch_obj:
            await ctx.send('Not a valid channel')
        else:
            if sql_ignored.check_ignore(channel):  # returns true if channel is in list
                sql_ignored.remove_ignored(channel)
                await ctx.send(f'Removed `{channel}` from ignored list.')
            else:
                await ctx.send(f'Channel `{channel}` is not ignored.')

    @commands.command()  # lists ignored channels
    @has_permissions(manage_roles=True)
    async def list_ignored(self, ctx):
        ignored_list = sql_ignored.get_ignored()
        for ignored in ignored_list:
            await ctx.send(f'<#{ignored[0]}>\n')

    @commands.command()  # adds letmeknow role
    async def letmeknow(self, ctx):
        role = discord.utils.get(ctx.author.guild.roles, name='letmeknow')
        if role in ctx.author.roles:
            await ctx.send('You already have the role...')
        else:
            await ctx.author.add_roles(role)
            await ctx.send('Role added!')

    @commands.command()  # returns local time in South Korea
    async def time(self, ctx):
        utc_now = pytz.utc.localize(datetime.utcnow())
        kst_now = utc_now.astimezone(pytz.timezone('Asia/Seoul'))
        await ctx.send(f'Lee\'s time is currently {kst_now.hour}:{kst_now.minute}, {kst_now.day}/{kst_now.month}/{kst_now.year}')

    @commands.command()  # useless report command
    async def report(self, ctx):
        await ctx.send('This incident has been reported to the authorities.')

    @commands.command()  # "catch" a message with funny pics
    @has_permissions(manage_roles=True)
    async def catch(self, ctx):
        await ctx.send(file=discord.File('catch1.png'))

        def check(m):
            return m.channel == ctx.message.channel

        await self.bot.wait_for('message', check=check)
        await ctx.send(file=discord.File('catch2.png'))


def setup(bot):
    bot.add_cog(AdminCog(bot))
