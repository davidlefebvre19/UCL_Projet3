from sense_hat import SenseHat, ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED
sense = SenseHat()
sense.low_light = True
from time import sleep
from signal import pause

#9Q4hr6iM

code_in_rpi = False
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
key = louvain
code = []
value = 0

def hashing(string): #fonction hachant la clef
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

def encode(key , plain_text ): #Fonction chiffrant le message selon le chiffrement vigenere
    enc = []
    for i, e in enumerate(plain_text):
        key_c = key[i % len(key)]
        enc_c = chr((ord(e) + ord(key_c)) % 256)
        enc.append(enc_c)
    return ("".join(enc).encode()).decode()

def CheckCode():
	#permet de verifier si il existe deja un code meme apres avoir eteinds le rpi
	#return True si un code est present
	return False 

def GyroCode():
	liste_action = [] #liste de stockage des positions dans l espace
	tourne = True
	while tourne :
	    sense.show_letter(str(len(liste_action)))
	    event = sense.stick.wait_for_event()
	    if event.action == "pressed" and event.direction == "middle" : #pression sur le joystick pour ajouter une position
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
	    if event.action == "held" and event.direction == "middle" :
	        sense.show_message("Valider?",scroll_speed = 0.05)
	        conserver = True
	        validation = True
	        delete = False
	        while validation :
	            while conserver :
	                sense.show_letter("V",(0, 255, 0))
	                for event in sense.stick.get_events(): # Si on valide en appuyant au milieu, le message sera conserve, une autre action proposera le x
	                    if event.action == 'pressed' and event.direction == "middle":
	                        tourne = False
	                        conserver = False
	                        validation = False
	                        sense.clear()
	                        f= open("key.txt","w") #ouvre le document message.txt
	                        f.write(hashing("".join(liste_action))) #ecrit la clef hashee
	                        f.close()
	                    if event.action == "pressed" and event.direction != "middle" :
	                        conserver = False
	                        delete = True
	            while delete :
	                sense.show_letter("X",(255, 0, 0))
	                for event in sense.stick.get_events(): # Si on valide en appuyant au milieu, le message sera supprime, une autre action recommencera la bouche
	                    if event.action == 'pressed' and event.direction == "middle":
	                        delete = False
	                        validation = False
	                        sense.clear()
	                        liste_action = []
	                    if event.action == "pressed" and event.direction != "middle" :
	                        conserver = True
	                        delete = False


def Up(event):
	    global value
	    if event.action != ACTION_RELEASED:
	        value += 1
	        if value < 0: value=9
	        if value > 9: value=0
	        sense.show_letter(str(value))

def Down(event):
    global value
    if event.action != ACTION_RELEASED:
        value -= 1
        if value < 0: value=9
        if value > 9: value=0
        sense.show_letter(str(value))

def Select(event):
    global value
    if event.action != ACTION_PRESSED:
        if event.action == ACTION_RELEASED:
            sense.show_letter(str(value), back_colour = green)
            code.append(str(value))
            sleep(0.2)
            sense.show_letter(str(value))
            GyroCode()
        else:
			f = open("message.txt", "w")
            f.write(encode(key,"".join(code)))
            f.write(code)
            f.close()
            sense.clear()
