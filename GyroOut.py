from sense_hat import SenseHat, ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED
sense = SenseHat()
sense.low_light = True
from time import sleep
from signal import pause
from subprocess import call

liste_action = []
action = 0
ListeningToJoystick = True
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
orange = (120,255,120)

def hashing(string):
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
    while ListeningToJoystick == True:
        sense.show_letter(str(action))
        event = sense.stick.wait_for_event()
        if event.action == "pressed" and even.direction == "middle":
            x = round(sense.get_accelerometer_raw()["x"])
            y = round(sense.get_accelerometer_raw()["y"])
            z = round(sense.get_accelerometer_raw()["z"])
            if y == 0 and x == 0 and z == 1:
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
            sense.show_message("Checking code", text_colour=orange, scroll_speed = 0.05)
            return True

def hashing(string):
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

def CheckCode(liste_action):
	uncheckedcode = hashing(liste_action)
	f = open("message.txt", "r")
	checkedcode = f.read()
	if uncheckedcode == checkedcode:
		return True
	else:
		return False

ReadInput()
if ReadInput():
	if CheckCode():
		call("python3 decrypt.py", shell=True)
	else:
		for i in range (2):
			liste_action = []
			i += 1
			ReadInput()
			if CheckCode(): call("python3 decrypt.py", shell=True)
		sense.show_message("Autodestruction du code", text_colour=red)
		call("sudo rm message.txt && rm code.txt", shell=True)
		sense.show_message("Message detruit")
		call("sudo shutdown now", shell=True)

			



