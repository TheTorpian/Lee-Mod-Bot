import discord.utils
from discord.ext import commands
from discord.ext.commands import has_permissions
from tokenfile import Vars
from datetime import datetime
import pytz

import time


class AdminFunCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def visit(self, ctx):
        visitor = discord.utils.get(ctx.guild.roles, name='Visitor')
        await ctx.send(f'<@{ctx.author.id}> is now a visitor. You have two minutes as a visitor.')
        await ctx.author.add_roles(visitor)
        time.sleep(105)
        await ctx.send(f'<@{ctx.author.id}>, you have 15 seconds left as a visitor.')
        time.sleep(15)
        await ctx.author.remove_roles(visitor)
        await ctx.send(f'<@{ctx.author.id}>, your visit power has been removed.')
