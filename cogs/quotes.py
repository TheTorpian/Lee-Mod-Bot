import re
import random
from discord.ext import commands
from discord.ext.commands import has_permissions
from fuzzywuzzy import fuzz
from sql import sql_quotes

tformat = '%d.%m.%Y'


class QuotesCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['q'])  # gets a random or selected quote from server
    async def quote(self, ctx, *quote_arg):
        try:
            quotes = sql_quotes.get_quote()

            # get random quote or selected quote
            if not quote_arg:  # if command is called without args
                quote_arg = random.randint(0, len(quotes) - 1)
                quote = quotes[quote_arg]
            else:
                quote_arg = quote_arg[0]  # command args are in a tuple, we only need the first result anyway
                match_nr = re.match(r'^[0-9]*$', quote_arg)
                if match_nr:  # if command is called with a quote number
                    quote_arg = int(quote_arg)
                    quote_arg -= 1
                    quote = quotes[quote_arg]
                else:
                    quotes_result = list()
                    for quote in quotes:
                        if fuzz.token_sort_ratio(quote_arg, quote[1]) > 80:
                            quotes_result.append(quote)
                    # await ctx.send(quotes_result)
                    quote = random.choice(quotes_result)

            # final message structuring
            if quote[1]:
                final_quote = f'#{quote[0]}: "{quote[2]}" - {quote[1]}'
            else:
                final_quote = f'#{quote[0]}: {quote[2]}'
            await ctx.send(final_quote)
        except IndexError:
            await ctx.send('No quote found')

    @commands.command()  # adds quote for server
    async def add_quote(self, ctx):
        author = re.search(r'(\s[^-"]*$)', ctx.message.content)
        quote = re.search(r'(")([^"]*)(")', ctx.message.content)
        quote_link = re.search(r'http[s]?://[^ ]+', ctx.message.content)

        if author and quote:  # if both name and quote is provided
            sql_quotes.add_quote(author.group(1)[1:], quote.group(2), ctx.guild.id)
            last_quote = sql_quotes.get_last_quote()
            await ctx.send(f'Quote entry #{last_quote[0]} added')
        elif quote_link:  # if only quote is provided (mainly screenshots/links)
            sql_quotes.add_quote_no_user(str(quote_link.group(0)), ctx.guild.id)
            last_quote = sql_quotes.get_last_quote()
            await ctx.send(f'Quote entry #{last_quote[0]} added')
        else:
            await ctx.send('Wrong format, do `"quote" - name` or `<link>`')

    @commands.command()  # deletes quote
    @has_permissions(manage_messages=True)
    async def remove_quote(self, ctx, quote_nr):
        sql_quotes.remove_quote(int(quote_nr))
        await ctx.send(f'Quote #{quote_nr} deleted')

    @commands.command()  # modifies quote for server
    @has_permissions(manage_messages=True)
    async def update_quote(self, ctx, quote_nr: int, quote):
        quote = re.search(r'(")([^"]*)(")', ctx.message.content)
        if quote:
            sql_quotes.update_quote(int(quote_nr), str(quote.group(1)))
            await ctx.send(f'Quote #{quote_nr} updated')
        else:
            await ctx.send('Wrong format, use `quote_nr` `"quote"`')


def setup(bot):
    bot.add_cog(QuotesCog(bot))
