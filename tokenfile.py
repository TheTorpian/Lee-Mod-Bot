class Vars:
	INVITE = ''  # bot invite link
	TOKEN = ''  # bot app link
	torp_tag = 249550049564950530  # big torpo's tag
	restart_bat = r""  # path to restart batch file

	def user_is_me(ctx):
		return ctx.message.author.id == Vars.torp_tag
