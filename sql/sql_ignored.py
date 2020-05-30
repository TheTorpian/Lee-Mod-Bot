import tokenfile
from tokenfile import connection

db = connection


def get_ignored():  # gets list of ignored channels
    cursor = tokenfile.get_cursor(connection)
    query = 'SELECT channel_id FROM Ignored_channel'
    cursor.execute(query,)
    # returns list of tuples, use double index to get actual values
    ignored = cursor.fetchall()
    return ignored


def add_ignored(c_id, c_name):  # adds channel to ignored list
    cursor = tokenfile.get_cursor(connection)
    query = 'INSERT INTO Ignored_channel (channel_id, channel_name) VALUES (%s, %s)'
    cursor.execute(query, (c_id, c_name))
    db.commit()


def remove_ignored(c_id):  # removes channel from db
    cursor = tokenfile.get_cursor(connection)
    query = 'DELETE FROM Ignored_channel WHERE channel_id = %s'
    cursor.execute(query, (c_id,))
    db.commit()


# function that checks if channel id is in ignored (returns true if it is)
def check_ignore(channel):
    ignored = get_ignored()
    if channel in ignored[0]:
        return True
    return False
