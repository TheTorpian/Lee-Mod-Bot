import discord.utils
from discord.ext import commands
from tokenfile import user_is_torp
# from sql import sql_offenses


class TestCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_role('Security')
    @user_is_torp()
    async def test_role(self, ctx):
        role = discord.utils.get(ctx.guild.roles, name='Security')
        if role in ctx.author.roles:
            await ctx.send(f'You already have the role {role.name}')
        else:
            await ctx.send('You don\'t have the role')

    @commands.command(pass_context=True)  # says args in code block
    @user_is_torp()
    async def get_args(self, ctx, *args):
        tag = ' '.join(args)
        await ctx.send(f'`{tag}`')

    @commands.command(pass_context=True)  # says args in code block
    @user_is_torp()
    async def get_guild(self, ctx):
        await ctx.send(f'`{ctx.guild.id}`')

    @commands.command(pass_context=True)
    @user_is_torp()
    async def say(self, ctx, *args):
        await ctx.send(' '.join(args))

    @commands.command(pass_context=True)  # just like say but in a specified channel
    @user_is_torp()
    async def says(self, ctx, ch, *args):
        channel = self.bot.get_channel(int(ch))
        await channel.send(' '.join(args))

    @commands.command()
    @user_is_torp()
    async def test_assign(self, ctx):
        role = discord.utils.get(ctx.author.guild.roles, name='test')
        await ctx.author.add_roles(role)

    @commands.command()
    @user_is_torp()
    async def test_member(self, ctx, user_id):
        try:
            user = await self.bot.fetch_user(int(user_id))
            await ctx.send(user)
        except discord.errors.HTTPException:
            await ctx.send('No user found.')
        except ValueError:
            await ctx.send('You must provide a user id.')

    # @commands.command()
    # @user_is_torp()
    # async def test_banlist(self, ctx, user):
    #     offense = sql_offenses.get_bancount(user)
    #     if offense:
    #         await ctx.send(f'{offense[0]}')
    #     else:
    #         await ctx.send('result is none')

    @commands.command()
    @user_is_torp()
    async def test_channelname(self, ctx, c_id):
        channel = self.bot.get_channel(int(c_id))
        await ctx.send(f'{c_id}: {channel.name}')

    @commands.command()
    @user_is_torp()
    async def test(self, ctx):
        await ctx.send('I work')


def setup(bot):
    bot.add_cog(TestCog(bot))
