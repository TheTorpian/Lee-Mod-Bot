class Vars:
    INVITE = ''  # bot invite link
    TOKEN = ''  # bot app link
    torp_tag = [249550049564950530]  # big torpo's tag
    lee_tag = 384297196113231882

    def user_is_me(ctx):
        return ctx.message.author.id in Vars.torp_tag
