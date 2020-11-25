import os
import discord.utils
from discord.ext import commands
from discord.ext.commands import has_permissions
from sql import sql_ignored, sql_offenses, sql_escape
import random
import time

poleece_tag = os.getenv('POLEECETAG')
deleted_messages_channel = os.getenv('DELMSGCHNL')
gulag_channel = os.getenv('GULAGCHNL')
poleece_tag = int(poleece_tag)
deleted_messages_channel = int(deleted_messages_channel)
gulag_channel = int(gulag_channel)


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
        if message.guild.id == 511192102273548292:  # hardcoded cause I don't want it working in my testing server
            if message.author.id != poleece_tag:  # doesn't show the bot's deleted messages
                if message.content.lower() != 'h!trick' and message.content.lower() != 'h!treat':  # prevent trick or treat commands to show up in the log
                    embed = discord.Embed(description='Deleted message', color=0xed1c27)
                    embed.add_field(name='Content', value=message.content, inline=True)
                    embed.add_field(name='Channel', value=message.channel.name, inline=False)
                    embed.set_footer(text=message.author, icon_url=message.author.avatar_url)
                    log_channel = self.bot.get_channel(deleted_messages_channel)
                    await log_channel.send(embed=embed)

    @commands.Cog.listener()  # sends an embed message in the message log channel when a message is edited
    async def on_message_edit(self, before, after):
        if before.guild.id == 511192102273548292:  # hardcoded cause I don't want it working in my testing server
            if before.author.id != poleece_tag and before.content != after.content:
                embed = discord.Embed(description='Edited message', color=0xed1c27)
                embed.add_field(name='Original', value=before.content, inline=True)
                embed.add_field(name='Edited', value=after.content, inline=True)
                embed.add_field(name='Channel', value=before.channel.name, inline=False)
                embed.set_footer(text=before.author, icon_url=before.author.avatar_url)
                log_channel = self.bot.get_channel(deleted_messages_channel)
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

        gulag_file = discord.File('gulag.png')
        await ctx.send(file=gulag_file)
        await ctx.send(f'What\'s missing from g_lag? U')

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
        gulag = self.bot.get_channel(gulag_channel)
        timeout = discord.utils.get(ctx.guild.roles, name='Timeout')
        cooldown = sql_escape.get_time()
        cooldown = cooldown[0]  # result from query is tuple, I need only first (and only) value of tuple

        if (ctx.channel == gulag) and (timeout in ctx.author.roles):
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

        # rigged escape, in case some guard "accidentally" drops the key
        # if (ctx.channel == gulag_channel) and (timeout in ctx.author.roles):
        #     await ctx.author.remove_roles(timeout)
        #     await ctx.send('Fuck he escaped')

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


def setup(bot):
    bot.add_cog(AdminCog(bot))
