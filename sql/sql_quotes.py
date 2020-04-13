import tokenfile
from tokenfile import connection

db = connection


def add_quote(tag, quote, sv):  # adds quote to db
    cursor = tokenfile.get_cursor(connection)
    query = 'INSERT INTO Quote (quoted_tag, quote, server_id) VALUES (%s, %s, %s)'
    cursor.execute(query, (tag, quote, sv))
    db.commit()


def add_quote_no_user(quote, sv):  # adds quote to db when no username is provided
    cursor = tokenfile.get_cursor(connection)
    query = 'INSERT INTO Quote (quote, server_id) VALUES (%s, %s)'
    cursor.execute(query, (quote, sv))
    db.commit()


def remove_quote(quote_nr):  # removes quote from db
    cursor = tokenfile.get_cursor(connection)
    query = 'DELETE FROM Quote WHERE id = %s'
    cursor.execute(query, (quote_nr,))
    db.commit()


def update_quote(quote_nr, quote):  # alters quote
    cursor = tokenfile.get_cursor(connection)
    query = 'UPDATE Quote SET quote = %s WHERE id = %s'
    cursor.execute(query, (quote, quote_nr))
    db.commit()


def get_quote():  # gets a random quote from current server
    cursor = tokenfile.get_cursor(connection)
    query = 'SELECT id, quoted_tag, quote, tstamp FROM Quote'
    cursor.execute(query,)
    quotes = cursor.fetchall()  # returns list of tuples, use double index to get actual values
    return quotes


def get_last_quote():  # gets a random quote from current server
    cursor = tokenfile.get_cursor(connection)
    query = 'SELECT id FROM Quote ORDER BY id DESC LIMIT 1'
    cursor.execute(query,)
    quotes = cursor.fetchone()  # query result is just one record, this should work
    return quotes
