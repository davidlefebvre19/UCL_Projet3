from sense_hat import SenseHat, ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED
sense = SenseHat()
sense.low_light = True
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

import os

def CheckIfMessage():
    try:
        os.path.isfile('/betap3/UCL_Projet3/message.txt')
        print("message found")
        return True
    else:
        print("message not found")
        return False

if CheckIfMessage():
    call("cd betap3 && sudo rm -rf UCL_Projet3 && git clone https://github.com/davidlefebvre19/UCL_Projet3.git", shell=True)
    call("cd UCL_Projet3 && python3 main.py", shell=True)
else:
    call("cd betap3/UCL_Projet3 && python3 main.py", shell=True)

"""
def confirmer():
    l = ["Y","N"]
    i = 0
    sense.show_message("Sure?", back_colour=green, scroll_speed=0.03)
    sense.show_letter(l[i])
    while joystick:
        event = sense.stick.wait_for_event()
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
            if i%2 == 0: i=0
            if i%2 != 0: i=1
            sense.show_letter(l[i])
        if event.action == "pressed" and event.direction == "right":
            i += 1
            if i%2 == 0: i=0
            if i%2 != 0: i=1
            sense.show_letter(l[i])
        if event.action == "pressed" and event.direction == "up":
            i += 1
            if i%2 == 0: i=0
            if i%2 != 0: i=1
            sense.show_letter(l[i])
        if event.action == "pressed" and event.direction == "down":
            i -= 1
            if i%2 == 0: i=0
            if i%2 != 0: i=1
            sense.show_letter(l[i])

if confirmer():
    print("returned True")
else:
    print("returned False")
"""
"""
def confirmer():
    #demande a l'utilisateur de confirmer son choix en choisissant "V" avec le joystick, "F", si il ne souhaite pas confirmer.
    #:return (boolean) True si l'utilisateur choisit "V" et inversement
    sense.show_letter(l[i])


    def Up(event):
        global i
        if event.action != ACTION_RELEASED:
            i += 1
            if i>1: i=0
            if i<1: i=1
            sense.show_letter(l[i])

    def Down(event):
        global i
        if event.action != ACTION_RELEASED:
            i -= 1
            if i>1: i=0
            if i<1: i=1
            sense.show_letter(l[i])


    def Select(event):
        global i
        if event.action == ACTION_RELEASED:
            if i == 0:
                sense.show_letter("V", back_colour = green)
                print("yes")
                return True
            else:
                sense.show_letter("F", back_colour = red)
                print("oui")
                return False

    sense.stick.direction_up = Up
    sense.stick.direction_down = Down
    sense.stick.direction_left = Down
    sense.stick.direction_right = Up
    sense.stick.direction_middle = Select
    pause()
"""

"""
confirmed = confirmer()
if confirmed:
    call("python3 main.py", shell=True)
    print("yes")
"""

    """
    def Up(event):
        #si l'utilisateur pousse le joystick vers le haut ou vers la droite, on incrmante 1 au compteur
        #la valeur du compteur est toujours comprise dans l'intervalle ferme [0,9].
        global value
        if 9+:
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
                return True
                print("2.5")


    sense.stick.direction_up = Up
    sense.stick.direction_down = Down
    sense.stick.direction_left = Down
    sense.stick.direction_right = Up
    sense.stick.direction_middle = Select
    pause()
    """
"""
def confirmer():
    #demande a l'utilisateur de confirmer son choix en choisissant "V" avec le joystick, "F", si il ne souhaite pas confirmer.
    #:return (boolean) True si l'utilisateur choisit "V" et inversement
    i = 1
    sense.show_letter(confirm[i])

    def Up(event):
        if event.action != ACTION_RELEASED:
            i += 1
            if i>1: i=0
            if i<1: i=1
            if i == 1:
                sense.show_letter("F", text_colour=red)
            else:
                sense.show_letter("V", text_colour=green)

    def Down(event):
        if event.action != ACTION_RELEASED:
            i += 1
            if i>1: i=0
            if i<1: i=1
            if i == 1:
                sense.show_letter("F", text_colour=red)
            else:
                sense.show_letter("V", text_colour=green)

    def Select(event):
            if event.action == ACTION_RELEASED:
                if i == 0
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
"""

