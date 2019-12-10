import discord.utils
from discord.ext import commands
from tokenfile import Vars


class TestCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_role('Security')
    async def test_role(self, ctx):
        role = discord.utils.get(ctx.guild.roles, name='Security')
        if role in ctx.author.roles:
            await ctx.send(f'You already have the role {role.name}')
        else:
            await ctx.send('You don\'t have the role')

    @commands.command(pass_context=True)  # just like say but in a specified channel
    @commands.check(Vars.user_is_me)
    async def says(self, ctx, ch, *args):
        channel = self.bot.get_channel(int(ch))
        await channel.send(' '.join(args))

    @commands.command()
    @commands.check(Vars.user_is_me)
    async def test_assign(self, ctx):
        role = discord.utils.get(ctx.author.guild.roles, name='test')
        await ctx.author.add_roles(role)

    @commands.command()
    async def test(self, ctx):
        await ctx.send('I work')


def setup(bot):
    bot.add_cog(TestCog(bot))
