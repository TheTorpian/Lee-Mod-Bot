import discord.utils
from discord.ext import commands
from discord.ext.commands import has_permissions
from tokenfile import Vars
from datetime import datetime
from sql import sql_ignored, sql_offenses
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
    async def on_message_delete(self, message):  # sends an embed message in the message log channel when a message is deleted
        if message.guild.id != 542698023973683220:
            if message.author.id != Vars.poleece_tag:
                embed = discord.Embed(description='Deleted message', color=0xed1c27)
                embed.add_field(name='Content', value=message.content, inline=True)
                embed.add_field(name='Channel', value=message.channel.name, inline=False)
                embed.set_footer(text=message.author, icon_url=message.author.avatar_url)
                log_channel = self.bot.get_channel(int(Vars.deleted_messages_channel))
                await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):  # sends an embed message in the message log channel when a message is edited
        if before.guild.id != 542698023973683220:
            if before.author.id != Vars.poleece_tag and before.content != after.content:
                embed = discord.Embed(description='Edited message', color=0xed1c27)
                embed.add_field(name='Original', value=before.content, inline=True)
                embed.add_field(name='Edited', value=after.content, inline=True)
                embed.add_field(name='Channel', value=before.channel.name, inline=False)
                embed.set_footer(text=before.author, icon_url=before.author.avatar_url)
                log_channel = self.bot.get_channel(int(Vars.deleted_messages_channel))
                await log_channel.send(embed=embed)

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

    @commands.command()  # mute user
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
                sql_offenses.add_ban(user_id, 1)

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

    @commands.command()
    async def time(self, ctx):
        utc_now = pytz.utc.localize(datetime.utcnow())
        kst_now = utc_now.astimezone(pytz.timezone('Asia/Seoul'))
        await ctx.send(f'Lee\'s time is currently {kst_now.hour}:{kst_now.minute}, {kst_now.day}/{kst_now.month}/{kst_now.year}')

    @commands.command()
    async def report(self, ctx):
        await ctx.send('This incident has been reported to the authorities.')


def setup(bot):
    bot.add_cog(AdminCog(bot))
