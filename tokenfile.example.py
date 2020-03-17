from discord.ext import commands
import mysql.connector as mysql

connection = None


def init_db():
    return mysql.connect(
        host="",
        user="",
        password="",
        database=""
    )


def get_cursor(conn):
    try:
        conn.ping(reconnect=True, attempts=3, delay=5)
    except mysql.Error:
        conn = init_db()
    return conn.cursor()


connection = init_db()


class Vars:
    INVITE = ''  # bot invite link
    TOKEN = ''  # bot app link
    torp_tag = 249550049564950530  # big torpo's tag
    lee_tag = 384297196113231882
    poleece_tag = 653600602764607498  # bot's tag
    deleted_messages_channel = 660102195504742400  # deleted messages channel
    ignored_channels = r''  # path to ignored_channels file


def user_is_torp():
    def predicate(ctx):
        return ctx.message.author.id == Vars.torp_tag
    return commands.check(predicate)


def check_ignore(ctx, channel):  # function that checks if channel id is in ignored_channels file (returns false if it is)
    channel = str(channel)
    with open(Vars.ignored_channels) as f:
        if str(channel) in f.read():
            f.close()
            return False
        else:
            f.close()
            return True
