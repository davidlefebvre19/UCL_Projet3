#!/usr/bin/env python3
from sense_hat import SenseHat, ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED
sense = SenseHat()
sense.low_light = True
import time
from time import sleep
from signal import pause
from subprocess import call

#couleurs utilisees pour le logo et l'interface
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
orange = (128,255,0)
yellow = (255, 255, 0)
blue = (0, 0, 255)
red = (255, 0, 0)
nothing = (0,0,0)
pink = (255,105, 180)
mauve = (194,46,220)

#True si message present
code_in_rpi = False

#clef de vigenere
key = "louvain"

#message secret 
message = []

#variable de la fonction confirmer
i = 0

#ecoute les actions du joystick si true
joystick = True

#mot de passe, chaque position correspond a chiffre que l'on incremante a cette liste
liste_action = []

#logo
def XenonDuck():
    G = green
    R = red
    W = white
    O = nothing
    B = blue
    Y = yellow
    M = mauve
    logo = [
    O, W, W, W, W, W, W, W,
    O, O, W, W, W, W, W, W,
    O, O, W, W, W, W, W, W,
    O, B, B, B, B, B, B, B,
    O, B, B, W, B, B, B, W,
    Y, Y, Y, W, W, W, W, W,
    O, O, W, W, W, W, W, W,
    O, O, W, W, W, W, W, W,
    ]
    sense.set_pixels(logo)
    time.sleep(2)

def ReadMessage():
    """
    Verifie si il existe deja un message crypte dans message.txt
    :return (boolean): True si un message est deja present / False dans le cas contraire
    """
    try:
        f = open("message.txt", "r")
        message = f.read()
        f.close()
        return True
    except:
        print("no message")
        return False

def encode(key , plain_text ): #Fonction chiffrant le message selon le chiffrement vigenere
    """
    Chiffre un texte en utilisant une clé de chiffrement.
    Les deux arguments sont fournis sous la forme d'une chaine de caractères.
    L'algorithme utilisé est le chiffrement de Vigenère.
    Attention : cette méthode est "craquée" depuis longtemps, mais elle illustre le fonctionnement d'un algorithme de chiffrement.

    :param (str) key: la clé symmétrique
    :param (str) plain_text: le texte à chiffrer
    :return (str): le texte chiffré
    """
    enc = []
    for i, e in enumerate(plain_text):
        key_c = key[i % len(key)]
        enc_c = chr((ord(e) + ord(key_c)) % 256)
        enc.append(enc_c)
    return ("".join(enc).encode()).decode()

def decode(key, cipher_text): #Fonction dechiffrant le message selon le chiffrement vigenere
    dec = []
    for i, e in enumerate(cipher_text):
        key_c = key[i % len(key)]
        dec_c = chr((256 + ord(e) - ord(key_c)) % 256)
        dec.append(dec_c)
    return str("".join(dec))

def hashing(list):
    string = ''.join(list)
    def to_32(value):
        value = value % (2 ** 32)
        if value >= 2**31:
            value = value - 2 ** 32
        value = int(value)
        return value

    if string:
        x = ord(string[0]) << 7
        m = 1000003
        for c in string:
            x = to_32((x*m) ^ ord(c))
        x ^= len(string)
        if x == -1:
            x = -2
        return str(x)
    return ""

def WriteAndEncodeMessage(message):
    """
    crypte le message dans un fichier appele message.txt
    prends en parametre une string a crypter
    :param (str) string contenant le message
    """
    str(message)
    f = open("message.txt", "w")
    f.write(encode(key,"".join(message)))
    f.close()

def WriteAndEncodeHashing(code):
    """
    Hash le message dans un fichier appele message.txt
    prends en parametre une string a crypter
    :param (str) string contenant le message
    """
    str(code)
    f = open("code.txt", "w")
    f.write(hashing("".join(code)))
    f.close()

def confirmer():
	"""
	Affiche sur la matrix du sensehat un message qui demande a l'utilisateur de confirmer son choix
	Ensuite celui-ci doit selectionner entre Y ou N a l'aide du joystick
	return: (Boolean) True Si l'utilisateur choisit Y
	return: (Boolean) False si l'utilisateur choisit N
	"""
    l = ["Y","N"]
    i = 0
    sense.show_message("Sure?", back_colour=green, scroll_speed=0.04)
    sense.show_letter(l[i])
    while joystick:
        event = sense.stick.wait_for_event()
        if event.action == "pressed" and event.direction == "middle" and event.action != ACTION_RELEASED:
            if i == 0:
                sense.show_letter("Y", back_colour = green)
                print("confirmed")
                return True
            else:
                sense.show_letter("N", back_colour = red)
                print("non confirmed")
                return False
        if event.action == "pressed" and event.direction == "left" and event.action != ACTION_RELEASED:
            i -= 1
            if i%2 == 0: i=0
            if i%2 != 0: i=1
            sense.show_letter(l[i])
        if event.action == "pressed" and event.direction == "right" and event.action != ACTION_RELEASED:
            i += 1
            if i%2 == 0: i=0
            if i%2 != 0: i=1
            sense.show_letter(l[i])
        if event.action == "pressed" and event.direction == "up" and event.action != ACTION_RELEASED:
            i += 1
            if i%2 == 0: i=0
            if i%2 != 0: i=1
            sense.show_letter(l[i])
        if event.action == "pressed" and event.direction == "down" and event.action != ACTION_RELEASED:
            i -= 1
            if i%2 == 0: i=0
            if i%2 != 0: i=1
            sense.show_letter(l[i])

def confirmer_wsure():
	"""
	L'utilisateur doit selectionner entre Y ou N a l'aide du joystick (aucun message n'est affiche a l'ecran a part Y/N)
	return: (Boolean) True Si l'utilisateur choisit Y
	return: (Boolean) False si l'utilisateur choisit N
	"""
    l = ["Y","N"]
    i = 0
    sense.show_letter(l[i])
    while joystick:
        event = sense.stick.wait_for_event()
        if event.action == "pressed" and event.direction == "middle" and event.action != ACTION_RELEASED:
            if i == 0:
                sense.show_letter("Y", back_colour = green)
                print("confirmed")
                return True
            else:
                sense.show_letter("N", back_colour = red)
                print("non confirmed")
                return False
        if event.action == "pressed" and event.direction == "left" and event.action != ACTION_RELEASED:
            i -= 1
            if i%2 == 0: i=0
            if i%2 != 0: i=1
            sense.show_letter(l[i])
        if event.action == "pressed" and event.direction == "right" and event.action != ACTION_RELEASED:
            i += 1
            if i%2 == 0: i=0
            if i%2 != 0: i=1
            sense.show_letter(l[i])
        if event.action == "pressed" and event.direction == "up" and event.action != ACTION_RELEASED:
            i += 1
            if i%2 == 0: i=0
            if i%2 != 0: i=1
            sense.show_letter(l[i])
        if event.action == "pressed" and event.direction == "down" and event.action != ACTION_RELEASED:
            i -= 1
            if i%2 == 0: i=0
            if i%2 != 0: i=1
            sense.show_letter(l[i])


def ReadInput():
    """
    Cette fonction guette les mouvements effectue sur le joystick
    Elle permet d'offrir une interface a l'utilisateur afin qu'il rentre le message a crypter
    Si l'utilisateur confirme le message, le fichier GyroIn, permettant d'entrer un code, est appelle.
    """
    value = 0
    sense.show_message("Welcome", text_colour=white, back_colour=red, scroll_speed=0.05)
    sense.show_letter(str(value))

    while joystick:
        event = sense.stick.wait_for_event()
        if event.action == "held" and event.direction == "middle" and event.action != ACTION_RELEASED:
            sense.show_message(message, text_colour = white, back_colour = green, scroll_speed=0.05)
            if confirmer():
                print("GyroIn")
                return True
            else:
                call("sudo shutdown now", shell=True)
        if event.action == "pressed" and event.direction == "middle" and event.action != ACTION_RELEASED:
            sense.show_letter(str(value), back_colour = green)
            message.append(str(value))
            sleep(0.2)
            sense.show_letter(str(value))
        if event.action == "pressed" and event.direction == "left" and event.action != ACTION_RELEASED:
            value -= 1
            if value < 0: value=9
            if value > 9: value=0
            sense.show_letter(str(value))
        if event.action == "pressed" and event.direction == "right" and event.action != ACTION_RELEASED:
            value += 1
            if value < 0: value=9
            if value > 9: value=0
            sense.show_letter(str(value))
        if event.action == "pressed" and event.direction == "up" and event.action != ACTION_RELEASED:
            value += 1
            if value < 0: value=9
            if value > 9: value=0
            sense.show_letter(str(value))
        if event.action == "pressed" and event.direction == "down" and event.action != ACTION_RELEASED:
            value -= 1
            if value < 0: value=9
            if value > 9: value=0
            sense.show_letter(str(value))

def GyroIn():
	"""
	Permet de creer un mot de passe a l'aide de l'accelerometere
	L'utilisateur doit confirmer chaque position en pressant le joystick
	L'utilisateur confirme le code en maintenant le click du joystick
	Cette fonction fais aussi appel a la fonction confirmer() pour etre sur du choix de l'utilisateur
	Elle fait egalement appel a la fonction hashing pour hasher le code et l'enregistrer sur un fichier .txt
	return: (Boolean) True si l'utilisateur confirme le code, le RPI s'etteinds si l'utilisateur ne souhaite pas enregistrer le code
	"""
    sense.show_message("Create password", text_colour=orange, scroll_speed=0.05)
    movements = []
    mouvement = 0
    while joystick:
        sense.show_letter(str(mouvement))
        event = sense.stick.wait_for_event()
        if event.action == "pressed" and event.direction == "middle" and event.action != ACTION_RELEASED:
            x = round(sense.get_accelerometer_raw()["x"])
            y = round(sense.get_accelerometer_raw()["y"])
            z = round(sense.get_accelerometer_raw()["z"])
            if y == 0 and x == 0 and z == 1 :
                action = "1"
                movements.append(action)
            if y == 0 and x == -1 and z == 0 :
                action = "2"
                movements.append(action)
            if y == 0 and x == -1 and z == -1 :
                action = "3"
                movements.append(action)
            if y == 0 and x == 1 and z == 0 :
                action = "4"
                movements.append(action)
            if y == 0 and x == 1 and z == -1 :
                action = "5"
                movements.append(action)
            if y == 1 and x == 0 and z == 0 :
                action = "6"
                movements.append(action)
            if y == -1 and x == 0 and z == 0 :
                action = "7"
                movements.append(action)
            if y == 0 and x == 0 and z == -1 :
                action = "8"
                movements.append(action)
            mouvement += 1
            sense.show_letter(str(mouvement))
        if event.action == "held" and event.direction == "middle":
            if confirmer():
                print(movements, "in")
                WriteAndEncodeHashing(movements)
                #le RPI est eteinds qu'elle que soit la decision de l'utilisateur
                return True
            else:
                XenonDuck()
                call("sudo rm message.txt && shutdown now", shell=True)

def CheckCode(movements):
	"""
	Recupere la liste du code a tester et le hashe.
	Ouvre ensuite le fichier code.txt contenant le code correct hashe
	Compare les deux codes hashes
	return: (Boolean) True si le code est correct
	return: (Boolean) False si ne l'est pas
	"""
    uncheckedcode = hashing(movements)
    print(uncheckedcode)
    f = open("code.txt", "r")
    checkedcode = f.read()
    print("good code: ",checkedcode," unchecked code: ",uncheckedcode)
    if uncheckedcode == checkedcode:
        return True
    else:
        return False

def GyroOut():
	"""
	Permet de creer un mot de passe a l'aide de l'accelerometere
	L'utilisateur doit confirmer chaque position en pressant le joystick
	L'utilisateur confirme le code en maintenant le click du joystick
	Cette fonction fais aussi appel a la fonction confirmer() pour etre sur du choix de l'utilisateur
	Elle fait egalement appel a la fonction CheckCode pour verifier l'exactitude du mot de passe entre
	return: (Boolean) True si l'utilisateur confirme le code, le RPI s'etteinds si l'utilisateur ne souhaite pas enregistrer le code
	"""

    liste_action_entree = []
    sense.show_message("Enter password", text_colour=orange, scroll_speed=0.05)
    mouvement = 0
    while joystick:
        sense.show_letter(str(mouvement))
        event = sense.stick.wait_for_event()
        if event.action == "pressed" and event.direction == "middle" and event.action != ACTION_RELEASED:
            x = round(sense.get_accelerometer_raw()["x"])
            y = round(sense.get_accelerometer_raw()["y"])
            z = round(sense.get_accelerometer_raw()["z"])
            if y == 0 and x == 0 and z == 1 :
                action = "1"
                liste_action_entree.append(action)
            if y == 0 and x == -1 and z == 0 :
                action = "2"
                liste_action_entree.append(action)
            if y == 0 and x == -1 and z == -1 :
                action = "3"
                liste_action_entree.append(action)
            if y == 0 and x == 1 and z == 0 :
                action = "4"
                liste_action_entree.append(action)
            if y == 0 and x == 1 and z == -1 :
                action = "5"
                liste_action_entree.append(action)
            if y == 1 and x == 0 and z == 0 :
                action = "6"
                liste_action_entree.append(action)
            if y == -1 and x == 0 and z == 0 :
                action = "7"
                liste_action_entree.append(action)
            if y == 0 and x == 0 and z == -1 :
                action = "8"
                liste_action_entree.append(action)
            mouvement += 1
            sense.show_letter(str(mouvement))
        if event.action == "held" and event.direction == "middle" and event.action != ACTION_RELEASED:
            if confirmer():
                print(liste_action_entree, "out")
                if CheckCode(liste_action_entree):
                    return True
                else: return False
            else:
                i = "retry"
                return i

def Show_Decrypted():
	"""
	Affiche sur la matrix du sensehat le message secret apres l'avoir decrypte
	"""
    f = open("message.txt", "r")
    encrypted_message = f.read()
    f.close()
    message = decode(key, encrypted_message)
    sense.show_message(message, text_colour=orange)

def DetruireLesPreuvesALerteRouge():
	"""
	Cette fonction est appellee si l'utilisateur se trompe 3x de code
	Elle detruit le fichier message.txt et code.txt tout en informant l'utilisateur de leurs suppression
	Le RPI s'eteind apres la suppression des fichiers
	"""
    sense.show_message("Autodestruction du code", back_colour=red, scroll_speed=0.04)
    call("sudo rm message.txt && rm code.txt", shell=True)
    sense.show_message("Message detruit", back_colour=red, scroll_speed=0.04)
    XenonDuck()
    call("sudo shutdown now", shell=True)

def ExpectPassword():
	"""
	Cette fonction permet de faire le liens entre toutes les fonctions pour entrer un code a tester et verifier si il est correct
	Cette fonction efface le message et le code si l'utilisateur se trompe plus de 3 fois

	"""


    #compteur d'erreurs. Si il est superieur a 3, le message s'autodetruit
    erreurs = 0

    print("l'utilisateur doit enter le code")
    while erreurs < 3:
        gyroout = GyroOut()
        if gyroout == True:
            Show_Decrypted()
            Show_Decrypted()
            sense.show_message("delete message?", text_colour=blue, scroll_speed=0.05)
            if confirmer_wsure():
                XenonDuck()
                call("sudo rm code.txt && sudo rm message.txt && sudo shutdown now", shell=True)
            else:
                XenonDuck()
                call("sudo shutdown now", shell=True)
        elif gyroout == False:
            sense.show_message("incorrect", back_colour=red, scroll_speed=0.05)
            erreurs += 1
    DetruireLesPreuvesALerteRouge()


XenonDuck()
if not ReadMessage():
    if ReadInput():
        WriteAndEncodeMessage(message)
        if GyroIn():
            black = (0,0,0)
            sense.show_message("shutdown?", text_colour=blue, scroll_speed=0.05)
            if confirmer_wsure():
                call("sudo shutdown now", shell=True)
            else:
                ExpectPassword()
else:
    ExpectPassword()





