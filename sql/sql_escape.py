import tokenfile
from tokenfile import connection

db = connection


def get_time():  # fetch last time escape was used
    cursor = tokenfile.get_cursor(connection)
    query = 'SELECT cooldown FROM Escape'
    cursor.execute(query,)
    cooldown = cursor.fetchone()
    return cooldown


def update_time(new_cooldown):  # updates when escape was used
    cursor = tokenfile.get_cursor(connection)
    query = 'UPDATE Escape SET cooldown = %s WHERE id = 1'
    cursor.execute(query, (new_cooldown,))
    db.commit()
