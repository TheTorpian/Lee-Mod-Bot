import os
import re
import random
import requests
import discord
import asyncio
from discord.ext import commands
from datetime import datetime
from sql import sql_ignored, sql_offenses
import pytz

lee_tag = os.getenv('LEETAG')
poleece_tag = os.getenv('POLEECETAG')
torp_tag = os.getenv('TORPTAG')
gulag_channel = os.getenv('GULAGCHNL')

lee_tag = int(lee_tag)
poleece_tag = int(poleece_tag)
torp_tag = int(torp_tag)
gulag_channel = int(gulag_channel)


class FunCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):  # checks if channel where command was called isn't ignored (value has to be false, func returns true if ignored)
        return not sql_ignored.check_ignore(ctx.message.channel.id)

    # dead meme
    # @commands.command()
    # async def morning(self, ctx):
    #     await ctx.send('https://tenor.com/view/leader-kim-jong-un-north-korea-gif-8893271')

    @commands.command()  # adds visitor role, allows chatting in gulag for a limited time
    async def visit(self, ctx):
        visitor = discord.utils.get(ctx.guild.roles, name='Visitor')
        timeout = discord.utils.get(ctx.guild.roles, name='Timeout')
        if timeout not in ctx.author.roles:
            if visitor not in ctx.author.roles:
                gulag = self.bot.get_channel(gulag_channel)
                await ctx.author.add_roles(visitor)
                await gulag.send(f'{ctx.author} is now a visitor. You have two minutes as a visitor.')
                await asyncio.sleep(105)
                await gulag.send(f'<@{ctx.author.id}>, you have 15 seconds left as a visitor.')
                await asyncio.sleep(15)
                await ctx.author.remove_roles(visitor)
                await gulag.send(f'<@{ctx.author.id}>, your visit has ended.')
            else:
                await ctx.send('You\'re already a visitor.')
        else:
            await ctx.send('You\'re already here, no need for a visitor pass :)')

    @commands.command()  # checks mutes and bans of user
    async def offenses(self, ctx, user_id):
        uid = re.search(r'(\d){18}', user_id, re.IGNORECASE)  # dirty solution with regex but it should work
        if uid is not None:
            ban_count = sql_offenses.get_bancount(uid.group(0))
            if ban_count:
                await ctx.send(f'User has {ban_count[0]} offense(s).')
            else:
                await ctx.send('User has no offenses.')

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

    @commands.command()  # challenge the tagged user
    async def challenge(self, ctx, tag: discord.Member):
        supreme_user = ctx.guild.get_member(lee_tag)
        bot_user = ctx.guild.get_member(poleece_tag)
        outcome = random.randint(0, 1)

        if tag == bot_user:  # PoLeece Bot never loses
            await ctx.send('You don\'t challenge the Secret PoLeece.')
        else:
            if tag == supreme_user:
                await ctx.send('You don\'t challenge the Supreme Leader')
            elif tag == ctx.author:
                await ctx.send('You can\'t challenge yourself')
            else:
                if outcome:
                    await ctx.send(f'{tag.display_name} won!')
                    await ctx.send(f'{ctx.author.display_name} lost!')
                else:
                    await ctx.send(f'{ctx.author.display_name} won!')
                    await ctx.send(f'{tag.display_name} lost!')

    # more dead memes
    # @commands.command()  # Happy birthday Lee
    # async def birthday(self, ctx):
    #     array = [
    #         'https://imgur.com/XKEfXzW',
    #         'https://imgur.com/xFTOsJe',
    #         'Happy birthday Lee <:LeeBday:519424058652098560>',
    #         'https://youtu.be/dq8iDBFvMm8'
    #     ]
    #     rand = random.randint(0, len(array) - 1)
    #     await ctx.send(array[rand])

    # @commands.command()  # best birthday video
    # async def best_birthday(self, ctx):
    #     msg = 'https://youtu.be/dq8iDBFvMm8'
    #     await ctx.send(msg)

    @commands.command()  # special happy birthday
    async def hbd(self, ctx):
        birthday = discord.utils.get(ctx.guild.roles, name='BIRTHDAY KID')
        for member in ctx.guild.members:
            if birthday in member.roles:
                await ctx.send(f'Everyone come say Happy Birthday to {member.mention} and give them attention <:LeeBday:519424058652098560>')

    @commands.command()
    async def dad(self, ctx):
        req = requests.get('https://icanhazdadjoke.com/', headers={"Accept": "application/json"})
        dadjoke = req.json().get('joke')
        await ctx.send(dadjoke)

    @commands.command()  # useless report command
    async def report(self, ctx):
        await ctx.send(f'Dear {ctx.author}, we\'re sorry for the inconvenience. Please check the email. The Secret Poleece team.')

    @commands.Cog.listener()  # listener, checks every message
    async def on_message(self, ctx):
        if ctx.author.id != torp_tag:
            await self.egg_pun_deleter(ctx)
            await self.dead_meme_deleter(ctx)

    async def egg_pun_deleter(self, ctx):  # checks for egg in message
        words = re.search(r'egg[^s\s\W]|eggs\w|\w[2:]egg|\wegg\w', ctx.content, re.IGNORECASE)
        if words is not None:
            await ctx.delete()

    async def dead_meme_deleter(self, ctx):  # checks for dead memes in message
        words = re.search(
            r'^.*?\bh(appy\b.*?\b)?b(irth)?d(ay)?\b.*?\b(love)?lee(face)?\b.*?$', ctx.content, re.IGNORECASE)
        if words is not None:
            await ctx.delete()


def setup(bot):
    bot.add_cog(FunCog(bot))
