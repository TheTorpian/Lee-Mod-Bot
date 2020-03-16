import tokenfile
from tokenfile import connection

db = connection


def add_quote(tag, quote, sv):  # adds quote to db
    cursor = tokenfile.get_cursor(connection)
    query = 'INSERT INTO quote (quoted_tag, quote, server_id) VALUES (%s, %s, %s)'
    cursor.execute(query, (tag, quote, sv))
    db.commit()


def remove_quote(quote_nr):  # removes quote from db
    cursor = tokenfile.get_cursor(connection)
    query = 'DELETE FROM quote WHERE id = %s'
    cursor.execute(query, (quote_nr,))
    db.commit()


def update_quote(quote_nr, quote):  # alters quote
    cursor = tokenfile.get_cursor(connection)
    query = 'UPDATE quote SET quote = %s WHERE id = %s'
    cursor.execute(query, (quote, quote_nr))
    db.commit()


def get_quote(sv):  # gets a random quote from current server
    cursor = tokenfile.get_cursor(connection)
    query = 'SELECT id, quoted_tag, quote, tstamp FROM quote WHERE server_id = %s'
    cursor.execute(query, (sv,))
    quotes = cursor.fetchall()  # returns list of tuples, use double index to get actual values
    return quotes
