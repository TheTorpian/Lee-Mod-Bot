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
    ban_count = r''  # path to ban_count file


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


def add_ban(user):  # var user needs to be the user.id
    with open(Vars.ban_count, 'r') as f:  # read ban_count file into lines var
        lines = f.readlines()
    user_new = True
    with open(Vars.ban_count, 'w') as f:  # rewrite ban_count file
        for line in lines:
            if user in line:  # if given user is in list
                newcount = int(line.strip('\n')[-1]) + 1  # increment the ban count by one
                newline = f'{user} {newcount}\n'
                f.write(newline)  # writes the modified line
                user_new = False
            else:
                f.write(line)  # rewrites old line if no need to modify
        if user_new:
            f.write(f'{user} 1\n')  # if user doesn't exist in list, it gets added


def get_ban_count(user):  # get ban/mute count
    with open(Vars.ban_count, 'r') as f:
        lines = f.readlines()
    for line in lines:
        if user in line:
            return line.strip('\n')[-1]
