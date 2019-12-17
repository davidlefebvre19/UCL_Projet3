from subprocess import call

def IsMessage():
	#verifie la presence du message, True si message present, False si absence de message
	try:
		f = open("/betap3/UCL_Projet3/message.txt", "r")
		message = f.read()
		f.close()
		return True
	except:
		return False

if IsMessage():
	#si un message est present, executer le code normalement
	call("cd betap3/UCL_Projet3 && python3 main.py", shell=True)
else:
	#si aucun message n'est present, ecraser le code avec le derniere version trouvee sur GitHub
	call("cd betap3 && sudo rm -rf UCL_Projet3 && git clone https://github.com/davidlefebvre19/UCL_Projet3.git", shell=True)
	call("cd UCL_Projet3 && python3 main.py", shell=True)