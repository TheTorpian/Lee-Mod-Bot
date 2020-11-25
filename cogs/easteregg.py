import discord.utils
from discord.ext import commands


class EasterEggCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()  # "catch" a message with funny pics
    async def catch(self, ctx):
        await ctx.send(file=discord.File('Lee-Mod-Bot/catch1.png'))

        def check(m):
            return m.channel == ctx.message.channel

        await self.bot.wait_for('message', check=check)
        await ctx.send(file=discord.File('Lee-Mod-Bot/catch2.png'))

    @commands.command()  # best birthday video
    async def torp_shag(self, ctx):
        msg = 'https://youtu.be/7wdh3KLm9Xo'
        await ctx.send(msg)


def setup(bot):
    bot.add_cog(EasterEggCog(bot))
