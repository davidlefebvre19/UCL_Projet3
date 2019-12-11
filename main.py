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
    l = ["Y","N"]
    i = 0
    sense.show_message("Sure?", back_colour=green, scroll_speed=0.03)
    sense.show_letter(l[i])
    while joystick:
        event = sense.stick.wait_for_event()
        for event in sense.stick.get_events():
            if event.action == "pressed" and event.direction == "middle":
                if i == 0:
                    sense.show_letter("Y", back_colour = green)
                    print("confirmed")
                    return True
                else:
                    sense.show_letter("N", back_colour = red)
                    print("non confirmed")
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
    liste_action = []
    mouvement = 0
    while joystick:
        sense.show_letter(str(mouvement))
        event = sense.stick.wait_for_event()
        if event.action == "pressed" and event.direction == "middle":
            x = round(sense.get_accelerometer_raw()["x"])
            y = round(sense.get_accelerometer_raw()["y"])
            z = round(sense.get_accelerometer_raw()["z"])
            if y == 0 and x == 0 and z == 1 :
                action = "1"
                liste_action.append(action)
            if y == 0 and x == -1 and z == 0 :
                action = "2"
                liste_action.append(action)
            if y == 0 and x == -1 and z == -1 :
                action = "3"
                liste_action.append(action)
            if y == 0 and x == 1 and z == 0 :
                action = "4"
                liste_action.append(action)
            if y == 0 and x == 1 and z == -1 :
                action = "5"
                liste_action.append(action)
            if y == 1 and x == 0 and z == 0 :
                action = "6"
                liste_action.append(action)
            if y == -1 and x == 0 and z == 0 :
                action = "7"
                liste_action.append(action)
            if y == 0 and x == 0 and z == -1 :
                action = "8"
                liste_action.append(action)
            mouvement += 1
            sense.show_letter(str(mouvement))
        if event.action == "held" and event.direction == "middle":
            if confirmer():
                print(liste_action, "in")
                WriteAndEncodeHashing(liste_action)
                #le RPI est eteinds qu'elle que soit la decision de l'utilisateur
                return True
            else:
                call("sudo shutdown now", shell=True)

def CheckCode(liste_action):
    uncheckedcode = hashing(liste_action)
    f = open("code.txt", "r")
    checkedcode = f.read()
    print(checkedcode, uncheckedcode)
    if uncheckedcode == checkedcode:
        return True
    else:
        return False

def GyroOut():
    liste_action_entree = []
    mouvement = 0
    while joystick:
        sense.show_letter(str(mouvement))
        event = sense.stick.wait_for_event()
        if event.action == "pressed" and event.direction == "middle":
            x = round(sense.get_accelerometer_raw()["x"])
            y = round(sense.get_accelerometer_raw()["y"])
            z = round(sense.get_accelerometer_raw()["z"])
            if y == 0 and x == 0 and z == 1 :
                action = "1"
                liste_action.append(action)
            if y == 0 and x == -1 and z == 0 :
                action = "2"
                liste_action.append(action)
            if y == 0 and x == -1 and z == -1 :
                action = "3"
                liste_action.append(action)
            if y == 0 and x == 1 and z == 0 :
                action = "4"
                liste_action.append(action)
            if y == 0 and x == 1 and z == -1 :
                action = "5"
                liste_action.append(action)
            if y == 1 and x == 0 and z == 0 :
                action = "6"
                liste_action.append(action)
            if y == -1 and x == 0 and z == 0 :
                action = "7"
                liste_action.append(action)
            if y == 0 and x == 0 and z == -1 :
                action = "8"
                liste_action_entree.append(action)
            mouvement += 1
            sense.show_letter(str(mouvement))
        if event.action == "held" and event.direction == "middle":
            if confirmer():
                print(liste_action_entree, "out")
                if CheckCode(liste_action_entree):
                    return True
                else:
                    return False
            else:
                i = "retry"
                return i

def Show_Decrypted():
    f = open("message.txt", "r")
    encrypted_message = f.read()
    f.close()
    message = decode(key, encrypted_message)
    sense.show_message(message, text_colour=orange)

def DetruireLesPreuvesALerteRouge():
    sense.show_message("Autodestruction du code", text_colour=red)
    call("sudo rm message.txt && rm code.txt", shell=True)
    sense.show_message("Message detruit")
    call("sudo shutdown now", shell=True)




erreurs = 0
if not ReadMessage():
    if ReadInput():
        WriteAndEncodeMessage(message)
        if GyroIn():
            while erreurs < 2:
                GyroOut()
                if GyroOut() == True:
                    Show_Decrypted()
                    call("sudo shutdown now", shell=True)
                elif GyroOut() == False:
                    erreurs += 1
                elif GyroOut() == "retry":
                    pass
            DetruireLesPreuvesALerteRouge()

else:
    print("2")
    while erreurs < 2:
        GyroOut()
        if GyroOut() == True:
            Show_Decrypted()
            call("sudo shutdown now", shell=True)
        elif GyroOut() == False:
            erreurs += 1
        elif GyroOut() == "retry":
            pass

    DetruireLesPreuvesALerteRouge()




