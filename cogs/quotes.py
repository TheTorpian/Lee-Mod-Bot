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
                        if (fuzz.token_sort_ratio(quote_arg, quote[1]) > 50) or (quote_arg in quote[2]):
                            quotes_result.append(quote)
                    quote = random.choice(quotes_result)

            # final message structuring
            if quote[1]:  # if quote has a quoted_tag value
                final_quote = f'#{quote[0]}: "{quote[2]}" - {quote[1]}'
            else:  # usually a link
                final_quote = f'#{quote[0]}: {quote[2]}'
            await ctx.send(final_quote)
        except IndexError:
            await ctx.send('No quote found')

    @commands.command()  # adds quote for server
    async def add_quote(self, ctx):
        author = re.search(r'(\s[^-"]*$)', ctx.message.content)
        quote = re.search(r'(")([^"]*)(")', ctx.message.content)
        quote_link = re.search(r'http[s]?://[^"]+', ctx.message.content)

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

    @commands.command(aliases=['delete_quote', 'del_quote'])  # deletes quote
    @has_permissions(manage_messages=True)
    async def remove_quote(self, ctx, quote_nr):
        sql_quotes.remove_quote(int(quote_nr))
        await ctx.send(f'Quote #{quote_nr} deleted')

    @commands.command(aliases=['edit_quote', 'mod_quote'])  # modifies quote for server
    @has_permissions(manage_messages=True)
    async def update_quote(self, ctx, quote_nr: int):
        author = re.search(r'(\s[^-"]*$)', ctx.message.content)
        quote = re.search(r'(")([^"]*)(")', ctx.message.content)
        quote_link = re.search(r'http[s]?://[^"]+', ctx.message.content)
        if author and quote:  # if both name and quote is provided
            sql_quotes.update_quote(int(quote_nr), str(quote.group(2)), author.group(1)[1:])  # quote_nr, actual quote, quote author
            await ctx.send(f'Quote #{quote_nr} updated')
        elif quote_link:  # if only quote is provided (mainly screenshots/links)
            sql_quotes.update_quote_no_user(int(quote_nr), str(quote_link.group(0)))
            await ctx.send(f'Quote #{quote_nr} updated')
        else:
            await ctx.send('Wrong format, use `quote_nr` `"<quote>" - <user>|<link>`')

    @commands.command()  # gets count of how many quotes user has
    async def qcount(self, ctx, user):
        q_count = sql_quotes.get_quote_count()  # first element is username, second is quote count

        q_result = list()
        for quote in q_count:
            if (fuzz.token_sort_ratio(user, quote[0]) > 50):
                q_result.append(quote)

        if not q_result:  # if <user> param is not found in db
            await ctx.send('I have no idea who that is')
        
        q_count = q_result[0]  # this is some real tuple fuckery
        if q_count[1] == 1:
            await ctx.send(f'{q_count[0]} has said only one interesting thing.')
        else:
            await ctx.send(f'{q_count[0]} has said {q_count[1]} interesting things.')


def setup(bot):
    bot.add_cog(QuotesCog(bot))
