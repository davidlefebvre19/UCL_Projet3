from sense_hat import SenseHat, ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED
sense = SenseHat()
sense.low_light = True
from time import sleep
from signal import pause
from subprocess import call
#9Q4hr6iM

code_in_rpi = False
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
orange = (128,255,0)
key = "louvain"
message = []
i = 0
joystick = True
liste_action = []
action = 0

sense.clear()

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
        return False

def WriteAndEncodeMessage(message):
    """
    crypte le message dans un fichier appele message.txt
    prends en parametre une string a crypter
    :param (str) string contenant le message
    """
    str(message)
    f = open("message", "w")
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
    f.write(hashing(key,"".join(code)))
    f.close()


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

def confirmer():
    l = ["V","F"]
    i = 0
    sense.show_message("Confirm :", text_colour=orange)
    sense.show_letter(l[i])
    while joystick:
        event = sense.stick.wait_for_event()
        if event.action == "pressed" and event.direction == "middle":
            if i == 0:
                sense.show_letter("Y", back_colour = green)
                print("yes")
                return True
            else:
                sense.show_letter("N", back_colour = red)
                print("non")
                return False
        if event.action == "pressed" and event.direction == "left":
            i -= 1
            if i>1: i=0
            if i<1: i=1
            sense.show_letter(l[i])
        if event.action == "pressed" and event.direction == "right":
            i += 1
            if i>1: i=0
            if i<1: i=1
            sense.show_letter(l[i])
        if event.action == "pressed" and event.direction == "up":
            i += 1
            if i>1: i=0
            if i<1: i=1
            sense.show_letter(l[i])
        if event.action == "pressed" and event.direction == "down":
            i -= 1
            if i>1: i=0
            if i<1: i=1
            sense.show_letter(l[i])




def ReadInput():
    """
    Cette fonction guette les mouvements effectue sur le joystick
    Elle permet d'offrir une interface a l'utilisateur afin qu'il rentre le message a crypter
    Si l'utilisateur confirme le message, le fichier GyroIn, permettant d'entrer un code, est appelle.
    """
    value = 0
    sense.show_message("Hello Kormrade", text_colour=white, back_colour=red, scroll_speed=0.005)
    sense.show_letter(str(value))

    while joystick:
        event = sense.stick.wait_for_event()
        if event.action == "held" and event.direction == "middle":
            sense.show_message(message, text_colour = white, back_colour = green, scroll_speed=0.05)
            if confirmer():
                print("GyroIn")
                return True
            else:
                call("sudo shutdown now", shell=True)
        if event.action == "pressed" and event.direction == "middle":
            sense.show_letter(str(value), back_colour = green)
            message.append(str(value))
            sleep(0.2)
            sense.show_letter(str(value))
        if event.action == "pressed" and event.direction == "left":
            value -= 1
            if value < 0: value=9
            if value > 9: value=0
            sense.show_letter(str(value))
        if event.action == "pressed" and event.direction == "right" :
            value += 1
            if value < 0: value=9
            if value > 9: value=0
            sense.show_letter(str(value))
        if event.action == "pressed" and event.direction == "up" :
            value += 1
            if value < 0: value=9
            if value > 9: value=0
            sense.show_letter(str(value))
        if event.action == "pressed" and event.direction == "down" :
            value -= 1
            if value < 0: value=9
            if value > 9: value=0
            sense.show_letter(str(value))

def GyroIn():
    while joystick:
        sense.show_letter(str(action))
        event = sense.stick.wait_for_event()
        if event.action == "pressed" and even.direction == "middle":
            x = round(sense.get_accelerometer_raw()["x"])
            y = round(sense.get_accelerometer_raw()["y"])
            z = round(sense.get_accelerometer_raw()["z"])
            if y == 0 and x == 0 and z == 1 :
                action = "Nothing"
                liste_action.append(action)
            if y == 0 and x == -1 and z == 0 :
                action = "turnleft"
                liste_action.append(action)
            if y == 0 and x == -1 and z == -1 :
                action = "flipleft"
                liste_action.append(action)
            if y == 0 and x == 1 and z == 0 :
                action = "turnright"
                liste_action.append(action)
            if y == 0 and x == 1 and z == -1 :
                action = "flipright"
                liste_action.append(action)
            if y == 1 and x == 0 and z == 0 :
                action = "turnbackward"
                liste_action.append(action)
            if y == -1 and x == 0 and z == 0 :
                action = "turnforward"
                liste_action.append(action)
            if y == 0 and x == 0 and z == -1 :
                action = "flipbackward"
                liste_action.append(action)
        if event.action == "held" and event.direction == "middle":
            sense.show_message("Are you sure ?", scroll_speed = 0.05)
            confirmer()
            if confirmer():
                WriteAndEncodeHashing(liste_action)
                #le RPI est eteinds qu'elle que soit la decision de l'utilisateur
                call("sudo shutdown now", shell=True)
            else:
                call("sudo shutdown now", shell=True)

if not ReadMessage():
    if ReadInput():
        WriteAndEncodeMessage(message)
        GyroIn()

