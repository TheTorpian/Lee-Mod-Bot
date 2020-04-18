import tokenfile
from tokenfile import connection

db = connection


def get_bancount(u_id):  # gets nr of offenses
    cursor = tokenfile.get_cursor(connection)
    query = 'SELECT offense_count FROM Offense WHERE user_id = %s'
    cursor.execute(query, (str(u_id),))
    bancount = cursor.fetchone()
    return bancount


def add_ban(u_id, offense_count):  # adds new user to ban count
    cursor = tokenfile.get_cursor(connection)
    query = 'INSERT INTO Offense (user_id, offense_count) VALUES (%s, %s)'
    cursor.execute(query, (u_id, offense_count))
    db.commit()


def alter_ban(u_id, offense_count):  # modifies offense count for user
    cursor = tokenfile.get_cursor(connection)
    query = 'UPDATE Offense SET offense_count = %s WHERE user_id = %s'
    cursor.execute(query, (offense_count, u_id))
    db.commit()
