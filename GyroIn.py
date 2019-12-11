from sense_hat import SenseHat, ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED
sense = SenseHat()
sense.low_light = True
from time import sleep
from signal import pause
from subprocess import call

white = (255,255,255)
red = (255,0,0)
green = (0,255,0)

sense.show_message("Enter code", text_colour = white, back_colour= green)

liste_action = []
action = 0
joystick = True


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
	    		WriteAndEncode(liste_action)
	    		#le RPI est eteinds qu'elle que soit la decision de l'utilisateur
	    		call("sudo shutdown now", shell=True)
	    	else:
	    		call("sudo shutdown now", shell=True)






