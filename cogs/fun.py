import re
import random
import discord
from discord.ext import commands
from tokenfile import Vars, check_ignore


class FunCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):  # checks if channel where command was called isn't ignored
        return check_ignore(ctx, ctx.message.channel.id)

    @commands.command()
    async def morning(self, ctx):
        await ctx.send('https://tenor.com/view/leader-kim-jong-un-north-korea-gif-8893271')

    @commands.command()  # challenge the tagged user
    async def challenge(self, ctx, tag: discord.Member):
        supreme_user = ctx.guild.get_member(Vars.lee_tag)
        bot_user = ctx.guild.get_member(Vars.poleece_tag)
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

    @commands.Cog.listener()  # listener, checks every message
    async def on_message(self, ctx):
        await self.egg_pun_deleter(ctx)

    async def egg_pun_deleter(self, ctx):  # checks for egg in message
        words = re.search(r'egg[^s\s\W]|eggs\w|\w[2:]egg|\wegg\w', ctx.content, re.IGNORECASE)
        if words is not None:
            await ctx.delete()


def setup(bot):
    bot.add_cog(FunCog(bot))
