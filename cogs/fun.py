import os
import re
import random
import requests
import discord
from discord.ext import commands
from sql import sql_ignored

lee_tag = os.getenv('LEETAG')
poleece_tag = os.getenv('POLEECETAG')
torp_tag = os.getenv('TORPTAG')

lee_tag = int(lee_tag)
poleece_tag = int(poleece_tag)
torp_tag = int(torp_tag)



class FunCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):  # checks if channel where command was called isn't ignored (value has to be false, func returns true if ignored)
        return not sql_ignored.check_ignore(ctx.message.channel.id)

    @commands.command()
    async def morning(self, ctx):
        await ctx.send('https://tenor.com/view/leader-kim-jong-un-north-korea-gif-8893271')

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

    @commands.command()  # Happy birthday Lee
    async def birthday(self, ctx):
        array = [
            'https://imgur.com/XKEfXzW',
            'https://imgur.com/xFTOsJe',
            'Happy birthday Lee <:LeeBday:519424058652098560>',
            'https://youtu.be/dq8iDBFvMm8'
        ]
        rand = random.randint(0, len(array) - 1)
        await ctx.send(array[rand])

    @commands.command()  # best birthday video
    async def best_birthday(self, ctx):
        msg = 'https://youtu.be/dq8iDBFvMm8'
        await ctx.send(msg)

    @commands.command()  # best birthday video
    async def torp_shag(self, ctx):
        msg = 'https://youtu.be/7wdh3KLm9Xo'
        await ctx.send(msg)

    @commands.command()  # special happy birthday
    async def hbd(self, ctx):
        birthday = discord.utils.get(ctx.guild.roles, name='BIRTHDAY KID')
        for member in ctx.guild.members:
            if birthday in member.roles:
                await ctx.send(f'Everyone come say Happy Birthday to {member.mention} and give them attention <:LeeBday:519424058652098560>')

    @commands.command()
    async def dad(self, ctx):
        req = requests.get('https://icanhazdadjoke.com/', headers = {"Accept": "application/json"})
        dadjoke = req.json().get('joke')
        await ctx.send(dadjoke)

    @commands.command()  # useless report command
    async def report(self, ctx):
        await ctx.send('This incident has been reported to the authorities.')

    @commands.Cog.listener()  # listener, checks every message
    async def on_message(self, ctx):
        if ctx.author.id != torp_tag:
            await self.egg_pun_deleter(ctx)
            # await self.dead_meme_deleter(ctx)

    async def egg_pun_deleter(self, ctx):  # checks for egg in message
        words = re.search(r'egg[^s\s\W]|eggs\w|\w[2:]egg|\wegg\w', ctx.content, re.IGNORECASE)
        if words is not None:
            await ctx.delete()

    async def dead_meme_deleter(self, ctx):  # checks for dead memes in message
        words = re.search(
            r'^.*?\bh(appy)?\b.*?\bb(irth)?d(ay)?\b.*?\b(love)?lee(face)?\b.*?$', ctx.content, re.IGNORECASE)
        if words is not None:
            await ctx.delete()


def setup(bot):
    bot.add_cog(FunCog(bot))
