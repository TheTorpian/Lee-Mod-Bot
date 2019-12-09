import discord.utils
from discord.ext import commands
from tokenfile import Vars


class AdminCog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot


	@commands.Cog.listener()  # listener, checks on member join, assigns default role
	async def on_member_join(self, member):
		role = discord.utils.get(member.guild.roles, name='baby chicks')
		if role not in member.roles:
			await member.add_roles(role)


	@commands.command()  # adds letmeknow role
	async def letmeknow(self, ctx):
		role = discord.utils.get(ctx.author.guild.roles, name='letmeknow')
		if role in ctx.author.roles:
			await ctx.send('You already have the role...')
		else:
			await ctx.author.add_roles(role)
			await ctx.send('Role added!')


def setup(bot):
	bot.add_cog(AdminCog(bot))
