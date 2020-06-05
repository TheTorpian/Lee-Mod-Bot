import os
from discord.ext import commands
import mysql.connector as mysql

dbhost = os.getenv('DBHOST')
dbuser = os.getenv('DBUSER')
dbpwd = os.getenv('DBPWD')
db = os.getenv('DB')
torp_tag = os.getenv('TORPTAG')

connection = None


def init_db():
    return mysql.connect(
        host=dbhost,
        user=dbuser,
        password=dbpwd,
        database=db
    )


def get_cursor(conn):
    try:
        conn.ping(reconnect=True, attempts=3, delay=5)
    except mysql.Error:
        conn = init_db()
    return conn.cursor()


connection = init_db()


def user_is_torp():
    def predicate(ctx):
        return ctx.message.author.id == int(torp_tag)
    return commands.check(predicate)
