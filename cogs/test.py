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

    @commands.command()
    @user_is_torp()
    async def test_banlist(self, ctx, user):
        with open(Vars.ban_count, 'r') as f:  # read ban_count file into lines var
            lines = f.readlines()
        user_new = True
        with open(Vars.ban_count, 'w') as f:  # rewrite ban_count file
            for line in lines:
                if user in line:  # if given user is in list
                    newcount = int(line.strip('\n')[-1]) + 1  # increment the ban count by one
                    newline = f'{user} {newcount}\n'
                    f.write(newline)  # writes the modified line
                    user_new = False
                else:
                    f.write(line)  # rewrites old line if no need to modify
            if user_new:
                f.write(f'{user} 1\n')  # if user doesn't exist in list, it gets added

    @commands.command()
    @user_is_torp()
    async def test(self, ctx):
        await ctx.send('I work')


def setup(bot):
    bot.add_cog(TestCog(bot))
