from sense_hat import SenseHat, ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED
sense = SenseHat()
sense.low_light = True
from time import sleep
from signal import pause
from subprocess import call
l = ["V","F"]
i = 0
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)

sense.clear()
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
                print("shit")
                return False

    sense.stick.direction_up = Up
    sense.stick.direction_down = Down
    sense.stick.direction_left = Down
    sense.stick.direction_right = Up
    sense.stick.direction_middle = Select
    pause()

confirmed = confirmer()
if confirmed:
    print("yes")