class Vars:
	INVITE = 'https://discordapp.com/api/oauth2/authorize?client_id=653600602764607498&permissions=8&scope=bot'  # bot invite link
	TOKEN = 'NjUzNjAwNjAyNzY0NjA3NDk4.Xe5XYA.vm1fbpNyRYWqOie-Tb-2zlKimCk'  # bot app link
	torp_tag = 249550049564950530  # big torpo's tag
	restart_bat = r"C:\Users\Alex\Documents\Github\Lees Mod Bot\restart.bat"  # path to restart batch file

	def user_is_me(ctx):
		return ctx.message.author.id == Vars.torp_tag
