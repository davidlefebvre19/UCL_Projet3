from sense_hat import SenseHat, ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED
sense = SenseHat()
sense.low_light = True
from time import sleep
from signal import pause
from subprocess import call
i = 0

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