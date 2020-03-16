import re
import random
from discord.ext import commands
from discord.ext.commands import has_permissions
from sql import sql_quotes

tformat = '%d.%m.%Y'


class QuotesCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['q'])  # gets a random or selected quote from server
    async def quote(self, ctx, *quote_nr: int):
        try:
            quotes = sql_quotes.get_quote(ctx.guild.id)
            if not quote_nr:  # if command is called without args
                quote_nr = random.randint(0, len(quotes) - 1)
            else:
                quote_nr = int(quote_nr[0])
                quote_nr -= 1
            quote = quotes[quote_nr]
            time = quote[3].strftime(tformat)
            str_quote = f'Quote #{quote_nr+1}: {quote[2]} - {quote[1]} ({time})'
            await ctx.send(str_quote)
        except IndexError:
            await ctx.send('No quote found')

    @commands.command()  # adds quote for server
    async def add_quote(self, ctx):
        author = re.search(r'(\s[^-"]*$)', ctx.message.content)
        quote = re.search(r'"[^"]*"', ctx.message.content)
        if author and quote:
            sql_quotes.add_quote(author.group(0)[1:], quote.group(0), ctx.guild.id)
            await ctx.send('Quote added')
        else:
            await ctx.send('Wrong format, do `"quote" - user`')

    @commands.command()  # deletes quote
    @has_permissions(manage_messages=True)
    async def remove_quote(self, ctx, quote_nr):
        # await ctx.send(f'`{type(int(quote_nr))}`')
        sql_quotes.remove_quote(int(quote_nr))
        await ctx.send(f'Quote {quote_nr} deleted')

    @commands.command()  # modifies quote for server
    @has_permissions(manage_messages=True)
    async def update_quote(self, ctx, quote_nr: int, quote):
        quote = re.search(r'"[^"]*"', ctx.message.content)
        if quote:
            sql_quotes.update_quote(int(quote_nr), str(quote.group(0)))
            await ctx.send('Quote updated')
        else:
            await ctx.send('Wrong format, use `quote_nr` `"quote"`')

    # @commands.command()  # gets all the quotes from the server
    # async def quote_list(self, ctx):
    #     try:
    #         quotes = sql_quotes.get_quote(ctx.guild.id)
    #         str_quotes = ''
    #         for idx, quote in enumerate(quotes, start=1):
    #             time = quote[3].strftime(tformat)
    #             str_quote = f'Quote #{idx}: {quote[2]} - {quote[1]} ({time})'
    #             str_quotes += f'{str_quote}\n'
    #         await ctx.send(str_quotes)
    #     except IndexError:
    #         await ctx.send('No quotes found')


def setup(bot):
    bot.add_cog(QuotesCog(bot))
