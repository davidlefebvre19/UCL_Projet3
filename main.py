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
key = "louvain"
message = []
value = 0
i = 0

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

def WriteAndEncode(message):
    """
    crypte le message dans un fichier appele message.txt
    prends en parametre une string a crypter
    :param (str) string contenant le message
    """
    str(message)
    f = open("message", "w")
    f.write(encode(key,"".join(message)))
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
    #demande a l'utilisateur de confirmer son choix en choisissant "V" avec le joystick, "F", si il ne souhaite pas confirmer.
    #:return (boolean) True si l'utilisateur choisit "V" et inversement
    if i == 1:
        sense.show_letter("F", text_colour=red)
    else:
        sense.show_letter("V", text_colour=green)

    def Up(event):
        global i
        if event.action != ACTION_RELEASED:
            i += 1
            if i>1: i=0
            if i<1: i=1
            if i == 1:
                sense.show_letter("F", text_colour=red)
            else:
                sense.show_letter("V", text_colour=green)

    def Down(event):
        global i
        if event.action != ACTION_RELEASED:
            i -= 1
            if i>1: i=0
            if i<1: i=1
            if i == 1:
                sense.show_letter("F", text_colour=red)
            else:
                sense.show_letter("V", text_colour=green)

    def Select(event):
        global i
        if event.action == ACTION_RELEASED:
            if i == 0:
                sense.show_letter("V", back_colour = green)
                return True
            else:
                sense.show_letter("F", back_colour = red)
                return False

    sense.stick.direction_up = Up
    sense.stick.direction_down = Down
    sense.stick.direction_left = Down
    sense.stick.direction_right = Up
    sense.stick.direction_middle = Select
    pause()

def ReadInput():
    """
    Cette fonction guette les mouvements effectue sur le joystick
    Elle permet d'offrir une interface a l'utilisateur afin qu'il rentre le message a crypter
    Si l'utilisateur confirme le message, le fichier GyroIn, permettant d'entrer un code, est appelle.
    """
    sense.show_message("Hello Kormrade", text_colour=white, back_colour=red, scroll_speed=0.05)
    sense.show_letter(str(value))
    def Up(event):
        #si l'utilisateur pousse le joystick vers le haut ou vers la droite, on incrmante 1 au compteur
        #la valeur du compteur est toujours comprise dans l'intervalle ferme [0,9].
        global value
        if event.action != ACTION_RELEASED:
            value += 1
            if value < 0: value=9
            if value > 9: value=0
            sense.show_letter(str(value))

    def Down(event):
        #si l'utilisateur pousse le joystick vers le haut ou vers la droite, on diminue de 1 le compteur
        #la valeur du compteur est toujours comprise dans l'intervalle ferme [0,9].
        global value
        if event.action != ACTION_RELEASED:
            value -= 1
            if value < 0: value=9
            if value > 9: value=0
            sense.show_letter(str(value))

    def Select(event):
        #rajoute le chiffre affiche sur le compteur au contenu du message si l'utilisateur clique sur le joystick
        #demande une confirmation puis enregistre completement le message si le click est maintenu
        global value
        if event.action != ACTION_PRESSED:
            if event.action == ACTION_RELEASED:
                sense.show_letter(str(value), back_colour = green)
                message.append(str(value))
                sleep(0.2)
                sense.show_letter(str(value))
            else:
                sense.show_message(message, text_colour = white, back_colour = green, scroll_speed=0.05)
                confirmer()
                if confirmer():
                    WriteAndEncode(message)
                    call("python3 GyroIn.py", shell=True)
                else:
                    call("sudo shutdown now", shell=True)
         
    sense.stick.direction_up = Up
    sense.stick.direction_down = Down
    sense.stick.direction_left = Down
    sense.stick.direction_right = Up
    sense.stick.direction_middle = Select
    pause()

#si un message est present, demander le code a l'utilisateur, sinon il demande d'enregistrer un nouveau message et code
if ReadMessage():
    call("python3 GyroOut.py", shell=True)
else:
    ReadInput()