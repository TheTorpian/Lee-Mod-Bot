import discord.utils
from discord.ext import commands
from tokenfile import Vars, check_ignore, user_is_torp


class TestCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):  # checks if channel where command was called isn't ignored
        return check_ignore(ctx, ctx.message.channel.id)

    @commands.command()
    @commands.has_role('Security')
    @user_is_torp()
    async def test_role(self, ctx):
        role = discord.utils.get(ctx.guild.roles, name='Security')
        if role in ctx.author.roles:
            await ctx.send(f'You already have the role {role.name}')
        else:
            await ctx.send('You don\'t have the role')

    @commands.command()
    @user_is_torp()
    async def test_embed(self, ctx):
        embed = discord.Embed(description='Edited message', color=0xed1c27)
        embed.add_field(name='Original', value='before.content', inline=True)
        embed.add_field(name='Edited', value='after.content', inline=True)
        embed.add_field(name='Channel', value=ctx.channel.name, inline=False)
        embed.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)

        log_channel = self.bot.get_channel(int(Vars.deleted_messages_channel_test))
        await log_channel.send(embed=embed)

    @commands.command(pass_context=True)  # says args in code block
    @user_is_torp()
    async def get_args(self, ctx, *args):
        tag = ' '.join(args)
        await ctx.send(f'`{tag}`')

    @commands.command(pass_context=True)  # says args in code block
    @user_is_torp()
    async def get_guild(self, ctx):
        await ctx.send(f'`{ctx.guild.id}`')

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
    async def test(self, ctx):
        await ctx.send('I work')


def setup(bot):
    bot.add_cog(TestCog(bot))
